import asyncio
import datetime
from typing import ParamSpec, TypeVar

from taskiq import AsyncBroker, AsyncTaskiqDecoratedTask
from taskiq.abc.schedule_source import ScheduleSource

from maxhack.core.ids import SchedulerTaskId
from maxhack.core.utils.datehelp import datetime_now
from maxhack.logger import get_logger

logger = get_logger(__name__, groups="scheduler")


_FuncParams = ParamSpec("_FuncParams")
_ReturnType = TypeVar("_ReturnType")


class BaseSchedulerClient:
    def __init__(self, broker: AsyncBroker, schedule_source: ScheduleSource) -> None:
        self._broker = broker
        self._schedule_source = schedule_source

    async def schedule_by_time(
        self,
        task: AsyncTaskiqDecoratedTask[_FuncParams, _ReturnType],
        timedelta: datetime.timedelta | None = None,
        on_datetime: datetime.datetime | None = None,
        *args: _FuncParams.args,
        **kwargs: _FuncParams.kwargs,
    ) -> SchedulerTaskId:
        if timedelta is not None:
            on_datetime = datetime_now() + timedelta
        if on_datetime is None:
            raise ValueError("`timedelta` or `on_datetime` must be specified`")

        scheduled = await task.schedule_by_time(
            self._schedule_source,
            on_datetime,
            *args,
            **kwargs,
        )

        logger.info(
            'Added task "%s" (args=%s, kwargs=%s) on %s with id=%s',
            task.task_name,
            args,
            kwargs,
            on_datetime,
            scheduled.schedule_id,
        )

        return SchedulerTaskId(scheduled.schedule_id)

    async def unschedule(self, scheduler_task_id: SchedulerTaskId) -> None:
        await self._schedule_source.delete_schedule(scheduler_task_id)

    async def bulk_unschedule(
        self,
        *scheduler_task_ids: SchedulerTaskId | None,
    ) -> None:
        await asyncio.gather(
            *(
                self.unschedule(task_id)
                for task_id in scheduler_task_ids
                if task_id is not None
            ),
        )
