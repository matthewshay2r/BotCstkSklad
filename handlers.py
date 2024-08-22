from aiogram.filters import Command
from config import *
from aiogram import types
from aiogram import F, Router, Bot
from db import Db

API_TOKEN = BOT_TOKEN
bot = Bot(token=API_TOKEN)
router = Router()
bot_database = Db('users_db.db')


@router.message(Command('start'))
async def start(message: types.Message):
    if not bot_database.check_user(message.from_user.id):
        await bot.send_message(message.from_user.id,
                               text="Привет. Это складской бот компании ЦСТК.\nЯ умею показывать остатки шин по "
                                    "ячейкам хранения и контейнерах.")
        bot_database.add_user(message.from_user.id, message.from_user.username)
    else:
        await bot.send_message(message.from_user.id, 'Привет!')


@router.message(F.text)
async def ans_message(message: types.Message):
    await bot.send_message(message.from_user.id, message.text)


@router.message(Command('help'))
async def help_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Это команда помощи. Чем могу помочь?')
