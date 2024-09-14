from aiogram import Router
from aiogram.filters import CommandStart
from aiogram import types
from aiogram.fsm.context import FSMContext

from routers.conversation.fsm import Document

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(None)
    await message.answer("Привет, введи номер документа:")
    await state.set_state(Document.id)
