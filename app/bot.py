import asyncio

import aiojobs
# import asyncpg as asyncpg
import orjson
import redis
import structlog
import tenacity
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram_dialog import setup_dialogs
from aiogram_dialog.setup import DialogRegistry
from aiohttp import web
from redis.asyncio import Redis

from app import handlers, utils, web_handlers
from app.data import config, genres
from app.middlewares import (
    StructLoggingMiddleware,
    DBSessionMiddleware,
    UserObjectMiddleware
)

from app.db import init_db, async_session
from app import dialogs

# DO NOT DELETE THIS LINE - it's needed for creating tables in DB
from app.models import User, Book, Genre, Author


async def create_db_connections(dp: Dispatcher) -> None:
    logger: structlog.typing.FilteringBoundLogger = dp["business_logger"]

    logger.debug("DataBase Initialization")
    await init_db()

    await genres.prepare_data()  # добавление заранее известных жанров

    if config.USE_CACHE:
        logger.debug("Connecting to Redis")
        try:
            redis_pool = await utils.connect_to_services.wait_redis_pool(
                logger=dp["cache_logger"],
                host=config.CACHE_HOST,
                password=config.CACHE_PASSWORD,
                port=config.CACHE_PORT,
                database=0,
            )
        except tenacity.RetryError:
            logger.error("Failed to connect to Redis")
            exit(1)
        else:
            logger.debug("Succesfully connected to Redis")
        dp["cache_pool"] = redis_pool

    dp["temp_bot_cloud_session"] = utils.smart_session.SmartAiogramAiohttpSession(
        json_loads=orjson.loads,
        logger=dp["aiogram_session_logger"],
    )
    if config.USE_CUSTOM_API_SERVER:
        dp["temp_bot_local_session"] = utils.smart_session.SmartAiogramAiohttpSession(
            api=TelegramAPIServer(
                base=config.CUSTOM_API_SERVER_BASE,
                file=config.CUSTOM_API_SERVER_FILE,
                is_local=config.CUSTOM_API_SERVER_IS_LOCAL,
            ),
            json_loads=orjson.loads,
            logger=dp["aiogram_session_logger"],
        )


async def close_db_connections(dp: Dispatcher) -> None:
    if "temp_bot_cloud_session" in dp.workflow_data:
        temp_bot_cloud_session: AiohttpSession = dp["temp_bot_cloud_session"]
        await temp_bot_cloud_session.close()
    if "temp_bot_local_session" in dp.workflow_data:
        temp_bot_local_session: AiohttpSession = dp["temp_bot_local_session"]
        await temp_bot_local_session.close()
    if "cache_pool" in dp.workflow_data:
        cache_pool: redis.asyncio.Redis = dp["cache_pool"]  # type: ignore[type-arg]
        await cache_pool.close()


def register_dialogs(dp: Dispatcher):
    all_dialogs = [
        dialogs.start_message.dialog,
        dialogs.add_books.dialog,
    ]
    for dialog in all_dialogs:
        dp.include_router(dialog)

    setup_dialogs(dp)  # aiogram-dialog init


def setup_handlers(dp: Dispatcher) -> None:
    dp.include_router(handlers.user.prepare_router())
    dp.include_router(handlers.book.prepare_router())

    register_dialogs(dp)


def setup_middlewares(dp: Dispatcher) -> None:
    dp.update.outer_middleware(StructLoggingMiddleware(logger=dp["aiogram_logger"]))
    dp.update.middleware(DBSessionMiddleware(session_pool=async_session))
    dp.update.middleware(UserObjectMiddleware())


def setup_logging(dp: Dispatcher) -> None:
    dp["aiogram_logger"] = utils.logging.setup_logger().bind(type="aiogram")
    dp["db_logger"] = utils.logging.setup_logger().bind(type="db")
    dp["cache_logger"] = utils.logging.setup_logger().bind(type="cache")
    dp["business_logger"] = utils.logging.setup_logger().bind(type="business")


async def setup_aiogram(dp: Dispatcher) -> None:
    setup_logging(dp)
    logger = dp["aiogram_logger"]
    logger.debug("Configuring aiogram")
    await create_db_connections(dp)
    setup_handlers(dp)
    setup_middlewares(dp)
    logger.info("Configured aiogram")


async def aiohttp_on_startup(app: web.Application) -> None:
    dp: Dispatcher = app["dp"]
    workflow_data = {"app": app, "dispatcher": dp}
    if "bot" in app:
        workflow_data["bot"] = app["bot"]
    await dp.emit_startup(**workflow_data)


async def aiohttp_on_shutdown(app: web.Application) -> None:
    dp: Dispatcher = app["dp"]
    for i in [app, *app._subapps]:  # dirty
        if "scheduler" in i:
            scheduler: aiojobs.Scheduler = i["scheduler"]
            scheduler._closed = True
            while scheduler.pending_count != 0:
                dp["aiogram_logger"].info(
                    f"Waiting for {scheduler.pending_count} tasks to complete"
                )
                await asyncio.sleep(1)
    workflow_data = {"app": app, "dispatcher": dp}
    if "bot" in app:
        workflow_data["bot"] = app["bot"]
    await dp.emit_shutdown(**workflow_data)


async def aiogram_on_startup_webhook(dispatcher: Dispatcher, bot: Bot) -> None:
    await setup_aiogram(dispatcher)
    webhook_logger = dispatcher["aiogram_logger"].bind(
        webhook_url=config.MAIN_WEBHOOK_ADDRESS
    )
    webhook_logger.debug("Configuring webhook")
    await bot.set_webhook(
        url=config.MAIN_WEBHOOK_ADDRESS.format(
            token=config.BOT_TOKEN, bot_id=config.BOT_TOKEN.split(":")[0]
        ),
        allowed_updates=dispatcher.resolve_used_update_types(),
        secret_token=config.MAIN_WEBHOOK_SECRET_TOKEN,
    )
    webhook_logger.info("Configured webhook")


async def aiogram_on_shutdown_webhook(dispatcher: Dispatcher, bot: Bot) -> None:
    dispatcher["aiogram_logger"].debug("Stopping webhook")
    await close_db_connections(dispatcher)
    await bot.session.close()
    await dispatcher.storage.close()
    dispatcher["aiogram_logger"].info("Stopped webhook")


async def aiogram_on_startup_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await setup_aiogram(dispatcher)
    dispatcher["aiogram_logger"].info("Started polling")


async def aiogram_on_shutdown_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    dispatcher["aiogram_logger"].debug("Stopping polling")
    await close_db_connections(dispatcher)
    await bot.session.close()
    await dispatcher.storage.close()
    dispatcher["aiogram_logger"].info("Stopped polling")


async def setup_aiohttp_app(bot: Bot, dp: Dispatcher) -> web.Application:
    scheduler = aiojobs.Scheduler()
    app = web.Application()
    subapps: list[tuple[str, web.Application]] = [
        ("/tg/webhooks/", web_handlers.tg_updates_app),
    ]
    for prefix, subapp in subapps:
        subapp["bot"] = bot
        subapp["dp"] = dp
        subapp["scheduler"] = scheduler
        app.add_subapp(prefix, subapp)
    app["bot"] = bot
    app["dp"] = dp
    app["scheduler"] = scheduler
    app.on_startup.append(aiohttp_on_startup)
    app.on_shutdown.append(aiohttp_on_shutdown)
    return app


def main() -> None:
    aiogram_session_logger = utils.logging.setup_logger().bind(type="aiogram_session")

    if config.USE_CUSTOM_API_SERVER:
        session = utils.smart_session.SmartAiogramAiohttpSession(
            api=TelegramAPIServer(
                base=config.CUSTOM_API_SERVER_BASE,
                file=config.CUSTOM_API_SERVER_FILE,
                is_local=config.CUSTOM_API_SERVER_IS_LOCAL,
            ),
            json_loads=orjson.loads,
            logger=aiogram_session_logger,
        )
    else:
        session = utils.smart_session.SmartAiogramAiohttpSession(
            json_loads=orjson.loads,
            logger=aiogram_session_logger,
        )
    bot = Bot(config.BOT_TOKEN, parse_mode="HTML", session=session)

    dp = Dispatcher(
        storage=RedisStorage(
            redis=Redis(
                host=config.FSM_HOST,
                password=config.FSM_PASSWORD,
                port=config.FSM_PORT,
                db=0,
            ),
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )
    )
    dp["aiogram_session_logger"] = aiogram_session_logger

    if config.USE_WEBHOOK:
        dp.startup.register(aiogram_on_startup_webhook)
        dp.shutdown.register(aiogram_on_shutdown_webhook)
        web.run_app(
            asyncio.run(setup_aiohttp_app(bot, dp)),
            handle_signals=True,
            host=config.MAIN_WEBHOOK_LISTENING_HOST,
            port=config.MAIN_WEBHOOK_LISTENING_PORT,
        )
    else:
        dp.startup.register(aiogram_on_startup_polling)
        dp.shutdown.register(aiogram_on_shutdown_polling)
        asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":
    main()
