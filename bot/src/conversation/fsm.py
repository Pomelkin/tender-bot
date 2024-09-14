from aiogram.fsm.state import State, StatesGroup


class Document(StatesGroup):
    id = State()
    conversation = State()
    create_agreement = State()
    doc_type = State()
