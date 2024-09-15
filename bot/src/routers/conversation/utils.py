import os
from contextlib import asynccontextmanager

from aiogram import Bot
from pyhtml2pdf import converter


def create_pdf(url: str):
    converter.convert(url, 'sample.pdf')


@asynccontextmanager
async def typing_message(chat_id: int, bot: Bot):
    message = await bot.send_message(chat_id, "Обработка...")
    yield
    await message.delete()
