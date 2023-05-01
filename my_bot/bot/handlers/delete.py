""" Module for delete command"""

from telebot import types  # type: ignore
from bot.main_bot import bot
from bot.models import User, LessonRecord, WordRecord, GameRecord

DEL_PREFIX = 'del_inline_keyboard_'


def get_del_inline_keyboard() -> types.InlineKeyboardMarkup:
    """ Keyboard creator"""
    ikbm = types.InlineKeyboardMarkup()

    ikbm.add(
        types.InlineKeyboardButton(
            text='Да, сноси 👹',
            callback_data=DEL_PREFIX + 'yes'
        ),
        types.InlineKeyboardButton(
            text='Нет, оставь 😫',
            callback_data=DEL_PREFIX + 'no'
        )
    )

    return ikbm


def act_on_del_command(message: types.Message) -> None:
    """ Reaction to /del command """

    u_id = message.from_user.id

    if not User.objects.filter(external_id=u_id):
        text = "У вас еще нет профиля 😅. Сначала зарегистрируйтесь /reg"
        bot.send_message(u_id, text=text)
        return

    text = "Уверены, что хотите удалить профиль?😱"
    ikbm = get_del_inline_keyboard()

    bot.send_message(u_id, text=text, reply_markup=ikbm)


def callback_on_del_command(call: types.CallbackQuery) -> None:
    """ Callback for answers in /del command """
    assert call.data.startswith(DEL_PREFIX)

    u_id = call.message.chat.id
    user = User.objects.get(external_id=u_id)
    answer = call.data[len(DEL_PREFIX):]

    if answer == 'yes':
        LessonRecord.objects.filter(user=user).delete()
        WordRecord.objects.filter(user=user).delete()
        GameRecord.objects.filter(user=user).delete()
        user.delete()

        bot.send_message(u_id, text='Ваш профиль удален 😵')

    elif answer == 'no':
        bot.send_message(u_id, text="Обошлось 😪 Давайте учить английский 🙃")


def register_del_handler() -> None:
    """ Register handlers for /del command"""
    bot.register_message_handler(commands=['del'], callback=act_on_del_command)
    bot.register_callback_query_handler(
        callback_on_del_command,
        lambda call: call.data.startswith(DEL_PREFIX),
    )
