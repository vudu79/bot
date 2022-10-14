from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()

# Запускаем машину состояния FSMAdmin хэндлером
@dp.message_handler(commands=['загрузить'], state=None)
async def cm_start(message : types.Message):
    await FSMAdmin.photo.set()
    await message.reply("загрузите фото")

# Устанавливаем машину состояния в состояние приема фото и запрашиваем у пользователя файл
@dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_fhoto(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply("Введи название")

# Устанавливаем машину состояния в состояние приема названия и запрашиваем у пользователя текст
@dp.message_handler(state=FSMAdmin.name)
async def load_name(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply("Введи описание")

# Устанавливаем машину состояния в состояние приема описания и запрашиваем у пользователя текст
@dp.message_handler(state=FSMAdmin.description)
async def load_description(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.reply("Теперь введи цену")

# Устанавливаем машину состояния в состояние приема цены товара и запрашиваем у пользователя текст. В конце останавливаем машину состояния
@dp.message_handler(state=FSMAdmin.price)
async def load_price(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)

    # ПОСЛЕ КОМАНДЫ finish() очишаются все данные в state storage!!!!
    async with state.proxy() as data:
        await message.reply(str(data))
    await state.finish()

# Выход из состояния
@dp.message_handler(state="*", commands='отмена')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cansel_state(maseege : types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await maseege.reply("Ok")


def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands=['загрузить'], state=None)
    dp.register_message_handler(load_fhoto, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(cansel_state, state="*", commands='отмена')
    dp.register_message_handler(cansel_state, Text(equals='отмена', ignore_case=True), state="*")
