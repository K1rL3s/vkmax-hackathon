from typing import Any

from maxhack.bot.states import Groups
from maxhack.core.ids import GroupId
from maxo.dialogs import DialogManager, ShowMode


async def on_select_group(
    _: Any,
    __: Any,
    dialog_manager: DialogManager,
    group_id: GroupId,
) -> None:
    dialog_manager.dialog_data["group_id"] = group_id
    await dialog_manager.switch_to(state=Groups.one, show_mode=ShowMode.EDIT)
