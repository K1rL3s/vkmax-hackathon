from dishka.integrations.taskiq import setup_dishka
from taskiq import AsyncBroker, TaskiqScheduler
from taskiq.cli.common_args import LogLevel
from taskiq.cli.scheduler.args import SchedulerArgs
from taskiq.cli.scheduler.run import run_scheduler

from maxhack.bot.init_bot import init_bot
from maxhack.logger import get_logger
from maxhack.scheduler.tasks import *  # noqa
from maxhack.utils.run import run

logger = get_logger(__name__, groups=("main", "taskiq"))


async def main() -> None:
    dp, container = await init_bot()

    broker = await container.get(AsyncBroker)
    scheduler = await container.get(TaskiqScheduler)
    scheduler_args = SchedulerArgs(
        scheduler=scheduler,
        log_level=LogLevel.DEBUG,  # type: ignore
        modules=["maxhack.scheduler.tasks"],
        update_interval=5,
        configure_logging=False,
    )

    setup_dishka(container, broker)

    logger.warning("Старт шедулера")
    try:
        await run_scheduler(scheduler_args)
    except Exception:
        logger.exception("Ошибка при работе планировщика, конец работы")
    finally:
        await scheduler.shutdown()
        for source in scheduler.sources:
            await source.shutdown()
        await container.close()


if __name__ == "__main__":
    run(main())
