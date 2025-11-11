import asyncio
import contextlib
import sys
from collections.abc import Awaitable
from typing import Any


def run(entrypoint: Awaitable[Any]) -> None:
    if sys.platform == "win32":
        # раб винды :(
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    if __debug__:
        runner = asyncio.run
    else:
        try:
            import uvloop

            runner = uvloop.run
        except ImportError:
            runner = asyncio.run

    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        runner(entrypoint)
