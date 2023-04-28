import telebot
from django.conf import settings
from telebot.types import InlineKeyboardButton

TOKEN = settings.TELEGRAM_BOT_TOKEN
bot = telebot.TeleBot(token=TOKEN, parse_mode=None)

