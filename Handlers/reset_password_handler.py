from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from passwords_db import set_status, db_conect, reset_password, get_botPassword
from Keybords.keybord_all_btns import create_keybord_watch_write_refactor
from Keybords.keybord_with_end import create_end
from Config import SET_STATUS_RESET_PASSWORD
from Filters.status_filter import StatusFilter

router = Router()


@router.callback_query(F.data == "reset_password")
async def reset(callback: CallbackQuery):
    await db_conect(user_id=callback.from_user.id)
    await set_status(user_id=callback.from_user.id, status=SET_STATUS_RESET_PASSWORD)
    await callback.message.delete()
    await callback.message.answer("*Отправьте старый пароль и новый пароль.\n\nСТАРЫЙ ПАРОЛЬ\nНОВЫЙ ПАРОЛЬ*",
                                  reply_markup=create_end(),
                                  parse_mode="Markdown")
    await callback.answer("Запрос выполнен!")

    @router.message(StatusFilter(status=SET_STATUS_RESET_PASSWORD))
    async def get_reset(message: Message):
        try:
            if await get_botPassword(user_id=message.from_user.id) == message.text.split("\n")[0].replace(" ", ""):
                await reset_password(user_id=message.from_user.id,
                                     new_password=message.text.split("\n")[1].replace(" ", ""))
                await message.delete()
                await callback.message.answer("*Пароль успешно обновлен!*",
                                              reply_markup=create_keybord_watch_write_refactor(), parse_mode="Markdown")
            else:
                await message.answer("*Таких данных не существует\nПопробуйте снова.*",
                                     reply_markup=create_keybord_watch_write_refactor(), parse_mode="Markdown")
        except Exception as e:
            await message.answer("Что-то пошло не так.\n/start - для перезагрузки.")
