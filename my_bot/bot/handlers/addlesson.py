from bot.main_bot import bot
from bot.models import User, LessonRecord

from telebot import types
from telebot.types import InlineKeyboardButton

from functools import partial
from datetime import datetime


def act_on_addlesson_command(message: types.Message):
    u_id = message.from_user.id

    if not User.objects.filter(external_id=u_id):
        text = "Please, register first. /reg"
        bot.send_message(u_id, text=text)
        return

    user = User.objects.get(external_id=u_id)
    text = "Let's record new lesson. Enter the date of the lesson (dd.mm.yyyy):"
    bot.send_message(u_id, text=text)

    lesson_record = LessonRecord(user=user)
    bot.register_next_step_handler(
        message, 
        callback=partial(get_date, lesson_record)
    )

def data_validator(data_text):
    try:
        datetime.strptime(data_text, '%d.%m.%Y')
    except ValueError:
        return False

    return True

def data_str_to_django(data_text):

    assert data_validator(data_text)
    d = datetime.strptime(data_text, '%d.%m.%Y')

    return d.strftime('%Y-%m-%d %H:%M')

def get_date(lesson_record: LessonRecord, message: types.Message):

    u_id = message.from_user.id
    entered_date = message.text

    # validation of entered data
    if not data_validator(entered_date):
        text = f"Wrong data format: {entered_date}. Should be dd.mm.yyyy. Try again:"

        bot.send_message(u_id, text=text)
        bot.register_next_step_handler(
            message, 
            callback=partial(get_date, lesson_record)
        )
        return
    # data is ok
    text = f"Fine, the date is {entered_date}. Enter duration in minutes:"
    bot.send_message(u_id, text=text)
    lesson_record.date = data_str_to_django(entered_date)

    bot.register_next_step_handler(
        message, 
        callback=partial(get_duration, lesson_record)
    )

def get_duration(lesson_record: LessonRecord, message: types.Message):
    lesson_record.duration = message.text
    u_id = message.from_user.id
    text = f"Fine, the duration is {message.text} minutes. Any comments?"

    bot.send_message(u_id, text=text)
    bot.register_next_step_handler(
        message, 
        callback=partial(get_comment, lesson_record)
    )

def get_comment(lesson_record: LessonRecord, message: types.Message):
    lesson_record.comment = message.text

    rkm = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('yes')
    btn2 = types.KeyboardButton('no')
    rkm.add(btn1, btn2)

    text = ("Got it. Is everything alright? "
           f"{lesson_record.duration} minutes lesson at {lesson_record.date} ({lesson_record.comment})")

    msg = bot.send_message(message.from_user.id, text=text, reply_markup=rkm)

    bot.register_next_step_handler(
        msg,
        callback=partial(lesson_record_confirm, lesson_record)
    )


def lesson_record_confirm(lesson_record: LessonRecord, message: types.Message):

    if message.text == 'yes':
        lesson_record.save()
        text = f"Great! Lesson is added."
    elif message.text == 'no':
        text = f"Sorry... Let's try again. /addlesson"

    bot.send_message(
        message.from_user.id, 
        text=text,
        reply_markup=types.ReplyKeyboardRemove()
    )

def register_handler_addlesson():
    bot.register_message_handler(commands=['addlesson'], callback=act_on_addlesson_command)