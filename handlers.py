from aiogram.filters import Command
from config import *
from aiogram import types
from aiogram import F, Router, Bot
from db import Db
import json
import re

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
        await bot.send_message(message.from_user.id,
                               text="Привет. Это складской бот компании ЦСТК.\nЯ умею показывать остатки шин по "
                                    "ячейкам хранения и контейнерах.")


@router.message(F.text)
async def ans_message(message: types.Message):
    with open('data/Остатки.json', 'r') as data_file:
        data = json.load(data_file)["Ячейки"]

    size_input = message.text.strip()
    size_parts = size_input.replace('-', ' ').split()

    filtered_items = [
        item for item in data
        if all(part in item["Номенклатура"] for part in size_parts)
    ]

    if not filtered_items:
        await message.reply("По вашему запросу ничего не найдено.")
        return

    response = ""
    for item in filtered_items:
        response += (f"{item['Номенклатура']}\n"
                     f"Складская ячейка: {item['СкладскаяЯчейка']}\n"
                     f"Подразделение: {item['Подразделение']}\n"
                     f"Остаток: {item['КонечныйОстаток']}\n\n\n")

    max_length = 4096
    for i in range(0, len(response), max_length):
        await message.reply(response[i:i + max_length])


@router.message(Command('help'))
async def help_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Это команда помощи. Чем могу помочь?')
