from functools import wraps
from typing import Optional, List

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
                MESSAGE["INPUT_ERROR"],
                parse_mode="HTML",
            )
    return wrapper



def questions_to_html(questions: List[str]):
    return "".join(
        list(
            map(
                lambda item: f"{str(item[0]+1)}. <code>{item[1]}</code>\n",
                enumerate(questions)
            )
        )
    )