import re
from email.utils import parseaddr

email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


def determine_email_or_tg_chat_id(instances: list[str]) -> dict[str, list[str]]:
    """
    Формирует списки email'ов и tg_chat_id из переданного списка адресатов
    """
    tg_chat_id_list = []
    email_list = []

    for instance in instances:
        if instance.isdigit():
            tg_chat_id_list.append(instance)
        else:
            email_list.append(instance)
    return {"tg_chat_id_list": tg_chat_id_list,
            "email_list": email_list}


def validate_email_or_tg_chat_id(instance: str) -> None:
    """
    Формирует списки email'ов и tg_chat_id из переданного списка адресатов
    """
    match = email_pattern.fullmatch(instance)
    parsed_email = parseaddr(instance)[1]
    if not any([(match and parsed_email == instance), instance.isdigit()]):
        raise ValueError(f"Введен некорректный получатель - {instance}")
    if len(instance) > 150:
        raise ValueError(f"Адрес получателя больше 150 символов - {instance}")
