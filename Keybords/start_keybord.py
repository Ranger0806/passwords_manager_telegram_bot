from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def create_keybord():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Записать пароль🖊", callback_data="write_password"))
    builder.row(types.InlineKeyboardButton(text="Выход из системы🔒", callback_data="off"))
    return builder.as_markup()