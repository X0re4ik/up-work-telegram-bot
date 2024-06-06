from functools import wraps
from typing import Optional

from aiogram.types import Message

from .messages import MESSAGE
from .services import telegram_user_service


def is_authorized(function):
    @wraps(function)
    async def wrapper(*args, **kwargs):
        message: Message = args[0]
        telegram_id = message.from_user.id
        is_valid: bool = await telegram_user_service.is_valid_user(telegram_id)
        if is_valid is False:
            return await message.answer(
                MESSAGE["NOT_REGISTERED"],
                parse_mode="HTML",
            )
        return await function(*args, **kwargs)
    return wrapper



def error_handler(function):
    @wraps(function)
    async def wrapper(*args, **kwargs):
        message: Message = args[0]
        try:
            return await function(*args, **kwargs)
        except Exception as e:
            return await message.answer(
                str(e)
            )
    return wrapper
    