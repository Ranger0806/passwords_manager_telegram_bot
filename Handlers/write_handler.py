from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from passwords_db import set_status, db_conect
from user_passwords_db import set_new_info
from Keybords.keybord_all_btns import create_keybord_watch_write_refactor
from Keybords.keybord_with_end import create_end
from Config import SET_STATUS_LOAD, SET_STATUS_DEFAULT
from Filters.status_filter import StatusFilter

router = Router()


@router.callback_query(F.data == "write_password")
async def info(callback: CallbackQuery):
    await db_conect(user_id=callback.from_user.id)
    await callback.message.delete()
    await set_status(user_id=callback.from_user.id, status=SET_STATUS_LOAD)
    await callback.message.answer(
        "*Отправьте сообщение с 3 параметрами, каждый в отдельной строке:\n\nНАЗВАНИЕ\nЛОГИН\nПАРОЛЬ*",
        reply_markup=create_end(), parse_mode="Markdown")
    await callback.answer("Запрос выполнен!")

    @router.message(StatusFilter(status=SET_STATUS_LOAD))
    async def write_and_get(message: Message):
        try:
            await set_new_info(user_id=message.from_user.id, site=message.text.split("\n")[0].replace(" ", ""),
                               login=message.text.split("\n")[1].replace(" ", ""),
                               password=message.text.split("\n")[2].replace(" ", ""))
            await message.delete()
            await message.answer("*Данные успешно добавлены!*", reply_markup=create_keybord_watch_write_refactor(),
                                 parse_mode="Markdown")
            await set_status(user_id=message.from_user.id, status=SET_STATUS_DEFAULT)
        except Exception as e:
            await message.answer("Что-то пошло не так.\n/start - для перезагрузки.")
