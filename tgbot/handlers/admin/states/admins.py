from aiogram.fsm.state import State, StatesGroup


class AdminSG(StatesGroup):
    lst = State()
    profile = State()


class AddAdminSG(StatesGroup):
    user_id = State()
    sudo = State()
    confirm = State()


class DelAdminSG(StatesGroup):
    confirm = State()