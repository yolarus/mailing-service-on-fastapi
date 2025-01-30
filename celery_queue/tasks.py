from os import getenv
from time import sleep

import requests

from celery_queue.celery import celery_app
from celery_queue.email import send_email

TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_URl = "https://api.telegram.org/bot"


@celery_app.task(name="celery_send_email")
def celery_send_email(message: str, emails: list[str], delay: int) -> dict:
    """
    Отправка email'а пользователю
    """
    if delay == 1:
        sleep(1 * 60 * 60)
    elif delay == 2:
        sleep(24 * 60 * 60)
    result = send_email(message, emails)
    print(result)
    return result


@celery_app.task(name="celery_send_telegram_message")
def celery_send_telegram_message(message: str, tg_chat_id: str, delay: int):
    """
    Отправка сообщения пользователю в чат-боте ТГ
    """
    if delay == 1:
        sleep(1 * 60 * 60)
    elif delay == 2:
        sleep(24 * 60 * 60)
    params = {
        'text': message,
        'chat_id': tg_chat_id}
    response = requests.get(f'{TELEGRAM_URl}{TELEGRAM_BOT_TOKEN}/sendMessage', params=params)
    print(response)
