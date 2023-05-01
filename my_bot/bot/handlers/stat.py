""" Module for statistics command"""
from datetime import datetime, date, timedelta
from telebot import types  # type: ignore
from telebot.types import InlineKeyboardButton  # type: ignore

from bot.main_bot import bot
from bot.models import User, LessonRecord, WordRecord
from bot.utils import start_menu, START_TEXT

STAT_PREFIX = 'stat_inline_keyboard_'


def get_stat_inline_keyboard() -> types.InlineKeyboardMarkup:
    """ Get statistics keyboard"""
    ikbm = types.InlineKeyboardMarkup()

    ikbm.add(
        InlineKeyboardButton(
            text='Уроки за 30 дней',
            callback_data=STAT_PREFIX + 'lessons_30_days'
        ),
        InlineKeyboardButton(
            text='Последние 10 слов',
            callback_data=STAT_PREFIX + 'recent_10_words'

        ),
        InlineKeyboardButton(
            text='Число слов за месяц',
            callback_data=STAT_PREFIX + 'words_month'
        )
    )

    return ikbm


def act_on_stat_command(u_id: int) -> None:
    """ Handler for stat command"""
    user = User.objects.get(external_id=u_id)
    text = f"Так-так, <b>{user.username}</b>, давай посмотрим на твой прогресс"
    ikbm = get_stat_inline_keyboard()

    bot.send_message(u_id, text=text, reply_markup=ikbm, parse_mode='HTML')


def callback_on_stat_command(call: types.CallbackQuery) -> None:
    """ Callback on statistics command"""
    assert call.data.startswith(STAT_PREFIX)

    today = datetime(year=date.today().year,
                     month=date.today().month, day=date.today().day)

    u_id = call.message.chat.id
    user = User.objects.get(external_id=u_id)
    answer = call.data[len(STAT_PREFIX):]

    if answer == 'lessons_30_days':
        start_date = today - timedelta(days=30)
        lessons = LessonRecord.objects.filter(
            date__date__gt=start_date) & LessonRecord.objects.filter(user=user)
        text = ''.join(
            [f'<b>{l.date}</b>: {l.duration} (минуты) [<i>{l.comment}</i>]\n' for l in lessons])

        if text == '':
            bot.send_message(
                u_id, text='За последние 30 дней не было уроков... 😰')
        else:
            bot.send_message(u_id, text=text, parse_mode='HTML')

    elif answer == 'words_month':
        start_date = today - timedelta(days=30)
        words = WordRecord.objects.filter(
            added_at__date__gt=start_date) & WordRecord.objects.filter(user=user)

        text = f'За последние 30 дней сохранено <b>{words.count()}</b> слов'
        bot.send_message(u_id, text=text, parse_mode='HTML')

    elif answer == 'recent_10_words':
        words = WordRecord.objects.filter(user=user)
        n_words = 10 if words.count() >= 10 else words.count()
        last_ten_words = WordRecord.objects.filter(
            user=user).order_by('added_at')[:n_words:-1]
        text = ''.join(
            [f'<b>{w.en_word}</b> = {w.ru_translation} [<i>{w.comment}</i>]\n'
             for w in last_ten_words])

        if text == '':
            bot.send_message(u_id, text='Пока что словарь пустой...')
        else:
            bot.send_message(u_id, text=text, parse_mode='HTML')

    bot.send_message(u_id, text=START_TEXT, parse_mode='HTML',
                     reply_markup=start_menu())


def register_stat_handler() -> None:
    """ Register handlers for stat command"""
    bot.register_callback_query_handler(
        callback_on_stat_command,
        lambda call: call.data.startswith(STAT_PREFIX),
    )
