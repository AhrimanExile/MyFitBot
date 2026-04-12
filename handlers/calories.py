from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from keyboards import gender_keyboard, activity_keyboard

calories_router = Router()

class Mifflin(StatesGroup):
    gender = State()
    age = State()
    weight = State()
    height = State()
    activity = State()


@calories_router.message(Command('calories'))
async def start_calories(message: Message, state: FSMContext):
    await message.answer('Сейчас рассчитаем твою суточную норму калорий по формуле Миффлина-Сан Жеора. Начнём!\n\nУкажи свой пол:', reply_markup=gender_keyboard)
    await state.set_state(Mifflin.gender)

@calories_router.callback_query(F.data.in_(['male', 'female']), Mifflin.gender) # Mifflin.gender не даст редактировать состояние gender если оно уже установленно
async def procces_male(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(gender = callback.data)

    #редактируем старое сообщение на новое без кнопок
    gender_text = 'Мужской'  if callback.data == 'male' else 'Женский'
    await callback.message.edit_text(f'Ваш пол: {gender_text}')

    await callback.message.answer('Отлично теперь введи свой возраст:')
    await state.set_state(Mifflin.age)

@calories_router.message(Mifflin.age)
async def procces_age(message: Message, state: FSMContext):
    try:
        await state.update_data(age = int(message.text))
        await message.answer('Теперь введи свой вес:')
        await state.set_state(Mifflin.weight)
    except ValueError:
        await message.answer('Возраст должен содержать только целые цифры!\nПопробуйте еще раз.')

@calories_router.message(Mifflin.weight)
async def process_mifflinWeight(message: Message, state: FSMContext):
    try:
        await state.update_data(weight = float(message.text))
        await message.answer('Теперь введи свой рост:')
        await state.set_state(Mifflin.height)
    except ValueError:
        await message.answer('Вес должен содержать только цифры!\nПопробуйте еще раз.')

@calories_router.message(Mifflin.height)
async def process_mifflinHeight(message: Message, state: FSMContext):
    try:
        await state.update_data(height = float(message.text))
        await message.answer('Выбери уровень своей активности.', reply_markup=activity_keyboard)
        await state.set_state(Mifflin.activity)
    except ValueError:
        await message.answer('Рост должен содержать только цифры!\nПопробуйте еще раз.')

@calories_router.callback_query(F.data.in_(['1.2', '1.375', '1.55', '1.725', '1.9']), Mifflin.activity)
async def process_activity(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(activity = float(callback.data))

    user_data = await state.get_data()
    if user_data.get('gender') == 'male':
        bmr = 10 * user_data.get('weight') + 6.25 * user_data.get('height') - 5 * user_data.get('age') + 5
    else:
        bmr = 10 * user_data.get('weight') + 6.25 * user_data.get('height') - 5 * user_data.get('age') - 161
    
    tdee = round(bmr * float(user_data.get('activity')))
    await callback.message.answer(f'Для поддержания веса твоя суточная норма калорий составит: {tdee} ккал')
    await state.clear()