import telebot as tg

from sqlite import SQLight

token = "1851253471:AAHTPikHhvOWWqcdIdK4QN19F49BUwyb74g"
admin_id = "697488147"
bot = tg.TeleBot(token)

db = SQLight('db.sqlite')


@bot.message_handler(commands=['id'])
def get_id(message):
    bot.send_message(message.chat.id, f'Ваш ID: {message.from_user.id}')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Добро пожаловать {message.from_user.first_name}!\n"
                                      f"Ваш никнейм: {message.from_user.username}\n"
                                      f"Ваш ID: {message.from_user.id}")

#
# @bot.message_handler(content_types=['text'])
# def body(message):
#     if message.reply_to_message:
#         bot.send_message(message.reply_to_message.forward_from.id, message.text)
#     else:
#         bot.forward_message(admin_id,
#                             message.from_user.id,
#                             message.id
#                             )


@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id)
    else:
        db.update_subscription(message.from_user.id, True)

    return bot.send_message(message.chat.id, "Вы успешно подписаны")


@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    if not db.subscriber_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id, False)
        bot.send_message(message.chat.id, "Вы итак не подписаны")
    else:
        db.update_subscription(message.from_user.id, False)
        bot.send_message(message.chat.id, "Вы успешно отписались")


bot.polling()
