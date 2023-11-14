from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from passwords_db import set_status, db_conect
from user_passwords_db import update_data, check_data
from Keybords.keybord_all_btns import create_keybord_watch_write_refactor
from Keybords.keybord_with_end import create_end
from Config import SET_STATUS_REFACTOR_DATA
from Filters.status_filter import StatusFilter

router = Router()


@router.callback_query(F.data == "refactor_data")
async def refactor(callback: CallbackQuery):
    await db_conect(user_id=callback.from_user.id)
    await set_status(user_id=callback.from_user.id, status=SET_STATUS_REFACTOR_DATA)
    await callback.message.delete()
    await callback.message.answer("*Отправьте данные в формате\n\nНАЗВАНИЕ\nНОВОЕ НАЗВАНИЕ\nНОВЫЙ ЛОГИН\nНОВЫЙ ПАРОЛЬ*",
                                  reply_markup=create_end(), parse_mode="Markdown")
    await callback.answer("Запрос выполнен!")

    @router.message(StatusFilter(status=SET_STATUS_REFACTOR_DATA))
    async def get_and_refactor(message: Message):
        try:
            if await check_data(user_id=message.from_user.id, site=message.text.split("\n")[0].replace(" ", "")):
                await update_data(user_id=message.from_user.id, site_old=message.text.split("\n")[0].replace(" ", ""),
                                  site=message.text.split("\n")[1].replace(" ", ""),
                                  login=message.text.split("\n")[2].replace(" ", ""),
                                  password=message.text.split("\n")[3].replace(" ", ""))
                await message.delete()
                await callback.message.answer("*Данные успешно обновлены!*",
                                              reply_markup=create_keybord_watch_write_refactor(), parse_mode="Markdown")
            else:
                await message.answer("*Таких данных не существует\nПопробуйте снова.*",
                                     reply_markup=create_keybord_watch_write_refactor(), parse_mode="Markdown")
        except Exception as e:
            await message.answer("Что-то пошло не так.\n/start - для перезагрузки.")
