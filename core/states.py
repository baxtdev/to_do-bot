from aiogram.filters.state import State, StatesGroup
from aiogram.types import DateTime

class TaskStates(StatesGroup):
    waiting_for_task_name = State()
    waiting_for_start_date = State()
    waiting_for_end_date = State()
    
    