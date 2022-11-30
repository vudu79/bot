import json
import random

from aiogram import types

from create_bot import stickers_list
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

phraze_list = ["Секундочку, склеиваю фотки...", "минутку, ищу в интернетах...)", "Подождите, собираю пазл...",
               "Надо подождать, вспоминаю, что надо было сделать...", "Подождите,выгружаю по частям...",
               "Приходите попозже, устал, у меня перерыв...", "Минутку подождите, я форматирую ваши диски))"]





# def get_stickers(count: int, massage: types.Message, img_list: list):
#     media = types.MediaGroup()
#     if len(img_list) <= 6:
#         for img in img_list:
#             media.attach_photo(types.InputMediaPhoto(img))
#     else:
#         for x in range(0, 5):
#             media.attach_photo(types.InputMediaPhoto(img_list[x]))
#
#     try:
#         if len(media.media) > 0:
#             print(f'Медиа группа - {len(media.media)} ')
#
#             await bot.send_message(message.from_user.id, f'<em>{random.choice(phraze_list)}</em>',
#                                    parse_mode="HTML")
#
#             await bot.send_media_group(message.from_user.id, media=media)
#             await bot.send_message(message.from_user.id, f'Стикеры <b>"{random_sticker_dict["name"]}"</b>',
#                                    parse_mode="HTML",
#                                    reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(
#                                        text="Добавить в телеграм", url=f'{random_sticker_dict["url"]}')))
#             count = count + 1
#     except Exception as ee:
#         print(f"Что то пошло не так {ee}")
#         with open("static/bad_pack.txt", 'a') as file:
#             file.write(random_sticker_dict["name"])
#

# await bot.send_message(message.from_user.id, "Что то пошло не так...")


def get_pagination_keyboard(page: int = 0, category_list: any = None,
                            categories_callback: CallbackData = None) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    has_next_page = len(category_list) > page + 1

    if page != 0:
        keyboard.add(
            InlineKeyboardButton(
                text="👈",
                callback_data=categories_callback.new(page=page - 1,
                                                      category_name=f'{category_list[page - 1]["searchterm"]}')
            )
        )

    keyboard.add(
        InlineKeyboardButton(
            text=f'Показать все из "{str.capitalize(category_list[page]["searchterm"])}"',
            callback_data=f'category__{category_list[page]["searchterm"]}"'
        )
    )

    if has_next_page:
        keyboard.add(
            InlineKeyboardButton(
                text="👉",
                callback_data=categories_callback.new(page=page + 1,
                                                      category_name=f'{category_list[page + 1]["searchterm"]}')
            )
        )

    return keyboard


def get_pagination_list(packs_count: int):
    res_list = list()
    count = packs_count % 50
    # print(count)
    last= 0
    if count > 0:
        for x in range(1, packs_count - 49, 50):
            last = x + 49
            res_list.append((x, last))
        res_list.append((last + 1, last + count))
    else:
        for x in range(1, packs_count, 50):
            last = x + 49
            res_list.append((x, last))
    return res_list
