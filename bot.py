import asyncio
import logging
from handlers import common_router, bmi_router, calories_router

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_routers(common_router, bmi_router, calories_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')