from bot.main_bot import bot
from bot.models import User, WordRecord

from telebot import types
from telebot.types import InlineKeyboardButton

from functools import partial

def act_on_addword_command(message: types.Message):
    u_id = message.from_user.id

    if not User.objects.filter(external_id=u_id):
        text = "Please, register first. \\reg"
        bot.send_message(u_id, text=text)
        return

    user = User.objects.get(external_id=u_id)
    text = "Let's fill your dictionary. Enter new word:"
    bot.send_message(u_id, text=text)

    word_record = WordRecord(user=user)
    bot.register_next_step_handler(
        message, 
        callback=partial(get_word_record_en_word, word_record)
    )

def get_word_record_en_word(word_record: WordRecord, message: types.Message):
    word_record.en_word = message.text
    u_id = message.from_user.id
    text = f"Fine, {message.text} is writen. Enter translation:"

    bot.send_message(u_id, text=text)

    bot.register_next_step_handler(
        message, 
        callback=partial(get_word_record_ru_translation, word_record)
    )

def get_word_record_ru_translation(word_record: WordRecord, message: types.Message):
    word_record.ru_translation = message.text
    u_id = message.from_user.id
    text = f"Fine, {message.text} is tranlation. Any comments?"

    bot.send_message(u_id, text=text)
    bot.register_next_step_handler(
        message, 
        callback=partial(get_word_record_comment, word_record)
    )

def get_word_record_comment(word_record: WordRecord, message: types.Message):
    word_record.comment = message.text

    # kb = types.InlineKeyboardMarkup()
    # kb.add(
    #     InlineKeyboardButton(text='Yes', callback_data='yes_add_word'),
    #     InlineKeyboardButton(text='No', callback_data='no_add_word')
    # )

    rkm = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('yes')
    btn2 = types.KeyboardButton('no')
    rkm.add(btn1, btn2)

    text = f"Got it. Is everything alright?\
           {word_record.en_word} = {word_record.ru_translation} ({word_record.comment})"

    msg = bot.send_message(message.from_user.id, text=text, reply_markup=rkm)

    bot.register_next_step_handler(
        msg,
        callback=partial(word_record_confirm, word_record)
    )


def word_record_confirm(word_record, message):

    if message.text == 'yes':
        word_record.save()
        text = f"Great! {word_record.en_word} is added to your dictionary."
    elif message.text == 'no':
        text = f"Sorry... Let's try again."

    bot.send_message(
        message.from_user.id, 
        text=text,
        reply_markup=types.ReplyKeyboardRemove()
    )

def register_handler_addword():
    bot.register_message_handler(commands=['addword'], callback=act_on_addword_command)
    #bot.register_callback_query_handler(callback=word_record_confirm, func=lambda call: call.data == )