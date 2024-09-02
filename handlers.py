from aiogram.filters import Command
from config import *
from aiogram import types
from aiogram import F, Router, Bot
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from db import Db
import json
import requests

API_TOKEN = BOT_TOKEN
bot = Bot(token=API_TOKEN)
router = Router()
bot_database = Db('users_db.db')

keyboard_list = [
    [KeyboardButton(text="Лишние"), KeyboardButton(text="Переделка")],
    [KeyboardButton(text="У6"), KeyboardButton(text="Хранение")]
]
keyboard = ReplyKeyboardMarkup(keyboard=keyboard_list, resize_keyboard=True)


@router.message(Command('start'))
async def start(message: types.Message):
    if not bot_database.check_user(message.from_user.id):
        await bot.send_message(message.from_user.id,
                               text="Привет. Это складской бот компании ЦСТК.\nЯ умею показывать остатки шин по "
                                    "ячейкам хранения и контейнерах.", reply_markup=keyboard)
        bot_database.add_user(message.from_user.id, message.from_user.username)
    else:
        await bot.send_message(message.from_user.id,
                               text="Привет. Это складской бот компании ЦСТК.\nЯ умею показывать остатки шин по "
                                    "ячейкам хранения и контейнерах.", reply_markup=keyboard)


@router.message(F.text == "Лишние")
async def ans_message(message: types.Message):
    msg = await bot.send_message(message.from_user.id, "🔄Подождите чуть-чуть")
    r = requests.get('http://176.67.54.67:777/UT10/hs/tire/case', headers=HEADERS)
    r.encoding = None
    if r.status_code == 200:
        data = json.loads(r.text)["Ячейки"][0]
        text = f'{data["СкладскаяЯчейка"]}\nКоличествоРасход {data["КоличествоРасход"]}\nКонечныйОстаток {data["КонечныйОстаток"]}'
        await bot.send_message(message.from_user.id, text, reply_markup=keyboard)
        await bot.delete_message(message.from_user.id, msg.message_id)
    else:
        await message.reply("Произошла ошибка при получение данных.", reply_markup=keyboard)
        await bot.delete_message(message.from_user.id, msg.message_id)


@router.message(F.text == "Переделка")
async def ans_message(message: types.Message):
    msg = await bot.send_message(message.from_user.id, "🔄Подождите чуть-чуть")
    r = requests.get('http://176.67.54.67:777/UT10/hs/tire/case', headers=HEADERS)
    r.encoding = None
    if r.status_code == 200:
        data = json.loads(r.text)["Ячейки"][1]
        text = f'{data["СкладскаяЯчейка"]}\nКоличествоРасход {data["КоличествоРасход"]}\nКонечныйОстаток {data["КонечныйОстаток"]}'
        await bot.send_message(message.from_user.id, text, reply_markup=keyboard)
        await bot.delete_message(message.from_user.id, msg.message_id)
    else:
        await message.reply("Произошла ошибка при получение данных.", reply_markup=keyboard)
        await bot.delete_message(message.from_user.id, msg.message_id)


@router.message(F.text == "У6")
async def ans_message(message: types.Message):
    msg = await bot.send_message(message.from_user.id, "🔄Подождите чуть-чуть")
    r = requests.get('http://176.67.54.67:777/UT10/hs/tire/case', headers=HEADERS)
    r.encoding = None
    if r.status_code == 200:
        data = json.loads(r.text)["Ячейки"][2]
        text = f'{data["СкладскаяЯчейка"]}\nКоличествоРасход {data["КоличествоРасход"]}\nКонечныйОстаток {data["КонечныйОстаток"]}'
        await bot.send_message(message.from_user.id, text, reply_markup=keyboard)
        await bot.delete_message(message.from_user.id, msg.message_id)
    else:
        await message.reply("Произошла ошибка при получение данных.", reply_markup=keyboard)
        await bot.delete_message(message.from_user.id, msg.message_id)


@router.message(F.text == "Хранение")
async def ans_message(message: types.Message):
    msg = await bot.send_message(message.from_user.id, "🔄Подождите чуть-чуть")
    r = requests.get('http://176.67.54.67:777/UT10/hs/tire/case', headers=HEADERS)
    r.encoding = None
    if r.status_code == 200:
        data = json.loads(r.text)["Ячейки"][3]
        text = f'{data["СкладскаяЯчейка"]}\nКоличествоРасход {data["КоличествоРасход"]}\nКонечныйОстаток {data["КонечныйОстаток"]}'
        await bot.send_message(message.from_user.id, text, reply_markup=keyboard)
        await bot.delete_message(message.from_user.id, msg.message_id)
    else:
        await message.reply("Произошла ошибка при получение данных.", reply_markup=keyboard)
        await bot.delete_message(message.from_user.id, msg.message_id)


@router.message(F.text)
async def ans_message(message: types.Message):
    msg = await bot.send_message(message.from_user.id, "🔄Подождите чуть-чуть")
    r = requests.get(URL, headers=HEADERS)
    r.encoding = None
    if r.status_code == 200:
        data = json.loads(r.text)["Ячейки"]

        size_input = message.text.strip()
        size_parts = size_input.replace('-', ' ').split()

        filtered_items = [
            item for item in data
            if all(part.lower() in item["Номенклатура"].lower() for part in size_parts)
        ]

        if not filtered_items:
            await message.reply("По вашему запросу ничего не найдено.", reply_markup=keyboard)
            await bot.delete_message(message.from_user.id, msg.message_id)
            return

        response = ""
        for item in filtered_items:
            response += (f"{item['Номенклатура']}\n"
                         f"Складская ячейка: {item['СкладскаяЯчейка']}\n"
                         f"Подразделение: {item['Подразделение']}\n"
                         f"Остаток: {item['КонечныйОстаток']}\n\n\n")

        max_length = 4096
        for i in range(0, len(response), max_length):
            await message.reply(response[i:i + max_length], reply_markup=keyboard)
        await bot.delete_message(message.from_user.id, msg.message_id)
    else:
        await message.reply("Произошла ошибка при получение данных.", reply_markup=keyboard)
        await bot.delete_message(message.from_user.id, msg.message_id)
