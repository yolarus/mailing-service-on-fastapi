from sqlalchemy import select

from mailings.dao.base import BaseDAO
from mailings.database import async_session_maker
from mailings.mailings.models import Message, Recipient


class MessageDAO(BaseDAO):
    """
    Класс для работы с БД для модели Message
    """
    model = Message


class RecipientDAO(BaseDAO):
    """
    Класс для работы с БД для модели Recipient
    """
    model = Recipient

    @classmethod
    async def add(cls, **kwargs):
        """
        Дополнительная проверка не существует ли получатель уже в базе данных
        """
        async with async_session_maker() as session:
            async with session.begin():
                query = select(cls.model).filter_by(email=kwargs.get("email"), tg_chat_id=kwargs.get("tg_chat_id"))
                result = await session.execute(query)
        if result.scalar_one_or_none() is None:
            await super().add(**kwargs)
        return None
