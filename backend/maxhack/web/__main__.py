import asyncio
import sys

import granian
from granian.constants import Interfaces

from maxhack.config import load_config

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    config = load_config()
    granian.Granian(
        "maxhack.web.asgi:app",
        address=config.app.host,
        port=config.app.port,
        interface=Interfaces.ASGI,
        reload=False,
        log_access=True,
        workers=1,
    ).serve()
