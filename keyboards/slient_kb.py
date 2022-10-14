from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, MenuButton

search_btn = KeyboardButton('/Выборка')
trend_btn = KeyboardButton('/Тренд')
random_btn = KeyboardButton('/Случайно')
translate_btn = KeyboardButton('/Перевести')

# translate_btn = KeyboardButton('поделится номером телефона', request_contact=True)
# translate_btn = KeyboardButton('дать свою локацию', request_location=True)

client_kb = ReplyKeyboardMarkup(resize_keyboard=True)

client_kb.add(search_btn).add(translate_btn).insert(random_btn).insert(trend_btn)



