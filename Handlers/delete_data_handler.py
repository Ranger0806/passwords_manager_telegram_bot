from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from passwords_db import set_status, db_conect
from user_passwords_db import delete_data, check_data
from Keybords.keybord_all_btns import create_keybord_watch_write_refactor
from Keybords.keybord_with_end import create_end
from Config import SET_STATUS_DELETE
from Filters.status_filter import StatusFilter


router = Router()


@router.callback_query(F.data == "delete_data")
async def delete(callback: CallbackQuery):
    await db_conect(user_id=callback.from_user.id)
    await set_status(user_id=callback.from_user.id, status=SET_STATUS_DELETE)
    await callback.message.delete()
    await callback.message.answer("*Отправьте НАЗВАНИЕ чтобы удалить.*",reply_markup=create_end(), parse_mode="Markdown")
    await callback.answer("Запрос выполнен!")

    @router.message(StatusFilter(status=SET_STATUS_DELETE))
    async def get_and_delete(message: Message):
        try:
            if await check_data(user_id=message.from_user.id, site=message.text.replace(" ", "")):
                await delete_data(user_id=message.from_user.id, site=message.text.replace(" ", ""))
                await message.delete()
                await callback.message.answer("*Данные успешно удалены!*",
                                              reply_markup=create_keybord_watch_write_refactor(), parse_mode="Markdown")
            else:
                await message.answer("*Таких данных не существует\nПопробуйте снова.*", reply_markup=create_keybord_watch_write_refactor(), parse_mode="Markdown")
        except Exception as e:
            await message.answer("Что-то пошло не так.\n/start - для перезагрузки.")
