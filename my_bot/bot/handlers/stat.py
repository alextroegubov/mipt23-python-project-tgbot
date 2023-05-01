from bot.main_bot import bot
from bot.models import User, LessonRecord, WordRecord

from telebot import types
from telebot.types import InlineKeyboardButton

from functools import partial
from datetime import datetime, date, timedelta

stat_prefix = 'stat_inline_keyboard_'

def get_stat_inline_keyboard() -> types.ReplyKeyboardMarkup:
    ikbm = types.InlineKeyboardMarkup()

    ikbm.add(
        InlineKeyboardButton(
            text='Уроки за 30 дней',
            callback_data=stat_prefix + 'lessons_30_days'
        ),
        InlineKeyboardButton(
            text='Последниу 10 слов',
            callback_data=stat_prefix + 'recent_10_words'

        ),
        InlineKeyboardButton(
            text='Число слов за месяц',
            callback_data=stat_prefix + 'words_month'
        )
    )

    return ikbm

def act_on_stat_command(u_id: int) -> None:

    if not User.objects.filter(external_id=u_id):
        text = "Please, register first. /reg"
        bot.send_message(u_id, text=text)
        return

    text = "Let's look at your progress. Select:"
    ikbm = get_stat_inline_keyboard()

    bot.send_message(u_id, text=text, reply_markup=ikbm)

def callback_on_stat_command(call: types.CallbackQuery) -> None:
    assert call.data.startswith(stat_prefix)

    today = datetime(year=date.today().year, month=date.today().month, day=date.today().day)

    u_id = call.message.chat.id
    user = User.objects.get(external_id=u_id)
    answer = call.data[len(stat_prefix):]

    if answer == 'lessons_30_days':
        start_date = today - timedelta(days=30)
        lessons = LessonRecord.objects.filter(date__date__gt=start_date) & LessonRecord.objects.filter(user=user)
        text = ''.join([f'{l.date}: {l.duration} minutes ({l.comment})\n' for l in lessons])

        if text == '':
            bot.send_message(u_id, text='You had no lessons in the last 30 days...')
        else:
            bot.send_message(u_id, text=text)

    elif answer == 'words_month':
        start_date = today - timedelta(days=30)
        words = WordRecord.objects.filter(added_at__date__gt=start_date) & WordRecord.objects.filter(user=user)

        text = f'You saved {words.count()} words for the last 30 days'
        bot.send_message(u_id, text=text)

    elif answer == 'recent_10_words':
        words = WordRecord.objects.filter(user=user)
        n_words = 10 if words.count() >= 10 else words.count()
        last_ten_words = WordRecord.objects.filter(user=user).order_by('added_at')[:n_words:-1]
        text = ''.join([f'{w.en_word} = {w.ru_translation} ({w.comment})\n' for w in last_ten_words])

        if text == '':
            bot.send_message(u_id, text='Not words added so far...')
        else:
            bot.send_message(u_id, text=text)

    else:
        bot.send_message(u_id, text='smth wrong')

def register_stat_handler() -> None:
    bot.register_message_handler(act_on_stat_command, commands=['stat'])
    bot.register_callback_query_handler(
        callback_on_stat_command,
        lambda call: call.data.startswith(stat_prefix),
    )