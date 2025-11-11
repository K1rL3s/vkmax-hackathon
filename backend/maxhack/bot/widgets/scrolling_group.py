from maxo.dialogs import DialogManager
from maxo.dialogs.api.internal import RawKeyboard
from maxo.dialogs.widgets.common import OnPageChangedVariants, WhenCondition
from maxo.dialogs.widgets.kbd import Keyboard, ScrollingGroup
from maxo.types.callback_keyboard_button import CallbackKeyboardButton

SCROLL_ID = "__scroll__"


class CustomScrollingGroup(ScrollingGroup):
    """
    Заменённый текст в кнопках пейджера
    Пейджер скрывается на одной странице по дефолту
    """

    def __init__(
        self,
        *buttons: Keyboard,
        id: str = SCROLL_ID,
        width: int = 1,
        height: int = 10,
        when: WhenCondition = None,
        on_page_changed: OnPageChangedVariants = None,
        hide_on_single_page: bool = True,
        hide_pager: bool = False,
    ) -> None:
        super().__init__(
            *buttons,
            id=id,
            width=width,
            height=height,
            when=when,
            on_page_changed=on_page_changed,
            hide_on_single_page=hide_on_single_page,
            hide_pager=hide_pager,
        )

    async def _render_pager(
        self,
        pages: int,
        manager: DialogManager,
    ) -> RawKeyboard:
        if self.hide_pager:
            return []
        if pages == 0 or (pages == 1 and self.hide_on_single_page):
            return []

        last_page = pages - 1
        current_page = min(last_page, await self.get_page(manager))
        next_page = min(last_page, current_page + 1)
        prev_page = max(0, current_page - 1)

        return [
            [
                CallbackKeyboardButton(
                    text="⏪",
                    payload=self._item_payload("0"),
                ),
                CallbackKeyboardButton(
                    text="⬅️",
                    payload=self._item_payload(prev_page),
                ),
                CallbackKeyboardButton(
                    text=str(current_page + 1),
                    payload=self._item_payload(current_page),
                ),
                CallbackKeyboardButton(
                    text="➡️",
                    payload=self._item_payload(next_page),
                ),
                CallbackKeyboardButton(
                    text="⏩",
                    payload=self._item_payload(last_page),
                ),
            ],
        ]
