import telebot as tg
from telebot import types

from sqlite import SQLight

token = "1851253471:AAHTPikHhvOWWqcdIdK4QN19F49BUwyb74g"
admin_id = "697488147"
bot = tg.TeleBot(token)

db = SQLight('db.sqlite')


# Inline Chat Buttons
class InlineButtons:
    btn1 = types.InlineKeyboardButton("Github", url="https://github.com/Lozerd")
    btn2 = types.InlineKeyboardButton("Pyrogram", url="https://docs.pyrogram.org/")
    btn3 = types.InlineKeyboardButton("Start")


# Reply Chat Buttons
class ReplyButtons:
    btn1 = types.KeyboardButton("Github")
    btn2 = types.KeyboardButton("Pyrogram")
    btn3 = types.KeyboardButton("Start")
    btn4 = types.KeyboardButton("Subscribe")
    btn5 = types.KeyboardButton("Unsubscribe")
    restart = types.KeyboardButton("Restart")

@bot.message_handler(content_types=['new_chat_members'])
def initial(message):
    bot.reply_to(message, "Список команд:\n\t/start\n\t/menu\n\t/subscribe\n\t/unsubscribe")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Добро пожаловать {message.from_user.first_name}!\n"
                                      f"Ваш никнейм: {message.from_user.username}\n"
                                      f"Ваш ID: {message.from_user.id}")


@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup()
    btn = ReplyButtons()
    markup.add(btn.btn1, btn.btn2, btn.restart)
    bot.send_message(message.chat.id, "Это главное меню, выберите опцию", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def msg_parser(message):
    proccessed_message = message.text.strip().lower()

    if proccessed_message == "github":
        markup = types.InlineKeyboardMarkup()
        btn = InlineButtons()
        markup.add(btn.btn1)
        end_message = "Lozerd's Github"
    elif proccessed_message == 'pyrogram':
        markup = types.InlineKeyboardMarkup()
        btn = InlineButtons()
        markup.add(btn.btn2)
        end_message = "Pyrogram Docs"
    elif proccessed_message == 'start':
        return bot.send_message(message.chat.id, f"Добро пожаловать {message.from_user.first_name}!\n"
                                          f"Ваш никнейм: {message.from_user.username}\n"
                                          f"Ваш ID: {message.from_user.id}")
    else:
        markup = types.ReplyKeyboardMarkup()
        btn = ReplyButtons()
        markup.add(btn.btn1, btn.btn2, btn.btn3, btn.btn4, btn.btn5)
        end_message = "Такой кнопки нет, выберите опцию"
    bot.send_message(message.chat.id, end_message, reply_markup=markup)


@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id)
        db.connection.commit()
    else:
        db.update_subscription(message.from_user.id, True)
        db.connection.commit()

    return bot.send_message(message.chat.id, "Вы успешно подписаны")


@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id, False)
        db.connection.commit()
        bot.send_message(message.chat.id, "Вы итак не подписаны")
    else:
        db.update_subscription(message.from_user.id, False)
        db.connection.commit()
        bot.send_message(message.chat.id, "Вы успешно отписались")


''' ECHO COMMAND'''
# @bot.message_handler(content_types=['text'])
# def body(message):
#     if message.reply_to_message:
#         bot.send_message(message.reply_to_message.forward_from.id, message.text)
#     else:
#         bot.forward_message(admin_id,
#                             message.from_user.id,
#                             message.id
#                             )


bot.polling(none_stop=True)