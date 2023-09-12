import asyncio
import logging
import os

from dotenv import load_dotenv
load_dotenv()

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor



# Initialize bot and dispatcher
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('broadcast')


@dp.message_handler(commands=['start'], state='*')
async def echo(message: types.Message, state: FSMContext):
    await state.finish()
    user = message.from_user.id
    await bot.send_message(text=f'Добро пожаловать! Твой телеграм ID {user}', chat_id=user)



if __name__ == '__main__':
    # executor.start_polling(dp, skip_updates=True, on_startup=vnesenie_v_tablicy )
    executor.start_polling(dp, skip_updates=True)