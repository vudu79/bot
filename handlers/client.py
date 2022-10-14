from aiogram import types, Dispatcher
from create_bot import bot, dp
from keyboards import client_kb


@dp.message_handler(commands=['start', 'help'])
async def start_handler(message : types.Message):
    await bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}!. Это бот для поиска гифок с различных ресурсов интернета.', reply_markup=client_kb)


@dp.message_handler(commands=['Выборка'])
async def start_handler(message : types.Message):
    await bot.send_message(message.from_user.id, 'Поиск gif картинок по заданному ключевому слову.' )


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(start_handler, commands=['start', 'help'])
