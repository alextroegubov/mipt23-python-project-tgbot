""" Module for help command """
from telebot import types  # type: ignore
from bot.main_bot import bot


def act_on_help_command(message: types.Message) -> None:
    """ Primary handler to /help command"""
    text = ("/start - <i>главное меню</i>\n"
            "/reg - <i>зарегистрироваться</i>\n"
            "/del - <i>удалить профиль</i>")

    bot.send_message(message.from_user.id, text=text, parse_mode='HTML')


def register_help_handler() -> None:
    """ Register handler for /reg command """
    bot.register_message_handler(commands=['help'], callback=act_on_help_command)
