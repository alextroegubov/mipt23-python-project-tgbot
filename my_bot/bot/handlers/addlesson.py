from bot.main_bot import bot
from bot.models import User, LessonRecord

from telebot import types
from telebot.types import InlineKeyboardButton

from typing import Dict

from bot.utils import date_validator, date_str_to_django, date_django_to_str
from bot.utils import get_yes_no_inline_keyboard

comment_prefix = 'comment_addlesson_inline_keyboard_'
confirm_prefix = 'confirm_addlesson_inline_keyabord_'

g_input_user_data: Dict[int, LessonRecord] = {}

def act_on_addlesson_command(u_id):

    if not User.objects.filter(external_id=u_id):
        text = "Please, register first. /reg"
        bot.send_message(u_id, text=text)
        return

    user = User.objects.get(external_id=u_id)
    text = "Let's record new lesson. Enter the date of the lesson (dd.mm.yyyy):"
    msg = bot.send_message(u_id, text=text)

    global g_input_user_data
    g_input_user_data[u_id] = LessonRecord(user=user)

    bot.register_next_step_handler(
        msg, 
        callback=get_date
    )

def get_date(message: types.Message):

    u_id = message.from_user.id
    global g_input_user_data
    assert u_id in g_input_user_data

    entered_date = message.text

    # validation of entered data
    if not date_validator(entered_date):
        text = f"Wrong data format: {entered_date}. Should be dd.mm.yyyy. Try again:"

        bot.send_message(u_id, text=text)
        bot.register_next_step_handler(
            message, 
            callback=get_date
        )
        return

    text = f"Fine, the date is {entered_date}. Enter duration in minutes:"
    bot.send_message(u_id, text=text)
    g_input_user_data[u_id].date = date_str_to_django(entered_date)

    bot.register_next_step_handler(
        message,
        callback=get_duration
    )


def get_duration(message: types.Message):
    u_id = message.from_user.id
    global g_input_user_data
    assert u_id in g_input_user_data
    g_input_user_data[u_id].duration = message.text

    yes_text = 'Yes, of course'
    no_text = 'No, thanks'
    kb = get_yes_no_inline_keyboard(comment_prefix, yes_text, no_text)

    text = f"Fine, the duration is {message.text} minutes. Any comments?"

    bot.send_message(u_id, text=text, reply_markup=kb, parse_mode='HTML')

def callback_on_comment(call: types.CallbackQuery) -> None:
    assert call.data.startswith(comment_prefix)

    u_id = call.message.chat.id
    answer = call.data[len(comment_prefix):]

    if answer == 'yes':
        msg = bot.send_message(u_id, text="Enter your comment then:")
        bot.register_next_step_handler(
            msg,
            callback=get_lesson_record_comment
        )

    elif answer == 'no':
        msg = bot.send_message(u_id, text="Ok")
        confirm_add_lesson(u_id)

    else:
        bot.send_message(u_id, text='smth wrong')

def get_lesson_record_comment(message: types.Message):
    u_id = message.from_user.id

    global g_input_user_data
    assert u_id in g_input_user_data
    g_input_user_data[u_id].comment = message.text
    confirm_add_lesson(u_id)

def confirm_add_lesson(u_id: int) -> None:

    yes_text = "Yes, that's right"
    no_text = "No, that's wrong"
    kb = get_yes_no_inline_keyboard(confirm_prefix, yes_text, no_text)

    global g_input_user_data
    assert u_id in g_input_user_data
    lesson = g_input_user_data[u_id]

    text = ("Got it. Is everything alright? "
           f"{lesson.duration} minutes lesson at {date_django_to_str(lesson.date)}"
           f"({lesson.comment})")

    bot.send_message(u_id, text=text, reply_markup=kb)


def callback_on_cofirm_add_lesson(call: types.CallbackQuery):
    assert call.data.startswith(confirm_prefix)

    u_id = call.message.chat.id
    answer = call.data[len(confirm_prefix):]

    global g_input_user_data
    assert u_id in g_input_user_data

    if answer == 'yes':
        g_input_user_data[u_id].save()
        text = f"Great! Lesson is added."

    elif answer == 'no':
        text = f"Sorry... Let's try again. /addlesson"

    # remove tmp input data
    g_input_user_data.pop(u_id)

    bot.send_message(
        u_id, 
        text=text
    )

def register_handler_addlesson():
    bot.register_message_handler(commands=['addlesson'], callback=act_on_addlesson_command)
    bot.register_callback_query_handler(callback=callback_on_cofirm_add_lesson, func=lambda call: call.data.startswith(confirm_prefix))
    bot.register_callback_query_handler(callback=callback_on_comment, func=lambda call: call.data.startswith(comment_prefix))