import telebot
import requests
import json
from config import token, keys
from extensions import ExchangeException, Exchange

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'Здравствуйте, {message.chat.first_name}.\n'
                                      f'Укажите исходную валюту и валюту, в которую нужно перевести.\n'
                                      f'Затем укажите сумму в исходной валюте.\n'
                                      f'Чтобы узнать о доступных для конвертации валютах, используйте /values')

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, f'Чтобы увидеть список доступных валют, используйте /values.\n'
                                      f'Чтобы провести конвертацию, укажите исходную валюту, валюту,'
                                      f' в которую нужно перевести, и сумму.')

@bot.message_handler(commands=['values'])
def get_values(message):
    text = "Доступные для конвертации валюты: "
    for key in keys.keys():
        text = '\n'.join((text, keys[key]))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    quote, base, amount = message.text.split(' ')
    try:
        if len(message.text.split(' ')) != 3:
            raise ExchangeException('Введите команду или 3 параметра')

        total_base = Exchange.get_price(quote, base, amount)
    except ExchangeException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Что-то пошло не так.')

    text = f'Цена {amount} {keys[quote]} -- {total_base} {keys[base]}'
    bot.send_message(message.chat.id, text)





bot.polling()
