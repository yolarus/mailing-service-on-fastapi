from os import getenv

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

load_dotenv(".env")

conf = ConnectionConfig(
    MAIL_USERNAME=getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=getenv("MAIL_PASSWORD"),
    MAIL_PORT=getenv("MAIL_PORT"),
    MAIL_SERVER=getenv("MAIL_SERVER"),
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    MAIL_FROM=getenv("MAIL_FROM"))

fast_mail = FastMail(conf)


def send_email(message: str, emails: list[str]):
    try:
        mail = MessageSchema(
            subject="Рассылка сообщений",
            message=message,
            recipients=emails,
            subtype="html")
        fast_mail.send_message(mail)
        return {"status_code": 200, "message": "Рассылка успешно отправлена"}
    except Exception as e:
        return {"status_code": 500, "message": f"Рассылка провалилась - {e}"}
