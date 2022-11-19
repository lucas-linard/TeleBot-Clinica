import os
from collections import UserDict
from time import sleep

import telebot
from telebot import types


API_TOKEN = '5787455269:AAHeom_PmlWUL5jgeiiLkxOPN1Y9ycCjQfc'

bot = telebot.TeleBot(API_TOKEN)




user_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.idade = None
        self.sex = None
        self.cpf = None


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])

def start_message(message):
    bot.send_message(message.chat.id,'Olá , Tudo bem ? Seja bem vindo . ' )
    sleep(2)
    bot.send_message(message.chat.id, 'Por favor , Informe seus dados ' )
    send_welcome(message)


def send_welcome(message):
    msg = bot.reply_to(message, """\

            informe seu nome :
            """)


    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'Qual sua idade')
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(message, 'Age should be a number. How old are you?')
            bot.register_next_step_handler(msg, process_age_step)
            return
        user = user_dict[chat_id]
        user.age = age
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Homem', 'Mulher')
        msg = bot.reply_to(message, 'What is your gender', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_sex_step(message):
    try:
        chat_id = message.chat.id
        sex = message.text
        user = user_dict[chat_id]
        if (sex == u'Homem') or (sex == u'Mulher'):
            user.sex = sex
        else:
            raise Exception("Unknown sex")
        bot.send_message(chat_id, 'Nice to meet you ' + user.name + '\n Age:' + str(user.age) + '\n Sex:' + user.sex)
    except Exception as e:
        bot.reply_to(message, 'oooops')




# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()



