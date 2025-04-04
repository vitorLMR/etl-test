FROM python:3.12.3-slim

# setup environment variable
ENV SERVICE_HOME=/usr/src/application \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYDEVD_DISABLE_FILE_VALIDATION=1 \
    -Xfrozen_modules=off \
    MODE=DEV


RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get -y install make && \
    apt-get -y install telnet && \
    apt-get -y install procps && \
    apt-get -y install python3-dev && \
    apt-get -y install libpq-dev gcc &&  \
    pip3 install psycopg2 && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir $SERVICE_HOME

RUN mkdir -p /usr/share/man/man1 /usr/share/man/man2 && \
    apt-get update &&\
    apt-get install -y python3-launchpadlib && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:openjdk-r/ppa && \
    apt-get update && \
    apt-get install -y default-jre && \
    apt-get install ca-certificates-java -y && \
    apt-get clean && \
    update-ca-certificates -f;
# where your code lives
WORKDIR $SERVICE_HOME

# copy whole project to your docker home directory.
COPY . .

RUN echo "Listando arquivos em /app:" && ls -alh

# Install poetry: Version 1.4.1 of the incompatibility with debufy
RUN pip3 install poetry && \
    poetry config virtualenvs.create false

# run this command to install all dependencies
RUN poetry lock 
RUN poetry install

EXPOSE 8000

