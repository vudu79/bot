from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


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
