from pydantic import BaseModel, Field, field_validator

from mailings.mailings.services import validate_email_or_tg_chat_id


class SMailingAdd(BaseModel):
    """
    Модель отправки данных на сервер при создании рассылки
    """
    message: str = Field(..., max_length=1024, description="Сообщение")
    recipient: str | list[str] = Field(..., description="Получатели рассылки")
    delay: int = Field(..., ge=0, le=2, description="Параметр задержки")

    @field_validator("recipient")
    @classmethod
    def validate_recipient(cls, values: str | list[str]) -> str | list[str]:
        """
        Проверка длины адреса получателя
        """
        if isinstance(values, str):
            validate_email_or_tg_chat_id(values)
        else:
            for value in values:
                validate_email_or_tg_chat_id(value)
        return values
