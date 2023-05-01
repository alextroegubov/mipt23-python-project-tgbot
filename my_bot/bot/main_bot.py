""" Module with bot and token"""

import telebot  # type: ignore
from django.conf import settings  # type: ignore

TOKEN = settings.TELEGRAM_BOT_TOKEN
bot = telebot.TeleBot(token=TOKEN, parse_mode=None)
