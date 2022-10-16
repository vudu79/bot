from aiogram import types, Dispatcher
from keyboards import reply_keyboard
from create_bot import dp, bot



@dp.message_handler(commands=['start', 'help'])
async def start_handler(message : types.Message):
    await bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}!. Это бот для поиска гифок разными способами)).', reply_markup=reply_keyboard)
    await bot.send_message(message.from_user.id, "Что будем искать?)")

@dp.message_handler(commands=['Выборка'])
async def start_handler(message : types.Message):
    await bot.send_message(message.from_user.id, 'Поиск gif картинок по заданному ключевому слову.' )


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(start_handler, commands=['start', 'help'])
