from django.http import HttpResponse, HttpRequest  # type: ignore
import telebot  # type: ignore

from bot.main_bot import bot
from bot.handlers import reg, start, addword, addlesson, stat, delete
from bot.handlers import help as help_module


def index(request: HttpRequest) -> HttpResponse:
    # if request.method == "POST":
    if request.META['CONTENT_TYPE'] == 'application/json':
        update = telebot.types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])

        return HttpResponse("")


reg.register_handler_reg()
start.register_handler_start()
addword.register_handler_addword()
addlesson.register_handler_addlesson()
stat.register_stat_handler()
delete.register_del_handler()
help_module.register_help_handler()

bot.polling(non_stop=True)
