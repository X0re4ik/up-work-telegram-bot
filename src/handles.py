
from functools import wraps
from typing import Optional, Type

from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message

from config.configs import redis_config

from .messages import COMMANDS, MESSAGE
from .services import UserAccount, telegram_user_service
from .utils import is_authorized


class RegistrationState(StatesGroup):
    START_WORKED = State()
    
    ENTERED_SECURITY_TOKEN = State()
    ENTERED_USER_UID = State()
    ENTERED_ORG_UID = State()
    
    READY_TO_RECORD_CONDITIONS = State()

class QuestionState(StatesGroup):
    START_WORKED = State()


storage = RedisStorage.from_url(redis_config.URL)
dp = Dispatcher(storage=storage)


default_parse_mode = "HTML"


@dp.message(Command(COMMANDS["HELP"]))
async def command_help(message: Message) -> None:
    await message.answer(
        text=MESSAGE["HELP"],
        parse_mode=default_parse_mode
    )

@dp.message(Command(COMMANDS["START"]))
async def command_start(message: Message) -> None:
    await message.answer(
        text=MESSAGE["HELP"],
        parse_mode=default_parse_mode
    )


@dp.message(Command(COMMANDS["GET"]))
@is_authorized
async def command_get(message: Message) -> None:
    
    user_account = await telegram_user_service.get_account(
        message.from_user.id
    )
    
    return await message.answer(
        text=MESSAGE["GET_ACCOUNT"].format(
            user_account.telegram_id,
            user_account.org_uid,
            user_account.user_uid,
            user_account.security_token,
            user_account.status,
            user_account.question,
        ),
        parse_mode=default_parse_mode
    )



@dp.message(Command(COMMANDS["CREATE_ACCOUNT"]))
async def command_start_create_account(message: Message, state: FSMContext) -> None:
    telegram_id = message.from_user.id
    user = await telegram_user_service.get_account(telegram_id)
    if user is not None:
        return await message.answer(
            text=MESSAGE["ACCOUNT_ALREADY_CREATED"],
            parse_mode=default_parse_mode
        )
        
    await message.answer(
        MESSAGE["INPUT_SECRET_TOKEN"],
        parse_mode=default_parse_mode
    )
    await state.set_state(RegistrationState.START_WORKED)



@dp.message(Command(COMMANDS["DELETE_ACCOUNT"]))
@is_authorized
async def command_delete_account(message: Message) -> None:
    await telegram_user_service.delete_account(message.from_user.id)
    await message.answer(
        MESSAGE["ACCOUNT_DELETE"],
        parse_mode=default_parse_mode
    )


@dp.message(Command(COMMANDS["SET_QUERY"]))
@is_authorized
async def command_set_query(message: Message, state: FSMContext) -> None:
    await message.answer(
        MESSAGE["SET_QUERY"],
        parse_mode=default_parse_mode
    )
    await state.set_state(QuestionState.START_WORKED)

@dp.message(Command(COMMANDS["RESET"]))
async def command_help(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(None)
    await message.answer(
        text=MESSAGE["CANCEL"],
        parse_mode=default_parse_mode
    )



@dp.message(QuestionState.START_WORKED)
@is_authorized
async def command_start_worker(message: Message, state: FSMContext) -> None:
    text = message.text
    question = await telegram_user_service.add_question(message.from_user.id, text)
    await message.answer(
        text=f"Запросы: {str(question)}",
    )
    await state.set_state(None)
    


@dp.message(RegistrationState.START_WORKED)
async def command_start_worked(message: Message, state: FSMContext) -> None:
    await state.update_data({"securityToken": message.text.strip()})
    await message.answer(
        MESSAGE["INPUT_ORG_UID"], 
        parse_mode=default_parse_mode
    )
    await state.set_state(RegistrationState.ENTERED_SECURITY_TOKEN)


@dp.message(RegistrationState.ENTERED_SECURITY_TOKEN)
async def command_entered_security_token(message: Message, state: FSMContext) -> None:
    await state.update_data({ "orgUid": message.text.strip() })    
    await message.answer(
        MESSAGE["INPUT_USER_UID"], 
        parse_mode=default_parse_mode
    )
    await state.set_state(RegistrationState.ENTERED_USER_UID)    

@dp.message(RegistrationState.ENTERED_USER_UID)
async def command_entered_user_uid(message: Message, state: FSMContext) -> None:
    await state.update_data({ "userUid": message.text.strip() })
    data = await state.get_data()
    
    telegram_id = message.from_user.id
    user = await telegram_user_service.create_account(
        telegram_id,
        security_token=data["securityToken"],
        user_uid=data["userUid"],
        org_uid=data["orgUid"],
    )
    
    await message.answer(
        MESSAGE["USER_SUCCESS_REGISTERED"],
        parse_mode=default_parse_mode,
    )
    await state.set_state(RegistrationState.READY_TO_RECORD_CONDITIONS)
    

@dp.message(Command(COMMANDS["RESET_QUERY"]))
@is_authorized
async def command_reset_query(message: Message) -> None:
    await telegram_user_service.delete_all_questions(message.from_user.id)
    await message.answer(
        MESSAGE["RESET_QUERY"],
        parse_mode=default_parse_mode,
    )
