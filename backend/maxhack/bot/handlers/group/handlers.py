from typing import Any

from dishka import FromDishka

from maxo.dialogs import DialogManager, ShowMode
from maxo.dialogs.integrations.dishka import inject

from maxhack.bot.states import Groups, Menu
from maxhack.core.exceptions import MaxHackError
from maxhack.core.group.service import GroupService
from maxhack.core.ids import GroupId, InviteKey
from maxhack.database.models import UserModel


async def on_select_group(
    _: Any,
    __: Any,
    dialog_manager: DialogManager,
    group_id: GroupId,
) -> None:
    dialog_manager.dialog_data["group_id"] = group_id
    await dialog_manager.switch_to(state=Groups.one, show_mode=ShowMode.EDIT)


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

    # TODO: Сообщение с стартапп в группу
    await dialog_manager.switch_to(state=Menu.menu, show_mode=ShowMode.EDIT)


@inject
async def on_get_all_group_events(
    _: Any,
    __: Any,
    dialog_manager: DialogManager,
) -> None:
    current_user: UserModel = dialog_manager.middleware_data["current_user"]
    group_id: GroupId = dialog_manager.dialog_data["group_id"]

    # TODO: Выброс календаря

    dialog_manager.show_mode = ShowMode.SEND


@inject
async def on_get_my_group_events(
    _: Any,
    __: Any,
    dialog_manager: DialogManager,
) -> None:
    current_user: UserModel = dialog_manager.middleware_data["current_user"]
    group_id: GroupId = dialog_manager.dialog_data["group_id"]

    # TODO: Выброс календаря

    dialog_manager.show_mode = ShowMode.SEND
