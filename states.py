from aiogram.fsm.state import State, StatesGroup

class ApplicationForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_region = State()
    waiting_for_subject = State()
    waiting_for_source = State()
