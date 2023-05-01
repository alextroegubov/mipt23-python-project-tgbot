from telebot import types
from typing import Dict

from bot.main_bot import bot
from bot.models import User, WordRecord
from bot.utils import get_yes_no_inline_keyboard, start_menu
from bot.utils import int_validator, word_validator


# prefixes to distinguish between callback queris
comment_prefix = 'comment_addword_inline_keyboard_'
confirm_prefix = 'confirm_addword_inline_keyabord_'

# to store data before saving in db
g_input_user_data: Dict[int, WordRecord] = {}


def act_on_addword_command(u_id: int) -> None:
    """ Handler to addword command"""

    user = User.objects.get(external_id=u_id)

    text = "Ура, пополняем словарь😃 Введите новое слово:"
    msg = bot.send_message(u_id, text=text)

    global g_input_user_data
    g_input_user_data[u_id] = WordRecord(user=user)

    bot.register_next_step_handler(
        msg,
        callback=get_word_record_en_word
    )


def get_word_record_en_word(message: types.Message) -> None:
    """ Get enlish word from message"""
    u_id = message.from_user.id
    user = User.objects.get(external_id=u_id)
    global g_input_user_data

    if not (u_id in g_input_user_data):
        return

    entered_data = message.text
    # validation of entered data
    if not word_validator(entered_data):
        text = (f"Неправильный формат (<b>{entered_data}</b>)😓 Слово может содержать только буквы и цифры.\n"
                 "Давайте еще раз:")

        msg = bot.send_message(u_id, text=text, parse_mode='HTML')
        bot.register_next_step_handler(msg, callback=get_word_record_en_word)
        return

    g_input_user_data[u_id].en_word = message.text.lower()

    if WordRecord.objects.filter(user=user, en_word=message.text.lower()).exists():
        word = WordRecord.objects.get(user=user, en_word=message.text.lower())
        text = ( "Такое слово уже есть в словаре 🙃"
                f"Слово: <i>{word.en_word}</i>\n"
                f"Перевод: <i>{word.ru_translation}</i>\n" +
                f"[<i>{word.comment}</i>]")

        bot.send_message(u_id, text=text, parse_mode='HTML', reply_markup=start_menu)
        return

    text = f"Записал <i>{message.text}</i>👌 Введите перевод:"

    bot.send_message(u_id, text=text, parse_mode='HTML')

    bot.register_next_step_handler(
        message,
        callback=get_word_record_ru_translation
    )


def get_word_record_ru_translation(message: types.Message) -> None:
    """ Get translation from message """
    u_id = message.from_user.id
    global g_input_user_data

    if not (u_id in g_input_user_data):
        return

    entered_data = message.text
    # validation of entered data
    if not word_validator(entered_data):
        text = (f"Неправильный формат (<b>{entered_data}</b>)😓 Слово может содержать только буквы и цифры.\n"
                 "Давайте еще раз:")

        msg = bot.send_message(u_id, text=text, parse_mode='HTML')
        bot.register_next_step_handler(msg, callback=get_word_record_ru_translation)
        return

    g_input_user_data[u_id].ru_translation = message.text

    text = f"Перевод записан <i>{message.text}</i>👌 Добавим пояснение?"

    yes_text = 'Ну разумеется 😉'
    no_text = 'Неа 🙄'
    kb = get_yes_no_inline_keyboard(comment_prefix, yes_text, no_text)

    bot.send_message(u_id, text=text, reply_markup=kb, parse_mode='HTML')


def callback_on_comment(call: types.CallbackQuery) -> None:
    """ Callback on question about comment"""
    assert call.data.startswith(comment_prefix)

    u_id = call.message.chat.id
    answer = call.data[len(comment_prefix):]

    if answer == 'yes':
        msg = bot.send_message(u_id, text="Тогда вводите пояснение 😂")
        bot.register_next_step_handler(msg, callback=get_word_record_comment)
    elif answer == 'no':
        msg = bot.send_message(u_id, text="Ну ладно...")
        confirm_add_word(u_id)


def get_word_record_comment(message: types.Message) -> None:
    """ Get comment from the message"""
    u_id = message.from_user.id
    global g_input_user_data

    if not (u_id in g_input_user_data):
        return

    g_input_user_data[u_id].comment = message.text

    confirm_add_word(u_id)


def confirm_add_word(u_id: int) -> None:
    """ Show confirm keyboard"""
    global g_input_user_data
    if not (u_id in g_input_user_data):
        return

    word = g_input_user_data[u_id]

    comment = f"\n({word.comment})" if word.comment != '' else ''
    text = (f"Все правильно?\n"
            f"Слово: <i>{word.en_word}</i>\n"
            f"Перевод: <i>{word.ru_translation}</i>" +
            comment)

    yes_text = "Да, все так 👍"
    no_text = "Я вводил другое 👎"
    kb = get_yes_no_inline_keyboard(confirm_prefix, yes_text, no_text)

    bot.send_message(u_id, text=text, reply_markup=kb, parse_mode='HTML')


def callback_on_cofirm_add_word(call: types.CallbackQuery):
    """ Callback on confirmation question"""
    assert call.data.startswith(confirm_prefix)
    global g_input_user_data

    u_id = call.message.chat.id
    answer = call.data[len(confirm_prefix):]

    if not (u_id in g_input_user_data):
        return

    if answer == 'yes':
        g_input_user_data[u_id].save()
        text = f"Супер! <i>{g_input_user_data[u_id].en_word}</i> успешно добавлено в словарь 🤝"

    elif answer == 'no':
        text = f"Упс... Давайте попробуем еще раз 👉👈"

    # remove tmp input data
    g_input_user_data.pop(u_id)

    bot.send_message(u_id, text=text, parse_mode='HTML', reply_markup=start_menu())


def register_handler_addword() -> None:
    """ register handlers for addword command"""
    bot.register_callback_query_handler(
        callback=callback_on_cofirm_add_word,
        func=lambda call: call.data.startswith(confirm_prefix)
    )
    bot.register_callback_query_handler(
        callback=callback_on_comment,
        func=lambda call: call.data.startswith(comment_prefix)
    )
