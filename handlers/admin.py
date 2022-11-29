import asyncio
import random
import re
import shutil
import time
from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import RetryAfter

from utils import *
from create_bot import dp, bot, calendar_dict, calendar_storage, stickers_list, stickers_dict
from client.http_client import *
from database import DBase
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards import reply_keyboard_main_menu, inline_keyboard_lang, reply_keyboard_cards, reply_keyboard_gifs, \
    reply_keyboard_mems, reply_keyboard_stickers


class FSMSearch(StatesGroup):
    subj = State()
    limit = State()


class FSMStickersRandom(StatesGroup):
    count = State()


class FSMStickersSearch(StatesGroup):
    word = State()
    count = State()


gifs = dict()
dbase = DBase()
storage = MemoryStorage()
leng_type = ""
leng_phrase = ""

categories_callback = CallbackData("CategorY__", "page", "category_name")

category_list = get_categories_tenor_req()


@dp.message_handler(Text(equals="Мемы", ignore_case=False), state=None)
async def mems_menu_show_handler(message: types.Message):
    # await bot.send_message(message.from_user.id,
    #                        "Более 10000 открыток на праздники!!!",
    #                        reply_markup=InlineKeyboardMarkup(row_width=2).row(
    #                            InlineKeyboardButton(text="Сегодня", callback_data="holiday__today_"),
    #                            InlineKeyboardButton(text="Календарь", callback_data="holiday__calendar_")))
    # await message.delete_reply_markup()
    await bot.send_message(message.from_user.id,
                           "Неприлично много мемов))",
                           reply_markup=reply_keyboard_mems)


@dp.message_handler(Text(equals="Гифки", ignore_case=False), state=None)
async def gifs_menu_show_handler(message: types.Message):
    # await bot.send_message(message.from_user.id,
    #                        "Более 10000 открыток на праздники!!!",
    #                        reply_markup=InlineKeyboardMarkup(row_width=2).row(
    #                            InlineKeyboardButton(text="Сегодня", callback_data="holiday__today_"),
    #                            InlineKeyboardButton(text="Календарь", callback_data="holiday__calendar_")))
    # await message.delete_reply_markup()
    await bot.send_message(message.from_user.id,
                           "Помогу найти гифки рызными способами))",
                           reply_markup=reply_keyboard_gifs)


@dp.message_handler(Text(equals="Открытки", ignore_case=False), state=None)
async def cards_menu_show_handler(message: types.Message):
    # await bot.send_message(message.from_user.id,
    #                        "Более 10000 открыток на праздники!!!",
    #                        reply_markup=InlineKeyboardMarkup(row_width=2).row(
    #                            InlineKeyboardButton(text="Сегодня", callback_data="holiday__today_"),
    #                            InlineKeyboardButton(text="Календарь", callback_data="holiday__calendar_")))
    # await message.delete_reply_markup()
    await bot.send_message(message.from_user.id,
                           "Более 10000 открыток на праздники!!!",
                           reply_markup=reply_keyboard_cards)


@dp.message_handler(Text(equals="Стикеры", ignore_case=False), state=None)
async def stickers_menu_show_handler(message: types.Message):
    # await bot.send_message(message.from_user.id,
    #                        "Более 10000 открыток на праздники!!!",
    #                        reply_markup=InlineKeyboardMarkup(row_width=2).row(
    #                            InlineKeyboardButton(text="Сегодня", callback_data="holiday__today_"),
    #                            InlineKeyboardButton(text="Календарь", callback_data="holiday__calendar_")))
    # await message.delete_reply_markup()
    await bot.send_message(message.from_user.id,
                           "Более 25000 стикер-паков!!! Найти бы только нужный((",
                           reply_markup=reply_keyboard_stickers)


@dp.message_handler(Text(equals="Случайные паки", ignore_case=False), state=None)
async def stickers_random_handler(message: types.Message):
    await message.answer("Сколько паков найти?")
    await FSMStickersRandom.count.set()


@dp.message_handler(Text(equals="Может найду...", ignore_case=False), state=None)
async def stickers_search_handler(message: types.Message):
    await message.answer("Введите слово или фразу для поиска (ru/en)...")
    await FSMStickersSearch.word.set()


@dp.message_handler(state=FSMStickersSearch.word)
async def load_word_search_stickers(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['word'] = message.text
        stickers_names = stickers_dict.keys()
        matches_list = list(filter(lambda x: data['word'] in x, stickers_names))
        await bot.send_message(message.from_user.id, f'{matches_list}')
        if len(matches_list) > 0:

            for name in matches_list:
                bold_name = name[:name.index(data['word'])] + \
                            "<b>" + data['word'].upper() + "</b>" \
                            + name[name.index(data['word'])
                                   + len(data['word']):]

                media = types.MediaGroup()
                img_list = stickers_dict[name]["stickers"]

                if len(img_list) <= 4:
                    for img in img_list:
                        media.attach_photo(types.InputMediaPhoto(img))
                else:
                    for x in range(0, 3):
                        media.attach_photo(types.InputMediaPhoto(img_list[x]))

                try:
                    if len(media.media) > 0:
                        print(f'Медиа группа - {len(media.media)} ')

                        await bot.send_media_group(message.from_user.id, media=media)
                        await bot.send_message(message.from_user.id, f'{bold_name}',
                                               parse_mode="HTML",
                                               reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(
                                                   text="Подробней / Добавить в телеграм",
                                                   url=f'{stickers_dict[name]["url"]}')))

                except Exception as ee:
                    print(f"Что то пошло не так {ee}")
                    with open("static/bad_pack1.txt", 'a') as file:
                        file.write(name)

        else:
            await bot.send_message(message.from_user.id, "По вашему запросу ничего не найдено")
    await state.finish()


@dp.message_handler(state=FSMStickersRandom.count)
async def load_count_random_stickers(message: types.Message, state: FSMContext):
    num_string = message.text
    if not (num_string.isnumeric() and num_string.isdigit() and re.match("[-+]?\d+$", num_string)):
        await bot.send_message(message.from_user.id, "Введите целое число")
    else:
        packs_count = int(num_string)
        async with state.proxy() as data:
            data['count'] = packs_count

            count = 0
            await message.answer(f'Ок, работаю...')
            while count < packs_count:
                random_sticker_dict = random.choice(stickers_list)
                img_list = random_sticker_dict["stickers"]

                media = types.MediaGroup()
                if len(img_list) <= 6:
                    for img in img_list:
                        media.attach_photo(types.InputMediaPhoto(img))
                else:
                    for x in range(0, 5):
                        media.attach_photo(types.InputMediaPhoto(img_list[x]))

                try:
                    if len(media.media) > 0:
                        print(f'Медиа группа - {len(media.media)} ')

                        await bot.send_message(message.from_user.id, f'<em>{random.choice(phraze_list)}</em>',
                                               parse_mode="HTML")

                        await bot.send_media_group(message.from_user.id, media=media)
                        await bot.send_message(message.from_user.id, f'Стикеры <b>"{random_sticker_dict["name"]}"</b>',
                                               parse_mode="HTML",
                                               reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(
                                                   text="Добавить в телеграм", url=f'{random_sticker_dict["url"]}')))
                        count = count + 1
                except Exception as ee:
                    print(f"Что то пошло не так {ee}")
                    with open("static/bad_pack.txt", 'a') as file:
                        file.write(random_sticker_dict["name"])
            # await bot.send_message(message.from_user.id, "Что то пошло не так...")

        await state.finish()


@dp.message_handler(Text(equals="Может найду...", ignore_case=False))
async def stickers_search_handler(message: types.Message):
    pass


@dp.message_handler(Text(equals="Календарь", ignore_case=False), state=None)
async def carendar_holiday_message_handler(message: types.Message):
    inline_keyboard_holiday = InlineKeyboardMarkup(row_width=3)
    for month in calendar_dict.keys():
        inline_keyboard_holiday.clean()
        inline_keyboard_holiday.insert(
            InlineKeyboardButton(text=f'{month}', callback_data=f'month__{month}'))

    await bot.send_message(message.from_user.id,
                           'Выберите месяц...',
                           reply_markup=inline_keyboard_holiday)


@dp.message_handler(Text(equals="Календарь", ignore_case=False), state=None)
async def carendar_holiday_message_handler(message: types.Message):
    inline_keyboard_holiday = InlineKeyboardMarkup(row_width=3)
    for month in calendar_dict.keys():
        inline_keyboard_holiday.clean()
        inline_keyboard_holiday.insert(
            InlineKeyboardButton(text=f'{month}', callback_data=f'month__{month}'))

    await bot.send_message(message.from_user.id,
                           'Выберите месяц...',
                           reply_markup=inline_keyboard_holiday)


@dp.message_handler(Text(equals="Сегодня", ignore_case=False), state=None)
async def today_holiday_message_handler(message: types.Message):
    inline_keyboard_today_events = InlineKeyboardMarkup(row_width=1)

    today = datetime.today().strftime("%-d.%m")
    count = 0
    for month in calendar_dict.keys():
        event_list = calendar_dict[month].keys()
        for event in event_list:
            if event.startswith(today):
                count = count + 1
                inline_keyboard_today_events.clean()
                inline_keyboard_today_events.insert(
                    InlineKeyboardButton(text=f'{event}', callback_data=f'&ev_{month}_{str(hash(event))}'))

    if count > 0:
        await bot.send_message(message.from_user.id,
                               'Выберите праздник.',
                               reply_markup=inline_keyboard_today_events)
    else:
        await bot.send_message(message.from_user.id,
                               'На сегодня ничего не нашел ((')


@dp.callback_query_handler(Text(startswith="month__"), state=None)
async def show_month_events_callback_handler(collback: types.CallbackQuery):
    callback_user_id = collback.from_user.id
    month = collback.data.split("__")[1]
    events_list = calendar_dict[month].keys()

    inline_keyboard_events = InlineKeyboardMarkup(row_width=1)
    for event in events_list:
        inline_keyboard_events.clean()
        inline_keyboard_events.insert(
            InlineKeyboardButton(text=f'{event}', callback_data=f'&ev_{month}_{str(hash(event))}'))

    await bot.send_message(callback_user_id,
                           'Выберите месяц...',
                           reply_markup=inline_keyboard_events)
    await collback.answer()


def func_chunk(lst, n):
    for x in range(0, len(lst), n):
        e_c = lst[x: n + x]

        if len(e_c) < n:
            e_c = e_c + ["" for y in range(n - len(e_c))]
        yield e_c


@dp.callback_query_handler(Text(startswith="&ev_"), state=None)
async def show_event_images_colaback_hendler(collback: types.CallbackQuery):
    # phraze_list = ["Склеиваю открытки...", "Ищу в интернетах...)", "Собираю пазл...",
    #                "Вспоминаю, что надо было сделать...", "Выгружаю по частям...", "Устал, у меня перерыв..."]
    callback_user_id = collback.from_user.id
    month = collback.data.split("_")[1]
    event_hash = collback.data.split("_")[2]

    # events_list = calendar_storage[month].keys()
    events_list = calendar_dict[month].keys()
    img_list = list()
    holiday = "???"

    for event in events_list:
        if event_hash == str(hash(event)):
            img_list = calendar_dict[month][event]
            holiday = event

    print(f'img_list - {img_list}')

    is_more_ten = bool

    len_img_list = len(img_list)
    print(f'len_img_list - {len_img_list}')
    len_generator = 0

    if len_img_list > 0:
        if len_img_list > 10:
            len_generator = (len_img_list // 10) + (0 if (len_img_list % 10) == 0 else 1)
            print(f'len_generator - {len_generator}')
            image_generator = func_chunk(img_list, 10)
            print(f'image_generator - {image_generator}')
            is_more_ten = True
        else:
            image_generator = (x for x in img_list)
            is_more_ten = False

        await bot.send_message(callback_user_id,
                               f'Выбран праздник "{holiday.split("-")[1]}". Найдено {len_img_list} шт.')

        if is_more_ten:
            for x in range(len_generator):
                step_list = next(image_generator)
                await bot.send_message(callback_user_id,
                                       f'{random.choice(phraze_list) if len_img_list > 10 else "Минутку, подбираю открытки..."}')
                media = types.MediaGroup()
                for img in step_list:
                    if img != "":
                        media.attach_photo(types.InputMediaPhoto(img), f'{holiday.split("-")[1]}')

                try:
                    await bot.send_media_group(callback_user_id, media=media)
                except RetryAfter as e:
                    await asyncio.sleep(e.timeout)
                except Exception as ee:
                    print(f'Что то пошло не так - {ee}')

        else:
            media = types.MediaGroup()
            for img in image_generator:
                media.attach_photo(types.InputMediaPhoto(img), f'{holiday.split("-")[1]}')

            try:
                await bot.send_media_group(callback_user_id, media=media)
            except RetryAfter as e:
                await asyncio.sleep(e.timeout)
            except Exception as ee:
                print(f'Что то пошло не так - {ee}')

        await collback.answer()

    await collback.answer("К сожалению, для этого праздника открыток нет.")


@dp.message_handler(Text(equals="Популярные категории", ignore_case=False), state=None)
async def category_index_handler(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "Показать все категории или по одной, но с превью?",
                           reply_markup=InlineKeyboardMarkup(row_width=2).row(
                               InlineKeyboardButton(text="Все сразу", callback_data="collect_cat__yes"),
                               InlineKeyboardButton(text="По одной", callback_data="collect_cat__no")))


@dp.callback_query_handler(Text(startswith="collect_cat__"), state=None)
async def show_type_category_callback_handler(collback: types.CallbackQuery):
    callback_user_id = collback.from_user.id
    res = collback.data.split("__")[1]
    if res == "yes":
        inline_keyboard_category = InlineKeyboardMarkup(row_width=3)
        for teg in category_list:
            inline_keyboard_category.clean()
            inline_keyboard_category.insert(
                InlineKeyboardButton(text=f'{teg["searchterm"]}', callback_data=f'category__{teg["searchterm"]}'))

        await bot.send_message(callback_user_id,
                               'В каждой категории по несколько вариантов популярных гифок. Нажмите на любую для просмотра.',
                               reply_markup=inline_keyboard_category)
        await collback.answer()
    else:
        if res == "no":
            category_one = category_list[0]
            keyboard = get_pagination_keyboard(category_list=category_list,
                                               categories_callback=categories_callback)  # Page: 0

            await bot.send_animation(
                chat_id=callback_user_id,
                animation=category_one["image"],
                reply_markup=keyboard
            )


@dp.callback_query_handler(categories_callback.filter())
async def paginate_category_callback_handler(query: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    category_one = category_list[page]
    keyboard = get_pagination_keyboard(page=page, category_list=category_list, categories_callback=categories_callback)

    await bot.send_animation(
        chat_id=query.from_user.id,
        animation=category_one["image"],
        reply_markup=keyboard
    )


@dp.callback_query_handler(Text(startswith="category__"), state=None)
async def show_list_category_colaback_hendler(collback: types.CallbackQuery):
    callback_user_id = collback.from_user.id
    res = collback.data.split("__")[1]
    await collback.answer(f'Выбрана категория {res}')
    gifs_from_tenor_list = get_category_list_tenor_req(res)
    for gif in gifs_from_tenor_list:
        try:
            await bot.send_animation(callback_user_id, gif, reply_markup=InlineKeyboardMarkup(row_width=1).add(
                InlineKeyboardButton(text="Сохранить в базу", callback_data="save__")))
        except RetryAfter as e:
            await asyncio.sleep(e.timeout)
    await collback.answer()


# Машина состояний для searchAPI________________________________________________________________________________________
# Запускаем машину состояния FSMAdmin хэндлером

@dp.message_handler(Text(equals="Найти по слову", ignore_case=False))
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
@dp.message_handler(Text(equals=['отмена', 'Отменить поиск'], ignore_case=False), state="*")
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


@dp.message_handler(Text(equals="Случайная по слову", ignore_case=False), state=None)
async def cm_start_random(message: types.Message):
    await FSMRandom.subj.set()
    await message.answer("Напишите ключевое слово для поиска на английском языке")


@dp.message_handler(state="*", commands='отмена')
@dp.message_handler(Text(equals=['отмена', 'Отменить поиск'], ignore_case=False), state="*")
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


@dp.message_handler(Text(equals="Гифка под фразу", ignore_case=False), state=None)
async def cm_start_translate(message: types.Message):
    await FSMTranslate.phrase.set()
    await message.answer("Напишите любую фразу на английском языке")


@dp.message_handler(state="*", commands='отмена')
@dp.message_handler(Text(equals=['отмена', 'Отменить поиск'], ignore_case=False), state="*")
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
    # print(gifs[res])
    await collback.answer("В разработке...")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(mems_menu_show_handler, Text(equals="Мемы", ignore_case=False))
    dp.register_message_handler(gifs_menu_show_handler, Text(equals="Гифки", ignore_case=False))
    dp.register_message_handler(cards_menu_show_handler, Text(equals="Открытки", ignore_case=False))
    dp.register_message_handler(stickers_menu_show_handler, Text(equals="Стикеры", ignore_case=False))

    dp.register_message_handler(stickers_random_handler, Text(equals="Случайные паки", ignore_case=False))
    dp.register_message_handler(stickers_search_handler, Text(equals="Может найду...", ignore_case=False))

    dp.register_message_handler(category_index_handler, Text(equals="Популярные категории", ignore_case=False))

    dp.register_callback_query_handler(carendar_holiday_message_handler, Text(equals="Календарь", ignore_case=False))
    dp.register_callback_query_handler(today_holiday_message_handler, Text(equals="Сегодня", ignore_case=False))

    dp.register_callback_query_handler(show_month_events_callback_handler, Text(startswith="month__"), state=None)

    dp.register_callback_query_handler(show_event_images_colaback_hendler, Text(startswith="&ev_"), state=None)

    dp.register_callback_query_handler(show_type_category_callback_handler, Text(startswith="collect_cat__"),
                                       state=None)

    dp.register_callback_query_handler(paginate_category_callback_handler, categories_callback.filter())
    dp.register_callback_query_handler(show_list_category_colaback_hendler, Text(startswith="category__"), state=None)

    dp.register_message_handler(choose_lang_handler, Text(equals="Найти по слову", ignore_case=False))
    dp.register_callback_query_handler(colaback_hendler_lang_start_search, Text(startswith="leng__"), state=None)
    dp.register_message_handler(cansel_state_search, state="*", commands='отмена')
    dp.register_message_handler(load_subj_sm_search, state=FSMSearch.subj)
    dp.register_message_handler(load_limit_sm_search, state=FSMSearch.limit)

    dp.register_message_handler(cm_start_random, Text(equals="Случайная по слову", ignore_case=False), state=None)
    dp.register_message_handler(cansel_state_random, state="*", commands='отмена')
    dp.register_message_handler(load_subj_sm_random, state=FSMRandom.subj)

    dp.register_message_handler(cm_start_translate, Text(equals="Гифка под фразу", ignore_case=False), state=None)
    dp.register_message_handler(cansel_state_translate, state="*", commands='отмена')
    dp.register_message_handler(load_subj_sm_translate, state=FSMTranslate.phrase)

    dp.register_message_handler(trand_api, Text(equals="Популярные гифки"))
