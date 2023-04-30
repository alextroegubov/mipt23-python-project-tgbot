from bot.main_bot import bot
from bot.models import User, WordRecord

from telebot import types
from functools import partial
from typing import Dict

comment_prefix = 'comment_inline_keyboard_'
confirm_prefix = 'confirm_inline_keyabord_'

g_input_user_data: Dict[int, WordRecord] = {}

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

def act_on_addword_command(message: types.Message) -> None:
    """ Primary handler for /addword command"""
    u_id = message.from_user.id

    if not User.objects.filter(external_id=u_id):
        text = "Please, register first. /reg"
        bot.send_message(u_id, text=text)
        return

    user = User.objects.get(external_id=u_id)

    text = "Let's fill your dictionary🧐 Enter new word:"
    bot.send_message(u_id, text=text)

    global g_input_user_data
    g_input_user_data[u_id] = WordRecord(user=user)

    bot.register_next_step_handler(
        message, 
        callback=get_word_record_en_word
    )

def get_word_record_en_word(message: types.Message) -> None:
    u_id = message.from_user.id

    global g_input_user_data
    assert u_id in g_input_user_data
    g_input_user_data[u_id].en_word = message.text

    text = f"Fine, <i>{message.text}</i> is writen👌 Enter translation:"

    bot.send_message(u_id, text=text)

    bot.register_next_step_handler(
        message, 
        callback=get_word_record_ru_translation
    )

def get_word_record_ru_translation(message: types.Message) -> None:
    u_id = message.from_user.id

    global g_input_user_data
    assert u_id in g_input_user_data
    g_input_user_data[u_id].ru_translation = message.text

    yes_text = 'Yes, of course'
    no_text = 'No, thanks'
    kb = get_yes_no_inline_keyboard(comment_prefix, yes_text, no_text)

    text = f"Fine, <i>{message.text}</i> is tranlation. Any additional comments?"

    bot.send_message(u_id, text=text, reply_markup=kb, parse_mode='HTML')

def callback_on_comment(call: types.CallbackQuery) -> None:
    assert call.data.startswith(comment_prefix)

    u_id = call.message.chat.id
    answer = call.data[len(comment_prefix):]

    if answer == 'yes':
        msg = bot.send_message(u_id, text="Enter your comment then:")
        bot.register_next_step_handler(
            msg,
            callback=get_word_record_comment
        )

    elif answer == 'no':
        msg = bot.send_message(u_id, text="Ok")
        confirm_add_word(u_id)

    else:
        bot.send_message(u_id, text='smth wrong')

def get_word_record_comment(message: types.Message) -> None:
    u_id = message.from_user.id

    global g_input_user_data
    assert u_id in g_input_user_data
    g_input_user_data[u_id].comment = message.text
    confirm_add_word(u_id)


def confirm_add_word(u_id: int) -> None:

    yes_text = "Yes, that's right"
    no_text = "No, that's wrong"
    kb = get_yes_no_inline_keyboard(confirm_prefix, yes_text, no_text)

    global g_input_user_data
    assert u_id in g_input_user_data
    word = g_input_user_data[u_id]

    text = f"Got it. Is everything alright?\
           {word.en_word} = {word.ru_translation} ({word.comment})"

    bot.send_message(u_id, text=text, reply_markup=kb)


def callback_on_cofirm_add_word(call: types.CallbackQuery):
    assert call.data.startswith(confirm_prefix)

    u_id = call.message.chat.id
    answer = call.data[len(confirm_prefix):]

    global g_input_user_data
    assert u_id in g_input_user_data

    if answer == 'yes':
        g_input_user_data[u_id].save()
        text = f"Great! {g_input_user_data[u_id].en_word} is added to your dictionary."
    elif answer == 'no':
        text = f"Sorry... Let's try again."

    bot.send_message(
        u_id, 
        text=text
    )

def register_handler_addword():
    bot.register_message_handler(commands=['addword'], callback=act_on_addword_command)
    bot.register_callback_query_handler(callback=callback_on_cofirm_add_word, func=lambda call: call.data.startswith(confirm_prefix))
    bot.register_callback_query_handler(callback=callback_on_comment, func=lambda call: call.data.startswith(comment_prefix))