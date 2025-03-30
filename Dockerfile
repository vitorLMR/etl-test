# python-base sets up all our shared environment variables
FROM python:3.7-slim as python-base 
# https://python-poetry.org/docs/configuration/#using-environment-variables
# make poetry create the virtual environment in the project's root
# it gets named `.venv`
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_PATH=/opt/poetry \
    VENV_PATH=/opt/venv \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 
# poetry and venv to path
ENV PATH="$POETRY_PATH/bin:$VENV_PATH/bin:$PATH"
WORKDIR /app

# builder-base stage is used to build deps + create the virtual environment
FROM python-base as poetry
RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    build-essential \
|| { echo "apt-get install failed"; exit 1; }

RUN curl -sSL https://install.python-poetry.org | python - || { echo "Poetry installation failed"; exit 1; }

RUN mv /root/.poetry $POETRY_PATH || { echo "Moving Poetry failed"; exit 1; }

RUN rm -rf /var/lib/apt/lists/* || { echo "Cleanup failed"; exit 1; }

ENV PATH="$POETRY_PATH/bin:$PATH"
RUN poetry --version
# pyproject.toml will be copied among other files
COPY . ./
# poetry will build the lock file from scratch if it's missing
RUN rm poetry.lock
# install [tool.poetry.dependencies]
# this will install virtual environment into /.venv because of POETRY_VIRTUALENVS_IN_PROJECT=true
# see: https://python-poetry.org/docs/configuration/#virtualenvsin-project
RUN poetry install --no-interaction --no-root
ENV PATH="/app/.venv/bin:$PATH"

# production stage used for runtime
FROM python-base as runtime
COPY --from=poetry /app /app
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8090
USER root
RUN chmod +x entrypoints/pytest_entrypoint.sh
FROM public.ecr.aws/docker/library/python:3.11.4-slim-bullseye

# setup environment variable
ENV SERVICE_HOME=/usr/src/application \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    MODE=PROD

RUN apt-get update -y &&  \
    apt-get upgrade -y &&  \
    apt-get -y install netcat && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir $SERVICE_HOME

# where your code lives
WORKDIR $SERVICE_HOME

# copy whole project to your docker home directory.
COPY . .

# Install poetry:
RUN pip3 install poetry && \
    poetry config virtualenvs.create false

# run this command to install all dependencies
RUN poetry lock --no-update && \
    poetry install --without dev

EXPOSE 8000