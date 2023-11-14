from aiogram import Router, F
from aiogram.types import CallbackQuery
from passwords_db import db_conect, set_status
from Config import SET_STATUS_SINGUP

router = Router()


@router.callback_query(F.data == "off")
async def off(callback: CallbackQuery):
    await db_conect(user_id=callback.from_user.id)
    await set_status(status=SET_STATUS_SINGUP, user_id=callback.from_user.id)
    await callback.message.delete()
    await callback.message.answer("*Вы вышли из системы.\nВведите пароль.*", parse_mode="Markdown")
    await callback.answer("Запрос выполнен!")
