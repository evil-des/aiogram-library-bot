# Telegram Library Bot
Run your own library database right in Telegram messenger

### Short description
The application is a book management base for the library. 
The user can add and delete a book. 
The books have genres.
User is able to search for a book by title and/or author. (search through a single query)

### Complete functionality
Adding a new book:

- The user can add a new book by specifying the title, author, description and genre of the book. The user should be offered genres that are previously registered in the database. The user can also enter their own genre.

Viewing the list of books:

- The application should display a list of all books (title and author).
- User can select a book from the list to view detailed information.
- User to display books with specific genre.

Book search:

- User can enter a keyword or phrase to search.
- The application should display a list of books containing this keyword in the 'author' and 'book title' fields.

Deleting a book:

- User can select a book from the list and delete it.
- The note should be deleted from the database.


### Installation and Running (Manual)
1. Create a new .env file and change all settings:

    `cp .env.example .env`

2. Install all dependencies:

    `poetry install`
3. Set sqlalchemy.uri in alembic.ini, then run migration:

    `poetry run python -m alembic upgrade head`

4. Run Telegram bot:

    `python3 app/bot.py`


### Auto install by Docker
1. Create a new .env file:

    `cp .env.example .env.docker`

2. Change desired options in docker-compose.yml (do not forget to update sqlalchemy.uri in alembic.ini)

3. Run this command for the first time build:

    `docker-compose up -d --build`