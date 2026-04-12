from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

bmi_router = Router()

class Form(StatesGroup):
    weight = State()
    height = State()

@bmi_router.message(Command('bmi'))
async def start_bmi(message: Message, state: FSMContext):
    await message.answer('Введи свой вес.')
    await state.set_state(Form.weight)

@bmi_router.message(Form.weight)
async def process_weight(message: Message, state: FSMContext):
    try:
        await state.update_data(weight = float(message.text))
        await message.answer('Теперь введи свой рост.')
        await state.set_state(Form.height)
    except ValueError:
        await message.answer('Вес должен содержать только цифры!\nПопробуй еще раз.')

@bmi_router.message(Form.height)
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