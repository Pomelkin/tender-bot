from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.row(KeyboardButton(text="Мои документы"))
    keyboard.adjust()
    return keyboard.as_markup(resize_keyboard=True)
