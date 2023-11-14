from aiogram.filters import BaseFilter
from aiogram.types import Message
from passwords_db import db_conect, get_status

class StatusFilter(BaseFilter):
    def __init__(self, status: str):
        self.status = status

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.status, str):
            await db_conect(user_id=message.from_user.id)
            if self.status == await get_status(user_id=message.from_user.id):
                return True
        else:
            return False
