import aiosqlite
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from keyboards import gender_keyboard
from database import add_user

profile_router = Router()

class profile(StatesGroup):
    gender = State()
    age = State()
    weight = State()
    height = State()

@profile_router.message(Command('profile'))
async def start_profile(message: Message, state: FSMContext):
    await message.answer('Укажите свой пол:', reply_markup=gender_keyboard)
    await state.set_state(profile.gender)

@profile_router.callback_query(F.data.in_(['male', 'female']), profile.gender)
async def procces_gender(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(gender = callback.data)

    gender_text = 'Мужской' if callback.data == 'male' else 'Женский'
    await callback.message.edit_text(f'Ваш пол: {gender_text}')

    await callback.message.answer('Теперь введите свой возраст:')
    await state.set_state(profile.age)

@profile_router.message(profile.age)
async def procces_age(message: Message, state: FSMContext):
    try:
        await state.update_data(age = int(message.text))
        await message.answer('Теперь введите свой вес:')
        await state.set_state(profile.weight)
    except ValueError:
        await message.answer('Возраст должен содержать только целые цифры!\nПопробуйте еще раз.')

@profile_router.message(profile.weight)
async def procces_weight(message: Message, state: FSMContext):
    try:
        await state.update_data(weight = float(message.text))
        await message.answer('Теперь введите свой рост:')
        await state.set_state(profile.height)
    except ValueError:
        await message.answer('Вес должен содержать только цифры!\nПопробуйте еще раз.')

@profile_router.message(profile.height)
async def procces_height(message: Message, state: FSMContext):
    try:
        await state.update_data(height = float(message.text))
        user_data = await state.get_data()
        await add_user(message.from_user.id, user_data.get('gender'), user_data.get('age'), user_data.get('weight'), user_data.get('height'))
        await state.clear()

    except ValueError:
        await message.answer('Рост должен содержать только цифры!\nПопробуйте еще раз.')
    except aiosqlite.Error:
        await message.answer('Ошибка базы данных. Попробуйте позже.')