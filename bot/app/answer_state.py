from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):
    name = State()
    city = State()
    preff_prod = State()
    preff_store = State()


class Request(StatesGroup):
    req = State()
  
