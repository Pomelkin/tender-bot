from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

from conversation.callback_data import DocTypeData


def get_main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.row(KeyboardButton(text="Сгенерировать соглашение"))
    keyboard.adjust()
    return keyboard.as_markup(resize_keyboard=True)


def get_choose_doc_type_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="PDF", callback_data=DocTypeData(type="pdf").pack())
    keyboard.button(text="DOCX", callback_data=DocTypeData(type="docx").pack())
    keyboard.adjust(1)
    return keyboard.as_markup()