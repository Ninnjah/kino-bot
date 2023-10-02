from aiogram.fsm.state import State, StatesGroup


class AddAdminSG(StatesGroup):
    user_id = State()
    confirm = State()


class DelAdminSG(StatesGroup):
    user_id = State()
    confirm = State()
