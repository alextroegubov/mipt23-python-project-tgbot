from datetime import datetime
from telebot import types


def date_validator(data_text):
    try:
        datetime.strptime(data_text, '%d.%m.%Y')
    except ValueError:
        return False

    return True


def date_str_to_django(data_text):

    assert date_validator(data_text)
    d = datetime.strptime(data_text, '%d.%m.%Y')

    return d.strftime('%Y-%m-%d %H:%M')


def date_django_to_str(date):
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


start_menu_prefix = "start_menu_keyboard_"
start_text = "Давай продолжим изучать английский 🧠"

def start_menu() -> types.InlineKeyboardMarkup:
    """Start menu keyboard"""
    ikbm = types.InlineKeyboardMarkup(row_width=1)

    ikbm.add(
        types.InlineKeyboardButton(
            text='Добавить новое слово',
            callback_data=start_menu_prefix + 'addword'
        ),
        types.InlineKeyboardButton(
            text='Записать урок',
            callback_data=start_menu_prefix + 'addlesson'
        ),
        types.InlineKeyboardButton(
            text='Повторять слова',
            callback_data=start_menu_prefix + 'game'
        ),
        types.InlineKeyboardButton(
            text='Статистика',
            callback_data=start_menu_prefix + 'stat'
        )
    )

    return ikbm
