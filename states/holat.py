from aiogram.dispatcher.filters.state import StatesGroup, State

class Kafe(StatesGroup):
    cats = State()
    sub_cat = State()
    product = State()
    amount = State()
    cats = State()
    savat = State()
    phone = State()
    location = State()