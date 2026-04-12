from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

gender_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Мужской', callback_data='male'), InlineKeyboardButton(text='Женский', callback_data='female')]])
activity_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='1 - Сидячий образ жизни', callback_data = '1.2')], 
                                                           [InlineKeyboardButton(text='2 - Активность 1–3 раза в неделю.', callback_data = '1.375')], 
                                                           [InlineKeyboardButton(text='3 - Активность 3–5 раз в неделю.', callback_data = '1.55')], 
                                                            [InlineKeyboardButton(text = '4 - Тренировки 6–7 раз в неделю.', callback_data = '1.725')], 
                                                            [InlineKeyboardButton(text = '5 - Экстремальная (2 тренировки в день)', callback_data = '1.9')]])