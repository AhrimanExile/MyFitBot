import asyncio
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f'Привет.')

async def main():
    await dp.start_polling(bot)

asyncio.run(main())