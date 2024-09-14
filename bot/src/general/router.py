from aiogram import Router
from aiogram.filters import CommandStart
from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.src.general.keyboards import get_main_keyboard
from conversation.fsm import Document

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: types.Message, state: FSMContext) -> None:
    await message.answer("Привет, введи номер документа:")
    await state.set_state(Document.id)
