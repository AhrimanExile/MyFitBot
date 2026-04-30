import aiosqlite
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from database import get_userprofile

myprofile_router = Router()

@myprofile_router.message(Command('myprofile'))
async def myprofile(message: Message):
    user_id = message.from_user.id
    user = await get_userprofile(user_id)
    if user is None:
        await message.answer('Пользователь не найден.\n' \
        'Для регистрации введите данные при помощи команды /profile')
    else:
       text = (
            f"📋 **Ваш профиль:**\n"
            f"👤 Пол: {'Мужчина' if user[1] == 'male' else 'Жунщина'}\n"
            f"🎂 Возраст: {user[2]}\n"
            f"⚖️ Вес: {user[3]} кг\n"
            f"📏 Рост: {user[4]} см"
        )
       await message.answer(text, parse_mode='Markdown')