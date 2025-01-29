from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from mailings.config import get_db_url

DATABASE_URL = get_db_url()

# Создание асинхронного подключения к БД PostgreSQL, используя драйвер asyncpg.
engine = create_async_engine(DATABASE_URL)

# Создание фабрики асинхронных сессий, используя созданный движок.
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# Настройка аннотаций
int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
str_null_true = Annotated[str, mapped_column(nullable=True)]


class Base(AsyncAttrs, DeclarativeBase):
    """
    Базовый класс для всех моделей в БД
    """
    __abstract__ = True

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Переименование таблиц моделей в БД
        :return:
        """
        return f"{cls.__name__.lower()}s"
