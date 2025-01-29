from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from mailings.database import Base, int_pk, str_null_true


class MessageRecipient(Base):
    """
    Модель для хранения связей Message и Recipient
    """
    __tablename__ = 'messagerecipient'
    id: Mapped[int_pk]
    message_id: Mapped[int] = mapped_column(ForeignKey("messages.id"), nullable=False)
    recipient_id: Mapped[int] = mapped_column(ForeignKey("recipients.id"), nullable=False)


class Message(Base):
    """
    Модель сообщения, сохраняющаяся в таблицу БД
    """
    id: Mapped[int_pk]
    message: Mapped[str] = mapped_column(Text)

    # Одно сообщение - много получателей
    recipients: Mapped[list["Recipient"]] = relationship("Recipient",
                                                         secondary="messagerecipient",
                                                         back_populates="messages")

    def __str__(self):
        """
        Отображение объекта пользователю
        """
        return self.message

    def __repr__(self):
        """
        Отображение объекта в режиме отладки
        """
        return str(self)

    def to_dict(self):
        """
        Преобразование в словарь
        """
        return {
            "id": self.id,
            "message": self.message,
            "recipients": self.recipients
        }


class Recipient(Base):
    """
    Модель получателя, сохраняющаяся в таблицу БД
    """
    id: Mapped[int_pk]
    email: Mapped[str_null_true]
    tg_chat_id: Mapped[str_null_true]

    # Один получатель - много сообщений
    messages: Mapped[list["Message"]] = relationship("Message",
                                                     secondary="messagerecipient",
                                                     back_populates="recipients")

    def __str__(self):
        """
        Отображение объекта пользователю
        """
        if self.tg_chat_id:
            return self.tg_chat_id
        return self.email

    def __repr__(self):
        """
        Отображение объекта в режиме отладки
        """
        return str(self)

    def to_dict(self):
        """
        Преобразование в словарь
        """
        return {
            "id": self.id,
            "email": self.email,
            "recipients": self.tg_chat_id
        }
