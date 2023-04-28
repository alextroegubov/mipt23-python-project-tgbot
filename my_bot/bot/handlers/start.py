from bot.main_bot import bot

def act_on_start_command(message):
	bot.send_message(
		message.from_user.id, 
	    "Hi, I am a telegram bot! I can help you study English words.\
        Please register to continue. /reg")
	
def register_handler_start():
	bot.register_message_handler(callback=act_on_start_command, commands=['start'])