from sqlalchemy.exc import SQLAlchemyError
from mailings.database import async_session_maker


class BaseDAO:
    """
    Базовый класс для работы с БД
    """
    model = None

    @classmethod
    async def add(cls, **kwargs):
        """
        Метод для сохранения объектов в БД
        """
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**kwargs)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance
