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