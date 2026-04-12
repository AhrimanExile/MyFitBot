import asyncio
import logging

from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from aiogram import Bot, Dispatcher, F

from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

gender_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Мужской', callback_data='male'), InlineKeyboardButton(text='Женский', callback_data='female')]])
activity_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='1 - Сидячий образ жизни', callback_data = '1.2')], 
                                                           [InlineKeyboardButton(text='2 - Активность 1–3 раза в неделю.', callback_data = '1.375')], 
                                                           [InlineKeyboardButton(text='3 - Активность 3–5 раз в неделю.', callback_data = '1.55')], 
                                                            [InlineKeyboardButton(text = '4 - Тренировки 6–7 раз в неделю.', callback_data = '1.725')], 
                                                            [InlineKeyboardButton(text = '5 - Экстремальная (2 тренировки в день)', callback_data = '1.9')]])

class Form(StatesGroup):
    weight = State()
    height = State()

class Mifflin(StatesGroup):
    gender = State()
    age = State()
    weight = State()
    height = State()
    activity = State()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f'Привет!!! Я твой помощник в мире фитнеса и правильного питания. Ты большой молодец что решил стать лучше. У тебя обязательно все получится я верю в тебя!!!')

@dp.message(Command('help'))
async def get_help(message: Message):
    await message.reply(f'Список доступных команд:\n/start - Начало работы с ботом.\n/help - Справочник по командам.\n/bmi - подсчет индекса массы тела.\n/calories - расчёт нормы калорий по формуле Миффлина-Сан Жеора.')

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

        match bmi:
            case n if n < 16:
                await message.answer(f'Твой bmi: {bmi}\nВыраженный дефицит массы')
            case n if n >= 16 and n <= 18.5:
                await message.answer(f'Твой bmi: {bmi}\nНедостаточная масса тела')
            case n if n > 18.5 and n <= 24.9:
                await message.answer(f'Твой bmi: {bmi}\nНормальный вес')
            case n if n >= 25 and n <= 29.9:
                await message.answer(f'Твой bmi: {bmi}\nИзбыточная масса (предожирение)')
            case n if n >= 30 and n <= 34.9:
                await message.answer(f'Твой bmi: {bmi}\nОжирение I степени')
            case n if n >= 35 and n <= 39.9:
                await message.answer(f'Твой bmi: {bmi}\nОжирение II степени')
            case n if n >= 40:
                await message.answer(f'Твой bmi: {bmi}\nОжирение III степени')
        
        await state.clear()
    except ValueError:
        await message.answer('Рост должен содержать только цифры!\nПопробуй еще раз.')

@dp.message(Command('calories'))
async def start_calories(message: Message, state: FSMContext):
    await message.answer('Сейчас рассчитаем твою суточную норму калорий по формуле Миффлина-Сан Жеора. Начнём!\n\nУкажи свой пол:', reply_markup=gender_keyboard)
    await state.set_state(Mifflin.gender)

@dp.callback_query(F.data.in_(['male', 'female']), Mifflin.gender) # Mifflin.gender не даст редактировать состояние gender если оно уже установленно
async def procces_male(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.update_data(gender = callback.data)

    #редактируем старое сообщение на новое без кнопок
    gender_text = 'Мужской'  if callback.data == 'male' else 'Женский'
    await callback.message.edit_text(f'Ваш пол: {gender_text}')

    await callback.message.answer('Отлично теперь введи свой возраст:')
    await state.set_state(Mifflin.age)

@dp.message(Mifflin.age)
async def procces_age(message: Message, state: FSMContext):
    try:
        await state.update_data(age = int(message.text))
        await message.answer('Теперь введи свой вес:')
        await state.set_state(Mifflin.weight)
    except ValueError:
        await message.answer('Возраст должен содержать только целые цифры!\nПопробуйте еще раз.')

@dp.message(Mifflin.weight)
async def process_mifflinWeight(message: Message, state: FSMContext):
    try:
        await state.update_data(weight = float(message.text))
        await message.answer('Теперь введи свой рост:')
        await state.set_state(Mifflin.height)
    except ValueError:
        await message.answer('Вес должен содержать только цифры!\nПопробуйте еще раз.')

@dp.message(Mifflin.height)
async def process_mifflinHeight(message: Message, state: FSMContext):
    try:
        await state.update_data(height = float(message.text))
        await message.answer('Выбери уровень своей активности.', reply_markup=activity_keyboard)
        await state.set_state(Mifflin.activity)
    except ValueError:
        await message.answer('Рост должен содержать только цифры!\nПопробуйте еще раз.')

@dp.callback_query(F.data.in_(['1.2', '1.375', '1.55', '1.725', '1.9']), Mifflin.activity)
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

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')