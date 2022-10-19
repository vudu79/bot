from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from client.http_client import *
from database import DBase
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards import inline_keyboard_lang, inline_keyboard_category
from aiogram.utils.markdown import text, italic, bold

gifs = dict()
dbase = DBase()
storage = MemoryStorage()
leng_type = ""
leng_phrase = ""
teg_list = []


@dp.message_handler(Text(equals="Популярные категории", ignore_case=True), state=None)
async def category_handler(message: types.Message):
    await message.answer("Часто ищут сейчас:")
    global teg_list
    teg_list.clear()
    teg_list = get_categories_tenor_req()
    for teg in teg_list:
        await bot.send_animation(message.from_user.id, teg["image"])
        await bot.send_message(message.from_user.id, bold('Показать варианты из категории'),
                               parse_mode=ParseMode.MARKDOWN,
                               reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                   InlineKeyboardButton(text=f'{teg["searchterm"]}',
                                                        callback_data=f'category__{teg["searchterm"]}')))


@dp.callback_query_handler(Text(startswith="category__"), state=None)
async def colaback_hendler_show_list_category(collback: types.CallbackQuery):
    res = collback.data.split("__")[1]
    await collback.answer(f'Выбрана категория {res}')
    gifs_from_tenor_list = get_category_list_tenor_req(res)
    for gif in gifs_from_tenor_list:
        await bot.send_animation(collback.from_user.id, gif, reply_markup=InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton(text="Сохранить в базу", callback_data="save__")))
    await collback.answer()
    await bot.send_message(collback.message.from_user.id,
                           "Сделано! Могу собрать все популярные теги в кучу, чтобы не листать навех))",
                           reply_markup=InlineKeyboardMarkup(row_width=2).row(
                               InlineKeyboardButton(text="Собрать в кучу", callback_data="collect_cat__yes"),
                               InlineKeyboardButton(text="Буду листать", callback_data="collect_cat__no")))


@dp.callback_query_handler(Text(startswith="collect_cat__"), state=None)
async def colaback_hendler_collect_category(collback: types.CallbackQuery):
    res = collback.data.split("__")[1]
    if res == "yes":
        for teg in teg_list:
            inline_keyboard_category.add(InlineKeyboardButton(text=f'{teg["searchterm"]}', callback_data=f'category__{teg["searchterm"]}'))

        await bot.send_message(collback.from_user.id, bold('Вот что получилось. Выбирайте!'),
                               parse_mode=ParseMode.MARKDOWN,
                               reply_markup=inline_keyboard_category)
        await collback.answer()
    else:
        if res == "no":
            await bot.send_message(collback.from_user.id, bold('Ну... тогда листайте))'))
            await collback.answer()



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
    print(f'Выбран язык - {res}')
    global leng_type
    global leng_phrase
    if res == "rus_":
        leng_type = "ru"
        leng_phrase = "русском языке"
        print(leng_type)
    elif res == "engl_":
        leng_type = "en"
        leng_phrase = "английском языке"
        print(leng_type)
    await FSMSearch.subj.set()
    await collback.answer()
    await bot.send_message(collback.from_user.id, f'Напишите ключевое слово поиска на {leng_phrase}')


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
    await message.answer("Сколько найти? Максимальное количество - 1000 gifs. Пишите число, это например 1, 2, 22))")


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
            await bot.send_animation(message.from_user.id, gif, reply_markup=InlineKeyboardMarkup(row_width=1).add(
                InlineKeyboardButton(text="Сохранить в базу", callback_data="save__")))
        await message.answer("Сделано, жду команд!")
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
        await bot.send_animation(message.from_user.id, random_req(data['subj']),
                                 reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                     InlineKeyboardButton(text="Сохранить в базу", callback_data="save__")))
    await state.finish()
    await message.answer("Сделано, жду команд!")


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
        await bot.send_animation(message.from_user.id, translate_req(data['phrase']),
                                 reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                     InlineKeyboardButton(text="Сохранить в базу", callback_data="save__")))
    await state.finish()
    await message.answer("Сделано, жду команд!")


# trendAPI_________________________________________________________________

@dp.message_handler(Text(equals="Популярные гифки"))
async def trand_api(message: types.Message):
    await message.answer("Минутку, произвожу поиск...")
    global gifs
    gifs.clear()
    gifs = trend_req()
    for item in gifs.items():
        await bot.send_animation(message.from_user.id, item[1],
                                 reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                     InlineKeyboardButton(text="Сохранить в базу", callback_data="save__")))
    await message.answer("Сделано, жду команд!")


@dp.callback_query_handler(Text(startswith="save_"))
async def colaback_hendler(collback: types.CallbackQuery):
    res = collback.data.split("_")[1]
    # dbase.save_gif(gifs[res])
    print(gifs[res])
    await collback.answer("Изображение сохранено!")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(category_handler, Text(equals="Популярные категории", ignore_case=True), state=None)
    dp.register_callback_query_handler(colaback_hendler_show_list_category, Text(startswith="category__"), state=None)
    dp.register_callback_query_handler(colaback_hendler_collect_category, Text(startswith="collect_cat__"), state=None)

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
