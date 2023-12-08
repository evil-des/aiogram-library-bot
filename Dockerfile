FROM python:3.10 as python-base

# https://python-poetry.org/docs#ci-recommendations
#ENV POETRY_VERSION=1.2.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv

# Tell Poetry where to place its cache and virtual environment
ENV POETRY_CACHE_DIR=/opt/.cache

# Create stage for Poetry installation
FROM python-base as poetry-base

# Creating a virtual environment just for poetry and install it with pip
RUN python3 -m venv $POETRY_VENV \
	&& $POETRY_VENV/bin/pip install -U pip setuptools \
	&& $POETRY_VENV/bin/pip install poetry

# Create a new stage from the base python image
FROM python-base as app

# Copy Poetry to app image
COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

# Add Poetry to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /src

# Copy Dependencies
COPY . ./

# [OPTIONAL] Validate the project is properly configured
RUN poetry check

# Install Dependencies
RUN poetry install --no-interaction --no-cache --without dev

#ENV PATH "$PATH:/app/scripts"

#RUN useradd -m -d /app -s /bin/bash app \
#    && chown -R app:app /app/* && chmod +x /app/scripts/*
#
#USER app

CMD ["./scripts/start-prod.sh"]