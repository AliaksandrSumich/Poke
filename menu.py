import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile
from datetime import datetime
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types

import os



async def buttons_user(user, bot, dp: Dispatcher):

    keyboard_markup = types.InlineKeyboardMarkup(row_width=5)
    text_and_data = (('Заготовки', 'semi'),)
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    keyboard_markup.row(*row_btns)

    text_and_data = (('Блюда', 'dishes'),)
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    keyboard_markup.row(*row_btns)

    await bot.send_message(user, "Выберите нужную операцию", reply_markup=keyboard_markup)


async def menu_handler(query, bot, dp: Dispatcher):
    answer_data = query.data
    print(f'button {answer_data} pressed')




