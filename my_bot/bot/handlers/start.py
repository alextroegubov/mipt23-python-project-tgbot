from bot.models import User
from bot.main_bot import bot
from telebot import types

def act_on_start_command(message: types.Message):

	if User.objects.filter(external_id=message.from_user.id).exists():
		user = User.objects.get(external_id=message.from_user.id)
		bot.send_message(
            message.from_user.id,
            f"Hi, <b>{user.username}</b>✌️ Let's continue learning English 🧠",
            parse_mode='HTML'
        )
	else:
		bot.send_message(
			message.from_user.id, 
			(f"Hi, <b>{message.from_user.username}</b>✌️, I am a telegram bot🤖\n"
    		  "I can help you study English words🤓 "
			  "Please register to continue. /reg"),
			parse_mode='HTML'
		)

def register_handler_start():
	bot.register_message_handler(callback=act_on_start_command, commands=['start'])