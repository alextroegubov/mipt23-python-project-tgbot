from bot.main_bot import bot
from bot.models import User

def act_on_reg_command(message):

    if User.objects.filter(external_id=message.from_user.id).exists():
        bot.send_message(
             message.from_user.id,
             "You are already registered :)"
        )
    else:
        bot.send_message(
            message.from_user.id,
            "Let's start the registration! What is your name?"
        )
        bot.register_next_step_handler(message, callback=get_user_name)

def get_user_name(message):
    name = message.text
    new_user = User(username=name, external_id=message.from_user.id)
    new_user.save()

    bot.reply_to(
        message.from_user.id,
        f"Successfully registered user {name}, id={message.from_user.id}. \
        Now you can use all functions of the bot. \help for more details"
    )

def register_handler_reg():
    bot.register_message_handler(commands=['reg'], callback=act_on_reg_command)