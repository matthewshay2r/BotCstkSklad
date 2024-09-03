from aiogram.filters import Command
from config import *
from aiogram import types
from aiogram import F, Router, Bot
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from db import Db
import json
import requests
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
                                    "ячейкам хранения и контейнерах.", reply_markup=types.ReplyKeyboardRemove())
        bot_database.add_user(message.from_user.id, message.from_user.username)
    else:
        await bot.send_message(message.from_user.id,
                               text="Привет. Это складской бот компании ЦСТК.\nЯ умею показывать остатки шин по "
                                    "ячейкам хранения и контейнерах.", reply_markup=types.ReplyKeyboardRemove())


@router.message(F.text)
async def ans_message(message: types.Message):
    msg = await bot.send_message(message.from_user.id, "🔄Подождите чуть-чуть")
    r = requests.get(URL, headers=HEADERS)
    r.encoding = None
    if r.status_code == 200:
        data = json.loads(r.text)["Ячейки"]
        formatted_data = {}

        for item in data:
            nomenclature = item['Номенклатура']
            storage_cell = item['СкладскаяЯчейка']
            department = item['Подразделение']
            stock = item['КонечныйОстаток']

            key = f"{storage_cell}_{department} {stock}"

            if nomenclature not in formatted_data:
                formatted_data[nomenclature] = []

            formatted_data[nomenclature].append(key)
        pattern = r'к\d+'
        filtered_items = []
        if re.findall(pattern, message.text.lower(), re.IGNORECASE):
            for item in formatted_data:
                for i in range(len(formatted_data[item])):
                    if formatted_data[item][i].lower().split('_')[0] in message.text.lower():
                        filtered_items.append({item: formatted_data[item]})
                        break
        else:
            size_input = message.text.strip()
            size_parts = size_input.replace('-', ' ').split()
            for item in formatted_data:
                if all(part.lower() in item.lower() for part in size_parts):
                    filtered_items.append({item: formatted_data[item]})
        if not filtered_items:
            await message.reply("По вашему запросу ничего не найдено.", reply_markup=types.ReplyKeyboardRemove())
            await bot.delete_message(message.from_user.id, msg.message_id)
            return

        response = ""
        for item in filtered_items:
            name = list(item.keys())[0]
            place = '\n'.join(*item.values())
            response += (f"{name}\n{place}\n\n")

        max_length = 4096
        for i in range(0, len(response), max_length):
            await message.reply(response[i:i + max_length], reply_markup=types.ReplyKeyboardRemove())
        await bot.delete_message(message.from_user.id, msg.message_id)
    else:
        await message.reply("Произошла ошибка при получение данных.", reply_markup=types.ReplyKeyboardRemove())
        await bot.delete_message(message.from_user.id, msg.message_id)
