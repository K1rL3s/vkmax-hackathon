from typing import Any

from dishka import FromDishka

from maxhack.bot.states import Groups
from maxhack.core.exceptions import MaxHackError
from maxhack.core.group.service import GroupService
from maxhack.core.ids import GroupId, InviteKey
from maxhack.core.invite.service import InviteService
from maxhack.infra.database.models import UserModel
from maxo.dialogs import DialogManager, ShowMode
from maxo.dialogs.integrations.dishka import inject


async def on_select_group(
    _: Any,
    __: Any,
    dialog_manager: DialogManager,
    group_id: GroupId,
) -> None:
    dialog_manager.dialog_data["group_id"] = group_id
    await dialog_manager.switch_to(state=Groups.one, show_mode=ShowMode.EDIT)


@inject
async def on_recreate_invite(
    _: Any,
    __: Any,
    dialog_manager: DialogManager,
    invite_service: FromDishka[InviteService],
) -> None:
    current_user: UserModel = dialog_manager.middleware_data["current_user"]
    group_id: GroupId = dialog_manager.dialog_data["group_id"]

    await invite_service.recreate_invite(group_id, current_user.id)


@inject
async def on_delete_invite(
    _: Any,
    __: Any,
    dialog_manager: DialogManager,
    invite_service: FromDishka[InviteService],
) -> None:
    current_user: UserModel = dialog_manager.middleware_data["current_user"]
    group_id: GroupId = dialog_manager.dialog_data["group_id"]

    await invite_service.delete_invite(group_id, current_user.id)


@inject
async def on_join_group(
    _: Any,
    __: Any,
    dialog_manager: DialogManager,
    group_service: FromDishka[GroupService],
) -> None:
    current_user: UserModel = dialog_manager.middleware_data["current_user"]
    invite_key: InviteKey = dialog_manager.dialog_data["invite_key"]

    try:
        await group_service.join_group(current_user.id, invite_key)
    except MaxHackError as e:
        # TODO: Сообщение что инвайт истёк
        raise e

    await dialog_manager.switch_to(state=Groups.one, show_mode=ShowMode.EDIT)
