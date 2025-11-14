from typing import Any

from maxo.dialogs import DialogManager
from maxo.dialogs.integrations.dishka import inject

from maxhack.core.utils.datehelp import datetime_now
from maxhack.core.utils.timezones import TIMEZONES
from maxhack.database.models import UserModel


@inject
async def get_current_user(dialog_manager: DialogManager, **__: Any) -> dict[str, Any]:
    user: UserModel = dialog_manager.middleware_data["current_user"]
    user_time = datetime_now(tz_offset=user.timezone // 60)
    return {
        "current_user": user,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": user.phone,
        "formatted_timezone": TIMEZONES.get(user.timezone, user.timezone),
        "user_time": user_time,
        "user_greeting": _get_greeting_by_hour(user_time.hour),
    }


def _get_greeting_by_hour(hour: int) -> str:
    if 5 <= hour <= 11:
        return "☀️ Доброе утро"
    if 12 <= hour < 16:
        return "🌤️ Добрый день"
    if 17 <= hour <= 22:
        return "🌅 Добрый вечер"
    return "🌙 Доброй ночи"
