from dishka import FromDishka
from dishka.integrations.taskiq import inject
from taskiq import async_shared_broker

from maxhack.core.max import MaxSender
from maxhack.core.utils.datehelp import datetime_now
from maxhack.logger import get_logger

logger = get_logger(__name__, groups="tasks")


@async_shared_broker.task(
    task_name="send_notifies",
    schedule=[{"cron": "* * * * *"}],
)
@inject(patch_module=True)
async def send_notifies(
    *,
    max_sender: FromDishka[MaxSender],
) -> None:
    now = datetime_now()
    # TODO: Логика проверки уведов
