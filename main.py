import asyncio

import os

from dotenv import load_dotenv

from database import DataBaseUsers
from menu import buttons_user, menu_handler, none_state_message_handler

load_dotenv()

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

# Initialize bot and dispatcher
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())

users_db = DataBaseUsers()


@dp.message_handler(commands=['start'], state='*')
async def echo(message: types.Message, state: FSMContext):
    await state.finish()
    user = [message.from_user.id, message.from_user.first_name, 'user']
    users_db.write_new_user(user)

    await buttons_user(message.from_user.id, bot, dp)


@dp.callback_query_handler(state=None)
async def inline_kb_answer_callback_handler(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    try:
        await query.message.delete()
    except:
        print('Кнопки были старые. Удалить не удалось.')

    await menu_handler(query, bot, dp)


@dp.message_handler(state=None)
async def echo(message: types.Message, state: FSMContext):
    print(f'None state message {message.text} form {message.from_user.id}')
    await none_state_message_handler(message, bot, dp)





if __name__ == '__main__':
    # executor.start_polling(dp, skip_updates=True, on_startup=vnesenie_v_tablicy )
    executor.start_polling(dp, skip_updates=True)