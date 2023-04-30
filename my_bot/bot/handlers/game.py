from bot.main_bot import bot
from bot.models import User, WordRecord, GameRecord

from telebot import types

from typing import Dict

from bot.utils import date_validator, date_str_to_django, date_django_to_str
from bot.utils import get_yes_no_inline_keyboard

from dataclasses import dataclass
from typing import List
import random

from functools import partial

select_prefix = 'select_game_inline_keyboard_'
confirm_prefix = 'confirm_game_inline_keyabord_'

@dataclass
class GameMetaData():
    n_questions: int
    n_asked_questions: int
    n_right_questions: int
    words: List[int]

    def __init__(self, words: List[int] = [], n_questions: int = 10, n_asked_questions: int = 0, n_right_questions: int = 0):
        self.n_questions = n_questions
        self.n_asked_questions = n_asked_questions
        self.n_right_questions = n_right_questions
        self.words = words


g_game_user_data: Dict[int, GameMetaData] = {}

def act_on_game_command(message: types.Message):
    u_id = message.from_user.id

    if not User.objects.filter(external_id=u_id):
        text = "Please, register first. /reg"
        bot.send_message(u_id, text=text)
        return

    if WordRecord.objects.count() < 5:
        text = "Too few words in the dictionary..."
        bot.send_message(u_id, text=text)
        return

    global g_game_user_data

    try:
        g_game_user_data.pop(u_id)
    except KeyError:
        pass

    user = User.objects.get(external_id=u_id)
    text = "Let's revise english words (10 pieces)"
    bot.send_message(u_id, text=text)

    g_game_user_data[u_id] = GameMetaData(words=[])

    # select 10 words:
    words_idx = list(WordRecord.objects.filter(user=user).values_list('pk', flat=True))

    print(words_idx)
    g_game_user_data[u_id].words = random.sample(words_idx, min(g_game_user_data[u_id].n_questions, len(words_idx)))

    g_game_user_data[u_id].n_questions = len(g_game_user_data[u_id].words)

    ask_word_ru_translation(u_id)


def get_keyboard_markup(translations: List[str]):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    print(translations)

    for translation in translations:
        btn = types.KeyboardButton(translation)
        kb.add(btn)

    return kb

def ask_word_ru_translation(u_id: int):
    global g_game_user_data
    assert u_id in g_game_user_data

    game = g_game_user_data[u_id]

    user = User.objects.get(external_id=u_id) 
    word = WordRecord.objects.get(pk=game.words[game.n_asked_questions], user=user)
    game.n_asked_questions += 1

    all_choices = list((WordRecord.objects.filter(user=user) 
               & WordRecord.objects.exclude(id=word.pk)).values_list('ru_translation', flat=True))

    choices = random.sample(all_choices, game.n_questions-1)
    choices.extend([word.ru_translation])

    kb = get_keyboard_markup(choices)

    text = f'What is translation for {word.en_word}?'
    msg = bot.send_message(u_id, text=text, reply_markup=kb)

    right_answer = word.ru_translation

    bot.register_next_step_handler(
        msg,
        callback=partial(check_choice, right_answer, u_id)
    )

def check_choice(right_answer: str, u_id: int, message: types.Message, ):
    global g_game_user_data
    assert u_id in g_game_user_data
    game = g_game_user_data[u_id]

    if message.text == right_answer:
        text = f'Absolutely right!'
        game.n_right_questions += 1
    else:
        text = f'Ooops, the right answer is {right_answer}...'

    bot.send_message(u_id, text=text, parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())

    if game.n_asked_questions < game.n_questions:
        ask_word_ru_translation(u_id)
    else:
        send_score(u_id)

def send_score(u_id: int):
    global g_game_user_data
    assert u_id in g_game_user_data
    game = g_game_user_data[u_id]

    user = User.objects.get(external_id=u_id)

    bot.send_message(u_id, text=f'Good results: {game.n_right_questions}/{game.n_asked_questions}')

    GameRecord(user=user, n_questions=game.n_asked_questions, n_answers=game.n_right_questions).save()


def register_game_handler():
    bot.register_message_handler(commands=['game'], callback=act_on_game_command)