import requests
from bs4 import BeautifulSoup
from decouple import config
import telebot
from datetime import datetime
now = datetime.now()

bot = telebot.TeleBot(config('API_KEY'))

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "How are you doing?")


@bot.message_handler(commands=['trm'])
def trm_handler(message):
    text = "Which TRM Do you want to know?\nChoose one: *Dolar*, *Euro*"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, fetchTrm)


def fetchTrm(message):
    trm = message.text.upper()
    if (trm == "DOLAR"):
        url = requests.get("https://www.dolar-colombia.com/")
        soup = BeautifulSoup(url.content, "html.parser")
        result = soup.find("span", class_="exchange-rate").get_text()

    elif (trm == "EURO"):
        url = requests.get("https://www.dolarhoy.co/eurohoy/")
        soup = BeautifulSoup(url.content, "html.parser")
        result = soup.find("span", class_="h1").get_text()
        result = result.split("€ ", 1)[-1]

    else:
        result = "Write /trm and then choose one: *Dolar*, *Euro*"
        
    bot.send_message(message.chat.id, f"Here's your TRM for: {now.day}/{now.month}/{now.year}")    
    bot.send_message(message.chat.id, result, parse_mode="Markdown")


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, "Write /trm for use the bot")


bot.polling()
