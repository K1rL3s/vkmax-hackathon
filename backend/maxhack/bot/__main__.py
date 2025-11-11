from maxhack.bot.init_bot import init_bot
from maxhack.logger import get_logger
from maxhack.utils.run import run
from maxo import Bot
from maxo.tools.long_polling import LongPolling

logger = get_logger(__name__, groups=("main", "bot", "maxbot"))


async def main() -> None:
    dp, container = await init_bot()

    bot = await container.get(Bot)
    try:
        await LongPolling(dp).start(bot)
    except Exception:
        logger.exception("Ошибка при поллинге, конец работы")
    finally:
        await container.close()


if __name__ == "__main__":
    run(main())
