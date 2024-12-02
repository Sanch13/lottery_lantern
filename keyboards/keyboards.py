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


def get_inline_keyboard_check_user_state() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Проверка подписки",
                                 callback_data="check_user_state"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_inline_keyboard_get_number_of_ticket() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Получить номер",
                                 callback_data="get_number_of_ticket"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_inline_keyboard_link_to_bot_registration() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Регистрация в Telegram-MIRAN",
                                 url="https://t.me/reg_user_miran_chat_bot"),
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
