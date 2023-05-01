""" Validators, common keyboards"""

from datetime import datetime
from telebot import types  # type: ignore


def date_validator(data_text: str) -> bool:
    """ Validate date"""
    try:
        datetime.strptime(data_text, '%d.%m.%Y')
    except ValueError:
        return False

    return True


def date_str_to_django(data_text: str) -> str:
    """Convert str to django str"""

    assert date_validator(data_text)
    date = datetime.strptime(data_text, '%d.%m.%Y')

    return date.strftime('%Y-%m-%d %H:%M')


def date_django_to_str(date: str) -> str:
    """Convert django str to user str"""
    return datetime.strptime(date, '%Y-%m-%d %H:%M').strftime('%d-%m-%Y')


def int_validator(text: str) -> bool:
    """ Validate int number"""
    return text.isdecimal() and (int(text) < 24*60)


def word_validator(text: str) -> bool:
    """ Validate word"""
    return text.isalnum() and (len(text) < 100)


def get_yes_no_inline_keyboard(prefix: str, yes_text: str, no_text: str
                               ) -> types.ReplyKeyboardMarkup:
    """ Keyboard creator"""
    ikbm = types.InlineKeyboardMarkup()

    ikbm.add(
        types.InlineKeyboardButton(
            text=yes_text,
            callback_data=prefix + 'yes'
        ),
        types.InlineKeyboardButton(
            text=no_text,
            callback_data=prefix + 'no'
        )
    )

    return ikbm


START_MENU_PREFIX = "start_menu_keyboard_"
START_TEXT = "Давай продолжим изучать английский 🧠"


def start_menu() -> types.InlineKeyboardMarkup:
    """Start menu keyboard"""
    ikbm = types.InlineKeyboardMarkup(row_width=1)

    ikbm.add(
        types.InlineKeyboardButton(
            text='Добавить новое слово',
            callback_data=START_MENU_PREFIX + 'addword'
        ),
        types.InlineKeyboardButton(
            text='Записать урок',
            callback_data=START_MENU_PREFIX + 'addlesson'
        ),
        types.InlineKeyboardButton(
            text='Повторять слова',
            callback_data=START_MENU_PREFIX + 'game'
        ),
        types.InlineKeyboardButton(
            text='Статистика',
            callback_data=START_MENU_PREFIX + 'stat'
        )
    )

    return ikbm
