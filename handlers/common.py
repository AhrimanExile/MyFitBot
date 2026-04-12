from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

common_router = Router()

@common_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f'Привет!!! Я твой помощник в мире фитнеса и правильного питания. Ты большой молодец что решил стать лучше. У тебя обязательно все получится я верю в тебя!!!')

@common_router.message(Command('help'))
async def get_help(message: Message):
    await message.reply(f'Список доступных команд:\n/start - Начало работы с ботом.\n/help - Справочник по командам.\n/bmi - подсчет индекса массы тела.\n/calories - расчёт нормы калорий по формуле Миффлина-Сан Жеора.')