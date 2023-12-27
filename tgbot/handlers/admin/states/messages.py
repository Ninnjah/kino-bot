from aiogram.fsm.state import State, StatesGroup


class MessageSG(StatesGroup):
    main = State()
    media = State()
    text = State()
    preview = State()
