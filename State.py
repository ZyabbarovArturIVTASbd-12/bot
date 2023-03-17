
from aiogram.dispatcher.filters.state import State, StatesGroup

class StateGroupExample(StatesGroup):
    wait_for_answer = State() #создаёте состояние