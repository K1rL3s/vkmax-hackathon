from typing import Any

from maxo.dialogs import DialogManager
from maxo.routing.updates.message_created import MessageCreated
from maxo.tools.facades.updates.message_created import MessageCreatedFacade


async def answer_str_error(
    _: MessageCreated,
    __: Any,
    dialog_manager: DialogManager,
    error: ValueError,
) -> None:
    facade: MessageCreatedFacade = dialog_manager.middleware_data["facade"]
    await facade.answer_text(text=str(error))
