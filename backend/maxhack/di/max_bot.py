from collections.abc import AsyncIterable

from dishka import Provider, Scope, from_context, provide

from maxo import Bot
from maxo.dialogs import BgManagerFactory
from maxo.enums.text_fromat import TextFormat

from maxhack.config import MaxConfig
from maxhack.core.max import MaxMailer, MaxSender
from maxhack.core.max.notifier import MaxNotifier


class MaxBotProvider(Provider):
    scope = Scope.APP

    bg_factory = from_context(BgManagerFactory)

    @provide
    async def max_bot(self, max_config: MaxConfig) -> AsyncIterable[Bot]:
        bot = Bot(token=max_config.token, text_format=TextFormat.HTML)
        async with bot:
            yield bot

    max_sender = provide(MaxSender)
    max_mailer = provide(MaxMailer)
    max_notifier = provide(MaxNotifier)
