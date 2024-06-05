from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config.configs import telegram_config

TOKEN = telegram_config.TOKEN
print(TOKEN, "TOKEN")
BOT = Bot(
    token=TOKEN, 
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)