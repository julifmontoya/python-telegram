import requests
from decouple import config
import telebot

bot = telebot.TeleBot(config('API_KEY'))

def getUrl():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "How are you doing?")


@bot.message_handler(commands=['images'])
def trm_handler(message):
    url = getUrl()
    bot.send_photo(message.chat.id, photo=url, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, "Write /images for use the bot")

bot.polling()
