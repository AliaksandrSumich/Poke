import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile
from datetime import datetime
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types

import os

from database import DataBaseSemi
from kitchen import Kitchen
from user import get_all_users

db = DataBaseSemi()
kitchen = Kitchen()

users = get_all_users()

headers_semi = ['Номер этапа', 'Название этапа', 'Это ожидание? (1-да)', 'Время ожидания (заполнять если это ожидание), мин', 'Инструкция', 'Наименование продукта', 'Вопрос 1', 'Хэштег 1', 'Вопрос 2', 'Хэштег 2']

async def buttons_user(user, bot, dp: Dispatcher):

    keyboard_markup = types.InlineKeyboardMarkup(row_width=5)
    text_and_data = (('Заготовки', 'semi'),)
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    keyboard_markup.row(*row_btns)

    text_and_data = (('Блюда', 'dishes'),)
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    keyboard_markup.row(*row_btns)

    await bot.send_message(user, "Выберите нужную операцию", reply_markup=keyboard_markup)


async def next_stage_semi_cooking_dialog(query, bot, dp):
    answer_data = query.data
    print(f'answer data in next_stage_semi_cooking_dialog {answer_data}')

    # f'semi finish {semi_number} {stage_number}')
    semi_number = answer_data.split()[2]
    stage = answer_data.split()[3]

    data = kitchen.move_next_stage(semi_number)

    if not data:
        await bot.send_message(query.from_user.id, text='Работа закончена')
        kitchen.finish_semi(semi_number)


        await buttons_user(query.from_user.id, bot, dp)
        return

    text = f"Заготовка {data['semi_name']}\nЭтап номер {data[headers_semi[0]]}\n{data[headers_semi[1]]}\n{data[headers_semi[4]]}"

    await bot.send_message(query.from_user.id, text=text)

    # 'semi_number': self.semi_number,
    # 'stage_number': self.stage_number,
    # 'question_number': self.question_number,
    # 'question': self.question,
    # 'answer_tag': self.answer_tag,
    # 'answer': self.answer


    answer = {
        'semi_number': int(semi_number),
        'stage_number': int(stage) + 1,
        'question_number': None,
        'question': None,
        'answer_tag': None,
        'answer': None
    }

    await ask_next_question(query.from_user.id, int(stage) + 1, bot, dp, answer=answer)


async def menu_handler(query, bot, dp: Dispatcher):
    answer_data = query.data

    print(f'button {answer_data} pressed')

    if answer_data == 'semi':
        await semi_menu(query, bot, dp)
        return

    if 'semi' in answer_data and 'finish' not in answer_data:
        await new_semi_cooking_dialog(query, bot, dp)

    if 'semi finish' in answer_data:
        print('semi finish in answer_data')
        await next_stage_semi_cooking_dialog(query, bot, dp)


async def semi_menu(query, bot, dp: Dispatcher):
    semi_list = db.semi_list()
    print(query)

    keyboard_markup = types.InlineKeyboardMarkup(row_width=5)
    for semi in semi_list:
        text_and_data = ((semi, f'semi {semi}'),)
        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
        keyboard_markup.row(*row_btns)

    await bot.send_message(chat_id=query.from_user.id, text='Выберите одну из заготовок', reply_markup=keyboard_markup)


async def new_semi_cooking_dialog(query, bot, dp: Dispatcher):
    answer_data = query.data
    semi = answer_data.replace('semi ', '')
    print(f'Semi {semi} chosen')
    global users
    if not users.get(query.from_user.id):
        users = get_all_users()
    data = kitchen.start_new_semi(users[query.from_user.id], semi)

    text = f"Заготовка {semi}\nЭтап номер {data[headers_semi[0]]}\n{data[headers_semi[1]]}\n{data[headers_semi[4]]}"

    await bot.send_message(query.from_user.id, text=text)
    print(users)

    if data.get(headers_semi[6]):
        # question number 1
        await bot.send_message(query.from_user.id, text=data[headers_semi[6]])
        users[query.from_user.id].set_question(data['semi_number'], 0, 1, data[headers_semi[6]], data[headers_semi[7]])
        print(users[query.from_user.id])
        return
    else:
        await send_finish_semi_stage_button(query.from_user.id, bot, data['semi_number'], data['stage_number'], dp)

async def send_finish_semi_stage_button(user_id, bot, semi_number, stage_number, dp: Dispatcher):
    print(f'send_finish_semi_stage_button with semi_number {semi_number}, stage_number {stage_number}')

    keyboard_markup = types.InlineKeyboardMarkup(row_width=5)
    text_and_data = (('Этап завершен', f'semi finish {semi_number} {stage_number}'),)
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    keyboard_markup.row(*row_btns)

    await bot.send_message(user_id, "Подтвердите завершение этапа", reply_markup=keyboard_markup)


async def none_state_message_handler(message, bot, dp: Dispatcher):

    user = users[message.from_user.id]
    if user.question:
        user.answer = message.text
        answer = user.get_answer()
        await ask_next_question(message.from_user.id, answer['stage_number'], bot, dp, answer=answer)
    else:
        semi_number = user.semi_number
        stage_number = user.stage_number
        await send_finish_semi_stage_button(message.from_user.id, bot, semi_number, stage_number, dp)
        user.reset_question(user.semi_number, user.stage_number)



async def ask_next_question(user_id, stage, bot, dp: Dispatcher, answer):

    user = users[user_id]

    next_question = kitchen.set_semi_answer(answer)
    if next_question:
        user.set_question(next_question['semi_number'],
                          next_question['stage_number'],
                          next_question['number'],
                          next_question['question'],
                          next_question['tag'])

        await bot.send_message(user_id, text=next_question['question'])
    else:
        semi_number = user.semi_number

        await send_finish_semi_stage_button(user_id, bot, semi_number, stage, dp)
        user.reset_question(user.semi_number, stage)













