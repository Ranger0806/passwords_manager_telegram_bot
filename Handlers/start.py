from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from passwords_db import db_conect, cheker_user, get_new_user, set_status, set_botPassword, get_botPassword
from Keybords.keybord_all_btns import create_keybord_watch_write_refactor
from Keybords.start_keybord import create_keybord
from Config import SET_STATUS_DEFAULT, SET_STATUS_SETUP_PASSWORD, SET_STATUS_SINGUP
from Filters.status_filter import StatusFilter

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await db_conect(user_id=message.from_user.id)
    if not await cheker_user(user_id=message.from_user.id):
        await get_new_user(user_id=message.from_user.id, name=message.from_user.first_name, status=SET_STATUS_DEFAULT,
                           botPassword=SET_STATUS_DEFAULT)
        await message.answer(
            f"*{message.from_user.first_name}, добрый день!\nЭтот бот может надежно хранить ваши пароли, не забывайте выходить из системы! Для начала придумайте пароль от вашего хранилища и введите его.*",
            parse_mode="Markdown")
        await set_status(user_id=message.from_user.id, status=SET_STATUS_SETUP_PASSWORD)

        @router.message(StatusFilter(status=SET_STATUS_SETUP_PASSWORD))
        async def set_bot_password(message: Message):
            await set_botPassword(user_id=message.from_user.id, botPassword=message.text.replace(" ", ""))
            await message.answer("*Пароль успешно сохранен.\nТеперь вы можете использовать бота!*",
                                 reply_markup=create_keybord(), parse_mode="Markdown")

    else:
        await set_status(status=SET_STATUS_SINGUP, user_id=message.from_user.id)
        await message.answer(
            f"*{message.from_user.first_name}, добрый день!\nВы уже зарегистрированы. Введите ваш пароль.*",
            parse_mode="Markdown")

@router.message(StatusFilter(status=SET_STATUS_SINGUP))
async def check_password(message: Message):
    await db_conect(user_id=message.from_user.id)
    if message.text.replace(" ", "") == await get_botPassword(user_id=message.from_user.id):
        await message.delete()
        await message.answer("*Вход выполнен успешно!\nНе забывайте выходить из системы!*",
                             reply_markup=create_keybord_watch_write_refactor(), parse_mode="Markdown")
    else:
        await message.delete()
        await message.answer("Неверный пароль!\nПопробуйте снова.")
