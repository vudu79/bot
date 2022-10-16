from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

search_btn = KeyboardButton('Найти по слову')
trend_btn = KeyboardButton('Популярные гифки')
random_btn = KeyboardButton('Случайная по слову')
translate_btn = KeyboardButton('Гифка под фразу')
cansel_btn = KeyboardButton('Отменить поиск')

# translate_btn = KeyboardButton('поделится номером телефона', request_contact=True)
# translate_btn = KeyboardButton('дать свою локацию', request_location=True)
reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
reply_keyboard.add(search_btn).add(translate_btn).insert(random_btn).insert(trend_btn).add(cansel_btn)


inline_keyboard = InlineKeyboardMarkup(row_width=2)
add_me = InlineKeyboardButton(text="Like", callback_data="like_1")
add_all = InlineKeyboardButton(text="Dislike", callback_data="like_-1")

inline_keyboard.add(add_me, add_all)

