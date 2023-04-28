# from django.conf import settings
# import telebot

# from django.core.exceptions import PermissionDenied

# from django.http import HttpResponse

# TOKEN = settings.TELEGRAM_BOT_TOKEN
# bot = telebot.AsyncTeleBot(TOKEN)


# @bot.csrf_exempt
# def bothook(request):
#     if request.META['CONTENT_TYPE'] == 'application/json':
#         json_data = request.body.decode('utf-8')
#         update = telebot.types.Update.de_json(json_data)
#         bot.process_new_updates([update])
#         return HttpResponse("")
#     else:
#         raise PermissionDenied

# # @bot.message_handler(commands=['start'])
# # def greet(message):
# #     bot.send_message(message.chat.id, 'Hello')



# @bot.message_handler(content_types=['text'])
# def send_echo(message):
#     bot.reply_to(message, message.text)

# bot.polling(non_stop=True)
