import secrets
from datetime import datetime
from typing import Optional

from maxhack.core.ids import InviteKey


def to_camel(string: str) -> str:
    """
    Верблюдезирует строку, со строчным написанием первого слова

    to_camel_case -> toCamelCase

    :param string: строка в snake case'е
    :type string: str
    :return: строка в camel case'е
    :rtype: str
    """
    return "".join(
        word if i == 0 else word.capitalize()
        for i, word in enumerate(string.split("_"))
    )


def generate_invite_key() -> InviteKey:
    return InviteKey(secrets.token_urlsafe(16)[:16])


def create_cron_expression(
        event_date: Optional[datetime],
        every_day: bool,
        every_week: bool,
        every_month: bool,
) -> str:
    """
    Создает cron выражение на основе параметров повторения.

    Args:
        event_date: Дата и время события (используется для извлечения минут и часов)
        every_day: Ежедневное повторение
        every_week: Еженедельное повторение
        every_month: Ежемесячное повторение

    Returns:
        str: cron выражение в формате "минуты часы день_месяца месяц день_недели"

    Raises:
        ValueError: Если не указан event_date или конфликтующие параметры
    """
    if event_date is None:
        raise ValueError("event_date обязателен для создания cron выражения")

    minute = event_date.minute
    hour = event_date.hour

    day_of_month = event_date.day
    day_of_week = event_date.weekday()

    if every_day:
        return f"{minute} {hour} * * *"

    elif every_week:
        return f"{minute} {hour} * * {day_of_week}"

    elif every_month:
        return f"{minute} {hour} {day_of_month} * *"

    else:
        month = event_date.month
        return f"{minute} {hour} {day_of_month} {month} *"