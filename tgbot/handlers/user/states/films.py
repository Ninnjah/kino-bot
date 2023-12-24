from aiogram.fsm.state import State, StatesGroup


class FilmSG(StatesGroup):
    lst = State()
    film = State()
