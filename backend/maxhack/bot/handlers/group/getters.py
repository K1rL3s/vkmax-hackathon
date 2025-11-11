from typing import Any

from dishka import FromDishka

from maxhack.core.group.service import GroupService
from maxhack.core.ids import GroupId
from maxhack.core.user.service import UserService
from maxhack.infra.database.models import UserModel
from maxo.dialogs import DialogManager
from maxo.dialogs.integrations.dishka import inject


@inject
async def get_my_groups(
    current_user: UserModel,
    user_service: FromDishka[UserService],
    **__: Any,
) -> dict[str, Any]:
    return {
        "groups": await user_service.get_user_groups(current_user.id, current_user.id),
    }


@inject
async def get_one_group(
    dialog_manager: DialogManager,
    current_user: UserModel,
    group_service: FromDishka[GroupService],
    **__: Any,
) -> dict[str, Any]:
    group_id: GroupId = dialog_manager.dialog_data["group_id"]
    group, role = await group_service.get_group(current_user.id, group_id)
    return {"group": group, "role": role}
