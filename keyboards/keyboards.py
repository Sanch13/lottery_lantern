from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import settings


def get_inline_keyboard_enter_data() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Ввести данные",
                                 callback_data="waiting_for_consent"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_button_reg() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Регистрация",
                                 url=settings.CHANNEL_LINK_MIRAN),
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_inline_keyboard_yes_no() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Да", callback_data="yes"),
            InlineKeyboardButton(text="Нет", callback_data="no"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
