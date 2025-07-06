from aiogram.dispatcher.filters.state import State, StatesGroup

class ProjectStates(StatesGroup):
    waiting_for_photo = State()
    waiting_for_status = State()
