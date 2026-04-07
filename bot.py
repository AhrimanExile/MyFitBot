import asyncio
import logging

from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

class Form(StatesGroup):
    weight = State()
    height = State()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f'Привет!!! Я твой помощник в мире фитнеса и правильного питания. Ты большой молодец что решил стать лучше. У тебя обязательно все получится я верю в тебя!!!')

@dp.message(Command('help'))
async def get_help(message: Message):
    await message.reply(f'Список доступных команд:\n/start - Начало работы с ботом.\n/help - Справочник по командам.\n/bmi - подсчет индекса массы тела.')

@dp.message(Command('bmi'))
async def start_bmi(message: Message, state: FSMContext):
    await message.answer('Введи свой вес.')
    await state.set_state(Form.weight)

@dp.message(Form.weight)
async def process_weight(message: Message, state: FSMContext):
    try:
        await state.update_data(weight = float(message.text))
        await message.answer('Теперь введи свой рост.')
        await state.set_state(Form.height)
    except ValueError:
        await message.answer('Вес должен содержать только цифры!\nПопробуй еще раз.')

@dp.message(Form.height)
async def process_height(message: Message, state: FSMContext):
    try:
        await state.update_data(height = float(message.text))

        user_data = await state.get_data()
        weight = user_data.get('weight')
        height = user_data.get('height')
        bmi = round(weight/(height/100) ** 2, 2)

        await message.answer(f'Твой bmi: {bmi}')
        match bmi:
            case n if n < 16:
                await message.answer(f'Выраженный дефицит массы')
            case n if n >= 16 and n <= 18.5:
                await message.answer(f'Недостаточная масса тела')
            case n if n > 18.5 and n <= 24.9:
                await message.answer(f'Нормальный вес')
            case n if n >= 25 and n <= 29.9:
                await message.answer(f'Избыточная масса (предожирение)')
            case n if n >= 30 and n <= 34.9:
                await message.answer(f'Ожирение I степени')
            case n if n >= 35 and n <= 39.9:
                await message.answer(f'Ожирение II степени')
            case n if n >= 40:
                await message.answer(f'Ожирение III степени')
        
        await state.clear()
    except ValueError:
        await message.answer('Рост должен содержать только цифры!\nПопробуй еще раз.')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')