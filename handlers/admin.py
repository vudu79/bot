from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp
from client.http_client import *
from database import DBase
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards import inline_keyboard_lang

gifs = dict()
dbase = DBase()
storage = MemoryStorage()
leng_type = ""
leng_phrase = ""


class FSMSearch(StatesGroup):
    subj = State()
    limit = State()


# Машина состояний для searchAPI________________________________________________________________________________________
# Запускаем машину состояния FSMAdmin хэндлером


@dp.message_handler(Text(equals="Найти по слову", ignore_case=True))
async def choose_lang_handler(message: types.Message):
    await message.answer("Выберите язык на котором будете писать запрос", reply_markup=inline_keyboard_lang)


@dp.callback_query_handler(Text(startswith="leng__"), state=None)
async def colaback_hendler_lang_start_search(collback: types.CallbackQuery):
    res = collback.data.split("__")[1]
    global leng_type
    global leng_phrase
    if res == "rus_":
        leng_type.join("ru")
        leng_phrase.join("русском языке")
    elif res == "engl_":
        leng_type.join("en")
        leng_phrase.join("английском языке")
    await FSMSearch.subj.set()
    await collback.answer(f'Напишите ключевое слово для поиска на {leng_phrase}')


# Выход из состояния
@dp.message_handler(state="*", commands='отмена')
@dp.message_handler(Text(equals=['отмена', 'Отменить поиск'], ignore_case=True), state="*")
async def cansel_state_search(maseege: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await maseege.reply("Ok, отменяем)")
    await maseege.answer("Что будем искать?)")


# Устанавливаем машину состояния в состояние приема фото и запрашиваем у пользователя файл
@dp.message_handler(state=FSMSearch.subj)
async def load_subj_sm_search(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['subj'] = message.text
    await FSMSearch.next()
    await message.answer("Сколько найти? Максимальное количество - 1000 gifs")

# Устанавливаем машину состояния в состояние приема названия и запрашиваем у пользователя текст
@dp.message_handler(state=FSMSearch.limit)
async def load_limit_sm_search(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['limit'] = message.text
    await FSMSearch.next()
    await message.answer("Okey, я запомнил. Произвожу поиск ...")
    async with state.proxy() as data:
        list_gifs = search_req(data["subj"], data["limit"], leng_type)
        for gif in list_gifs:
            await message.answer(gif)
            await message.answer("Ну вот, что просили то и получили)) если ничего не появилось - я не виноват!!!")
    await state.finish()


# Машина состояний для randomAPI________________________________________________________________________________________


class FSMRandom(StatesGroup):
    subj = State()


@dp.message_handler(Text(equals="Случайная по слову", ignore_case=True), state=None)
async def cm_start_random(message: types.Message):
    await FSMRandom.subj.set()
    await message.answer("Напишите ключевое слово для поиска на английском языке")


@dp.message_handler(state="*", commands='отмена')
@dp.message_handler(Text(equals=['отмена', 'Отменить поиск'], ignore_case=True), state="*")
async def cansel_state_random(maseege: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await maseege.answer("Ok, отменяем)")
    await maseege.answer("Что будем искать?)")


@dp.message_handler(state=FSMRandom.subj)
async def load_subj_sm_random(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['subj'] = message.text
    await FSMSearch.next()
    await message.answer("Okey, я запомнил. Произвожу поиск ...")
    async with state.proxy() as data:
        await message.answer(random_req(data['subj']))
    await state.finish()


# Машина состояний для translateAPI________________________________________________

class FSMTranslate(StatesGroup):
    phrase = State()


@dp.message_handler(Text(equals="Гифка под фразу", ignore_case=True), state=None)
async def cm_start_translate(message: types.Message):
    await FSMTranslate.phrase.set()
    await message.answer("Напишите любую фразу на английском языке")


@dp.message_handler(state="*", commands='отмена')
@dp.message_handler(Text(equals=['отмена', 'Отменить поиск'], ignore_case=True), state="*")
async def cansel_state_translate(maseege: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await maseege.reply("Ok, отменяем)")
    await maseege.answer("Что будем искать?)")


@dp.message_handler(state=FSMTranslate.phrase)
async def load_subj_sm_translate(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phrase'] = message.text
    await FSMTranslate.next()
    await message.answer("Okey, я запомнил. Произвожу поиск ...")
    async with state.proxy() as data:
        await message.answer(translate_req(data['phrase']))
    await state.finish()


# trendAPI_________________________________________________________________

@dp.message_handler(Text(equals="Популярные гифки"))
async def trand_api(message: types.Message):
    await message.answer("Минутку, произвожу поиск...")
    global gifs
    gifs.clear()
    gifs = trend_req()
    for item in gifs.items():
        await message.answer(item[1], reply_markup=InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(text='Сохранить', callback_data=f'save_{item[0]}')))


@dp.callback_query_handler(Text(startswith="save_"))
async def colaback_hendler(collback: types.CallbackQuery):
    res = collback.data.split("_")[1]
    # dbase.save_gif(gifs[res])
    # print(gifs[res])
    await collback.answer("Изображение сохранено!")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(choose_lang_handler, Text(equals="Найти по слову", ignore_case=True))
    dp.register_callback_query_handler(colaback_hendler_lang_start_search, Text(startswith="leng__"), state=None)
    dp.register_message_handler(cansel_state_search, state="*", commands='отмена')
    dp.register_message_handler(load_subj_sm_search, state=FSMSearch.subj)
    dp.register_message_handler(load_limit_sm_search, state=FSMSearch.limit)

    dp.register_message_handler(cm_start_random, Text(equals="Случайная по слову", ignore_case=True), state=None)
    dp.register_message_handler(cansel_state_random, state="*", commands='отмена')
    dp.register_message_handler(load_subj_sm_random, state=FSMRandom.subj)

    dp.register_message_handler(cm_start_translate, Text(equals="Гифка под фразу", ignore_case=True), state=None)
    dp.register_message_handler(cansel_state_translate, state="*", commands='отмена')
    dp.register_message_handler(load_subj_sm_translate, state=FSMTranslate.phrase)

    dp.register_message_handler(trand_api, Text(equals="Популярные гифки"))
