import os
import time

import requests
import telebot
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telebot import types

load_dotenv()

URL = os.getenv('URL')
API_KEY = os.getenv('API_KEY')
WEBSITE = os.getenv('WEBSITE')

bot = telebot.TeleBot(API_KEY)

HISTORY_NEWS = []  # Список предыдущих новостей
USER_ID = None


def parser_news(url):
    r = requests.get(url)
    soap = BeautifulSoup(r.text, "html.parser")
    news = soap.find_all('div', class_='title')
    list_news = [c.text for c in news]
    last_news = list_news[:1][0].replace('\xa0', ' ')
    last_link = WEBSITE + news[:1][0].a['href']
    return last_news, last_link


def check_news():
    while True:
        last_news, last_link = parser_news(URL)
        if len(HISTORY_NEWS) == 0:
            HISTORY_NEWS.append(last_news)
            bot.send_message(USER_ID, (f'{last_news}.\n'
                                       f'Подробности по ссылке {last_link}'))
        else:
            if last_news != HISTORY_NEWS[0]:
                HISTORY_NEWS[0] = last_news
                # Отправить новую новость пользователю
                bot.send_message(USER_ID, (f'{last_news}\n'
                                           f'Подробности по ссылке {last_link}'))
        time.sleep(60)


@bot.message_handler(commands=['start'])
def select_choose(m):
    global USER_ID
    USER_ID = m.chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start = types.KeyboardButton(text='Да')
    stop = types.KeyboardButton(text='Нет')
    keyboard.add(start, stop)
    message = '''Здравствуйте!Начинаем следить за новостями?
Нажмите "Да" чтобы продолжить.
Нажмите "Нет", если хотите отключить уведомления о новостях.'''
    bot.send_message(USER_ID, message, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Да')
def send_news(m):
    if m.text == "нет":
        exit()
    else:
        check_news()


@bot.message_handler(func=lambda message: message.text == 'Нет')
def stop_tracking_news(m):
    message = '''Хорошо, если захотите начать следить за\
    новостями, просто напишите "/start".'''
    bot.send_message(USER_ID, message)


if __name__ == "__main__":
    bot.polling()
