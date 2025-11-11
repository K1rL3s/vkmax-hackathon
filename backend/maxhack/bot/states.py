from maxo.fsm.state import State, StatesGroup


class Errors(StatesGroup):
    error_intent = State()
    unexcepted_error = State()


class Menu(StatesGroup):
    menu = State()


class Profile(StatesGroup):
    my = State()


class Groups(StatesGroup):
    all = State()
    one = State()
    join = State()
    create = State()
    delete = State()


class GroupsCreate(StatesGroup):
    wait_name = State()
    wait_description = State()
    wait_timezone = State()
    confirm = State()
