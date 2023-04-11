import telebot
from extensions import APIException, Convert
from config import TOKEN, exchanges
import traceback

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    bot.reply_to(message, f'Добро пожаловать \n \
    Чтобы начать работу введите комманду боту в следующем формате:\n\
    <имя первой валюты><имя валюты в которую перевести>\
    <количество переводимой валюты>\n\
    Посмотреть список всех валют: /values, {message.chat.username}')

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convert.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка :\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling()
