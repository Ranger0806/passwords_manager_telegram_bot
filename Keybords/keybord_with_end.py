from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def create_end():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Выход из системы🔒", callback_data="off"))
    return builder.as_markup()