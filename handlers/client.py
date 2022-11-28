from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from keyboards import reply_keyboard_main_menu
from create_bot import dp, bot
from aiogram.utils import exceptions
from aiogram.utils.callback_data import CallbackData


@dp.errors_handler(exception=exceptions.RetryAfter)
async def exception_handler(update: types.Update, exception: exceptions.RetryAfter):
    await bot.send_message(update.message.from_user.id, "Не надо мне тут спамить!!!")

    return True


@dp.message_handler(commands=['start', 'help'])
async def start_handler(message: types.Message):
    await bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}!')
    await bot.send_message(message.from_user.id, 'Это бот для поиска полезного и не очень медиа в интернете.',
                           reply_markup=reply_keyboard_main_menu)
    await bot.send_message(message.from_user.id, "Что будем искать?")
    await bot.send_message(message.from_user.id, "Тыц 👇")


@dp.message_handler(Text(equals="Меню", ignore_case=True))
async def main_menu_handler(message: types.Message):
    # await bot.send_message(message.from_user.id, "", reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(message.from_user.id, "...", reply_markup=reply_keyboard_main_menu)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start', 'help'])
    dp.register_message_handler(main_menu_handler, Text(equals="Меню", ignore_case=True))
    dp.register_errors_handler(exception_handler, exception=exceptions.RetryAfter)
