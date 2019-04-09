# Chuzz Backend

A mobile app for creating and answering polls.

## Built With

* [Docker](https://www.docker.com)
* [Docker Compose](https://docs.docker.com/compose)
* [Python](https://www.python.org)
* [Alembic](http://alembic.zzzcomputing.com/en/latest)
* [Psycopg 2](http://initd.org/psycopg/docs)

## Getting Started

To setup development environment:

```bash
docker-compose build
docker-compose up
```

## Database Migration

Update value `sqlalchemy.url` in `alembic.ini`.

```bash
export SCHEMA_NAME=app_chuzz
alembic upgrade head

```

## Create New Migration Script

```bash
alembic revision -m "add is #{field} to #{table}"
alembic upgrade head

```

## Server Deployment

Skygear Cloud deployment uses a commandline tool [skycli](https://github.com/SkygearIO/skycli).

The file `skygear.json` configures the name of the App in [Skygear Cloud](https://portal.skygear.io/).

```bash
npm install -g skycli
skycli login #Input email and password of your Skygear Cloud Account
skycli deploy

```
