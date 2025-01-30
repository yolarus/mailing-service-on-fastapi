from fastapi import APIRouter

from celery_queue.tasks import celery_send_email, celery_send_telegram_message
from mailings.mailings.dao import MessageDAO, RecipientDAO
from mailings.mailings.schemas import SMailingAdd
from mailings.mailings.services import determine_email_or_tg_chat_id

router = APIRouter(prefix='/api/notify', tags=['Отправка рассылки'])


@router.post("/")
async def add_mailing(mailing: SMailingAdd):
    """
    Обработчик для сохранения объектов Message и Recipient в БД
    """
    await MessageDAO.add(message=mailing.message)

    if isinstance(mailing.recipient, str):
        email_list = determine_email_or_tg_chat_id([mailing.recipient]).get("email_list")
        tg_chat_id_list = determine_email_or_tg_chat_id([mailing.recipient]).get("tg_chat_id_list")
        await MessageDAO.add(message=mailing.recipient)
    else:
        email_list = determine_email_or_tg_chat_id(mailing.recipient).get("email_list")
        tg_chat_id_list = determine_email_or_tg_chat_id(mailing.recipient).get("tg_chat_id_list")

    for email in email_list:
        await RecipientDAO.add(email=email)

    celery_send_email.delay(mailing.message, email_list, mailing.delay)

    for tg_chat_id in tg_chat_id_list:
        await RecipientDAO.add(tg_chat_id=tg_chat_id)

    celery_send_telegram_message.delay(mailing.message, tg_chat_id_list, mailing.delay)
