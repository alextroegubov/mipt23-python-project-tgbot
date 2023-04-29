from bot.main_bot import bot
from bot.models import User, LessonRecord, WordRecord
from telebot import types

del_prefix = 'del_inline_keyboard_'


def get_del_inline_keyboard() -> types.ReplyKeyboardMarkup:
    """ Keyboard creator"""
    ikbm = types.InlineKeyboardMarkup()

    ikbm.add(
        types.InlineKeyboardButton(
            text='Yes, delete it 👹',
            callback_data=del_prefix + 'yes'
        ),
        types.InlineKeyboardButton(
            text='No, keep it 😫',
            callback_data=del_prefix + 'no'
        )
    )

    return ikbm


def act_on_del_command(message: types.Message) -> None:
    """ Reaction to /del command """

    u_id = message.from_user.id

    if not User.objects.filter(external_id=u_id):
        text = "Please, register first. /reg"
        bot.send_message(u_id, text=text)
        return

    text = "Are you sure to delete your profile?😱"
    ikbm = get_del_inline_keyboard()

    bot.send_message(u_id, text=text, reply_markup=ikbm)


def callback_on_del_command(call: types.CallbackQuery) -> None:
    """ Callback for answers in /del command """
    assert call.data.startswith(del_prefix)

    u_id = call.message.chat.id
    user = User.objects.get(external_id=u_id)
    answer = call.data[len(del_prefix):]

    if answer == 'yes':
        LessonRecord.objects.filter(user=user).delete()
        WordRecord.objects.filter(user=user).delete()
        user.delete()

        bot.send_message(u_id, text='Your profile has been deleted 😵')

    elif answer == 'no':
        bot.send_message(u_id, text="Nice 😪 Let's learn English then 🙃")
    else:
        bot.send_message(u_id, text='smth wrong')


def register_del_handler() -> None:
    """ Register handlers for /del command"""
    bot.register_message_handler(commands=['del'], callback=act_on_del_command)
    bot.register_callback_query_handler(
        callback_on_del_command,
        lambda call: call.data.startswith(del_prefix),
    )
