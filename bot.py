import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings
import ephem
import datetime

logging.basicConfig(filename='bot.log', level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 
    'password': settings.PROXY_PASSWORD}}


def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')


def planet(update, context):
    date = datetime.date.today()
    planeta = update.message.text.split()
    print(date)
    print(planeta)
    if planeta[1] == 'Mars' or 'mars':
        a = ephem.Mars(date)    
        constellation = ephem.constellation(a)
        print(constellation)
    update.message.reply_text(f'на {date} планета находится в созвездии {constellation}') 


def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher

    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', planet))
    dp.add_handler(MessageHandler(Filters.text, planet))
    

    logging.info("Бот стартовал")

    mybot.start_polling()

    mybot.idle()


if __name__ == "__main__":
    main()
