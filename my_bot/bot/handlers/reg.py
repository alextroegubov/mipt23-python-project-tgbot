from bot.main_bot import bot
from bot.models import User
from telebot import types


def act_on_reg_command(message: types.Message) -> None:
    """ Primary handler to /reg command"""

    if User.objects.filter(external_id=message.from_user.id).exists():
        user = User.objects.get(external_id=message.from_user.id)

        bot.send_message(
            message.from_user.id,
            (f"<b>{user.username}</b>, you are already registered😅"
             "To delete your profile, use /del"),
            parse_mode='HTML'
        )
    else:
        bot.send_message(
            message.from_user.id,
            "Let's start the registration! What is your name?"
        )
        bot.register_next_step_handler(message, callback=get_user_name)


def get_user_name(message: types.Message) -> None:
    """ Handler to get user name """
    name = message.text
    new_user = User(username=name, external_id=message.from_user.id)
    new_user.save()

    bot.reply_to(
        message.from_user.id,
        (f"Successfully registered user <b>{name}</b>"
         "Now you can use all functions of the bot. Use \help for more details."),
         parse_mode='HTML'
    )


def register_handler_reg() -> None:
    """ Register handler for /reg command """
    bot.register_message_handler(commands=['reg'], callback=act_on_reg_command)
