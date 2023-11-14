from aiogram import Router, F
from aiogram.types import CallbackQuery
from user_passwords_db import get_data
from passwords_db import db_conect, set_status
from Config import SET_STATUS_WATCH
from Keybords.keybord_all_btns import create_keybord_watch_write_refactor

router = Router()


@router.callback_query(F.data == "read_passwords")
async def read(callback: CallbackQuery):
    await db_conect(user_id=callback.from_user.id)
    await callback.message.delete()
    await set_status(status=SET_STATUS_WATCH, user_id=callback.from_user.id)
    await callback.message.answer(await get_data(user_id=callback.from_user.id),
                                  reply_markup=create_keybord_watch_write_refactor(), parse_mode="Markdown")
    await callback.answer("Запрос выполнен!")
