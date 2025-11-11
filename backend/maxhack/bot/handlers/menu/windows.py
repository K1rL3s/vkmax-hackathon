from maxhack.bot.handlers.getters import get_current_user
from maxhack.bot.states import Menu, Profile
from maxhack.bot.widgets.to_groups import TO_GROUPS_BUTTON
from maxo.dialogs import Dialog, ShowMode, StartMode, Window
from maxo.dialogs.widgets.kbd import Start
from maxo.dialogs.widgets.text import Const, Format

_menu = Window(
    Format("👋 Привет, {first_name}!"),
    TO_GROUPS_BUTTON,
    Start(
        Const("🐵 Профиль"),
        state=Profile.my,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT,
        id="to_profile",
    ),
    getter=get_current_user,
    state=Menu.menu,
)

menu_dialog = Dialog(
    _menu,
)
