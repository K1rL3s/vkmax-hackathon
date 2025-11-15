import secrets
from datetime import datetime

from maxhack.core.ids import InviteKey
from maxhack.core.utils.datehelp import UTC_TIMEZONE


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
    return InviteKey(secrets.token_urlsafe(8)[:8])


def create_cron_expression(
    event_date: datetime,
    every_day: bool,
    every_week: bool,
    every_month: bool,
) -> str:
    event_date = event_date.astimezone(UTC_TIMEZONE)
    minute = event_date.minute
    hour = event_date.hour

    day_of_month = event_date.day
    day_of_week = event_date.weekday()

    if every_day:
        return f"{minute} {hour} * * *"

    if every_week:
        return f"{minute} {hour} * * {day_of_week}"

    if every_month:
        return f"{minute} {hour} {day_of_month} * *"

    month = event_date.month
    return f"{minute} {hour} {day_of_month} {month} *"
