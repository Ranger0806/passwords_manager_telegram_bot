from aiogram import Bot, Dispatcher
import asyncio
import logging
from Config import BOT_TOKEN
from passwords_db import close
from user_passwords_db import close_users
from Handlers import start, write_handler, read_handler, off_handler, refactor_data_handler, delete_data_handler, \
    reset_password_handler


async def main():
    logging.basicConfig(level=logging.INFO, filename="paswords_bot_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_routers(start.router, write_handler.router, read_handler.router, off_handler.router,
                       refactor_data_handler.router, delete_data_handler.router, reset_password_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    await dp.shutdown(await close(), await close_users())


if __name__ == "__main__":
    asyncio.run(main())
