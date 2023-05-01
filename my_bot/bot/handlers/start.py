from telebot import types

from bot.models import User
from bot.main_bot import bot

from bot.utils import start_menu, start_menu_prefix

from bot.handlers.addword import act_on_addword_command
from bot.handlers.addlesson import act_on_addlesson_command
from bot.handlers.game import act_on_game_command
from bot.handlers.stat import act_on_stat_command




def act_on_start_command(message: types.Message) -> None:
    """ Primary handler for /start command"""

    if User.objects.filter(external_id=message.from_user.id).exists():
        user = User.objects.get(external_id=message.from_user.id)
        bot.send_message(
            message.from_user.id,
            f"Привет, <b>{user.username}</b>✌️ Давай продолжим изучать английский 🧠",
            parse_mode='HTML',
            reply_markup=start_menu()
        )

    else:
        bot.send_message(
            message.from_user.id,
            (f"Привет, <b>{message.from_user.username}</b> ✌️, я телеграм-бот🤖\n"
             "Я могу помочь тебе в изучении английских слов 🤓 "
             "Пожалуйста, зарегистрируйся /reg"),
            parse_mode='HTML'
        )


def callback_on_start_menu(call: types.CallbackQuery) -> None:
    """ Callback on menu"""
    assert call.data.startswith(start_menu_prefix)

    u_id = call.message.chat.id
    answer = call.data[len(start_menu_prefix):]

    if answer == 'addword':
        act_on_addword_command(u_id)
    elif answer == 'addlesson':
        act_on_addlesson_command(u_id)
    elif answer == 'game':
        act_on_game_command(u_id)
    elif answer == 'stat':
        act_on_stat_command(u_id)
    else:
        bot.send_message(u_id, 'smth wrong')


def register_handler_start() -> None:
    """ Register handlers for /start command"""
    bot.register_message_handler(
        callback=act_on_start_command, commands=['start'])
    bot.register_callback_query_handler(
        callback=callback_on_start_menu,
        func=lambda call: call.data.startswith(start_menu_prefix)
    )
