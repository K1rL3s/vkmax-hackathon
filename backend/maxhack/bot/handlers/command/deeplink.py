from typing import Any

from dishka import FromDishka
from magic_filter import F

from maxhack.bot.states import Groups
from maxhack.core.exceptions import MaxHackError
from maxhack.core.ids import InviteKey
from maxhack.core.invite.service import InviteService
from maxhack.core.max.deeplinker import InvitePrefix
from maxo import Router
from maxo.dialogs import DialogManager, ShowMode, StartMode
from maxo.integrations.magic_filter import MagicData
from maxo.routing.filters.deeplink import DeeplinkFilter
from maxo.routing.filters.logic import AndFilter
from maxo.routing.sentinels import UNHANDLED, SkipHandler

deeplinks_router = Router(name=__name__)


@deeplinks_router.bot_started(
    AndFilter(
        DeeplinkFilter(),
        MagicData(F.deeplink.startswith(InvitePrefix)),
    ),
)
async def invite_deeplink_handler(
    _: Any,
    deeplink: str,
    dialog_manager: DialogManager,
    invite_service: FromDishka[InviteService],
) -> UNHANDLED:
    raw_invite_key = deeplink[len(InvitePrefix) :]
    try:
        invite_key = InviteKey(str(raw_invite_key))
    except ValueError as e:
        # TODO: Ответ, что такого инвайта нет
        raise SkipHandler from e

    dialog_manager.show_mode = ShowMode.SEND

    try:
        invite, group = await invite_service.is_valid_key(invite_key)
    except MaxHackError as e:
        # TODO: Ответ, что такого инвайта нет
        raise SkipHandler from e

    # TODO: Если юзер уже в этой группе - отправка сразу в группу

    await dialog_manager.start(
        state=Groups.join,
        show_mode=ShowMode.SEND,
        mode=StartMode.RESET_STACK,
        data={"invite_key": invite.key, "group_id": group.id},
    )
