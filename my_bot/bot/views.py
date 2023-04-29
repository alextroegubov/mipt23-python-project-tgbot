from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

import telebot

from .models import User, WordRecord, LessonRecord


from bot.main_bot import bot

from bot.handlers import reg, start, addword, addlesson, stat

def index(request):
    #if request.method == "POST":
    if request.META['CONTENT_TYPE'] == 'application/json':
        update = telebot.types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])

        return HttpResponse("")

reg.register_handler_reg()
start.register_handler_start()
addword.register_handler_addword()
addlesson.register_handler_addlesson()
stat.register_stat_handler()

@bot.message_handler(commands=['help'])
def send_welcome(message):
    # TBD
	bot.reply_to(message, "Howdy, how are you doing?")






# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
# 	bot.reply_to(message, '<b>message.text</b>', parse_mode='HTML')


bot.polling(non_stop=True)