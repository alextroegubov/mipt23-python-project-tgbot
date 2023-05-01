import random
from telebot import types
from typing import Dict
from dataclasses import dataclass
from typing import List
from functools import partial

from bot.main_bot import bot
from bot.models import User, WordRecord, GameRecord

# prefixes for callback queris
select_prefix = 'select_game_inline_keyboard_'
confirm_prefix = 'confirm_game_inline_keyabord_'

CONST_N_CHOICES = 5


@dataclass
class GameMetaData():
    """ Class to store meta data about game"""
    n_questions: int
    n_asked_questions: int
    n_right_questions: int
    words: List[int]

    def __init__(
        self, words: List[int] = [],
        n_questions: int = 10,
        n_asked_questions: int = 0,
        n_right_questions: int = 0
    ):
        self.n_questions = n_questions
        self.n_asked_questions = n_asked_questions
        self.n_right_questions = n_right_questions
        self.words = words


# store meta data before saving in db
g_game_user_data: Dict[int, GameMetaData] = {}


def act_on_game_command(u_id) -> None:
    """ Handler for game command"""

    n_words = WordRecord.objects.count()
    if n_words < CONST_N_CHOICES:
        text = ("В словаре слишком мало слов 😓({n_words}). "
                "Должно быть <u>минимум 5 слов</u>.")
        bot.send_message(u_id, text=text, parse_mode='HTML')
        return

    global g_game_user_data

    user = User.objects.get(external_id=u_id)
    text = "Давай повторять английские слова 🧠"
    bot.send_message(u_id, text=text)

    g_game_user_data[u_id] = GameMetaData(words=[])

    # select n_questions words:
    words_idx = list(WordRecord.objects.filter(
        user=user).values_list('pk', flat=True))

    g_game_user_data[u_id].words = random.sample(words_idx, min(
        g_game_user_data[u_id].n_questions, len(words_idx)))
    g_game_user_data[u_id].n_questions = len(g_game_user_data[u_id].words)

    ask_word_ru_translation(u_id)


def get_keyboard_markup(translations: List[str]) -> types.ReplyKeyboardMarkup:
    """ Keyboard markup with answers"""
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    for translation in translations:
        btn = types.KeyboardButton(translation)
        kb.add(btn)

    return kb


def ask_word_ru_translation(u_id: int) -> None:
    """ Ask for translation"""
    global g_game_user_data

    game = g_game_user_data[u_id]

    user = User.objects.get(external_id=u_id)
    word = WordRecord.objects.get(
        pk=game.words[game.n_asked_questions], user=user)
    game.n_asked_questions += 1

    right_answer = word.ru_translation

    all_choices = list(
        (WordRecord.objects.filter(user=user) &
         WordRecord.objects.exclude(id=word.pk)).values_list('ru_translation', flat=True)
    )

    choices = random.sample(all_choices, CONST_N_CHOICES-1)
    choices.extend([word.ru_translation])

    text = f'Как переводится <i>{word.en_word}</i>?'
    kb = get_keyboard_markup(choices)
    msg = bot.send_message(u_id, text=text, reply_markup=kb, parse_mode='HTML')

    bot.register_next_step_handler(
        msg,
        callback=partial(check_choice, right_answer, u_id)
    )


def check_choice(right_answer: str, u_id: int, message: types.Message) -> None:
    """ Check the answer and add score"""
    global g_game_user_data
    game = g_game_user_data[u_id]

    if message.text == right_answer:
        text = f'Верно ✅'
        game.n_right_questions += 1
    else:
        text = f'Неверно ❌, правильный ответ <i>{right_answer}</i>'

    bot.send_message(
        u_id,
        text=text,
        parse_mode='HTML',
        reply_markup=types.ReplyKeyboardRemove()
    )

    if game.n_asked_questions < game.n_questions:
        ask_word_ru_translation(u_id)
    else:
        send_score(u_id)


def send_score(u_id: int) -> None:
    """ Send score in chat and save it in db"""
    global g_game_user_data

    game = g_game_user_data[u_id]
    user = User.objects.get(external_id=u_id)

    ratio = game.n_right_questions/game.n_asked_questions
    result = f'Результат: {game.n_right_questions}/{game.n_asked_questions}. '

    if ratio < 0.5:
        text = 'Неплохо, но надо бы подучить слова 😅'
    elif 0.5 < ratio < 0.8:
        text = 'Хороший результат 👍'
    elif ratio > 0.8:
        text = 'Отличный результат 👏'
    bot.send_message(u_id, text=result + text)

    GameRecord(user=user, n_questions=game.n_asked_questions,
               n_answers=game.n_right_questions).save()
