from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def create_keybord_watch_write_refactor():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Записать пароль🖊", callback_data="write_password"))
    builder.row(types.InlineKeyboardButton(text="Показать пароли🗒", callback_data="read_passwords"))
    builder.row(types.InlineKeyboardButton(text="Изменить данные📝", callback_data="refactor_data"))
    builder.row(types.InlineKeyboardButton(text="Удалить данные❌", callback_data="delete_data"))
    builder.row(types.InlineKeyboardButton(text="Сменить пароль🔏", callback_data="reset_password"))
    builder.row(types.InlineKeyboardButton(text="Выход из системы🔒", callback_data="off"))
    return builder.as_markup()
