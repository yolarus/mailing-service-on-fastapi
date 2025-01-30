FROM python:3.11

WORKDIR .

RUN pip install fastapi uvicorn redis sqlalchemy alembic asyncpg pydantic pydantic-settings greenlet celery psycopg2

COPY . .

EXPOSE 8000
