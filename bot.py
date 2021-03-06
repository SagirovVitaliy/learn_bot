import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from random import randint, choice
from glob import glob
from emoji import emojize

import settings
import ephem
import datetime


logging.basicConfig(filename='bot.log', level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 
    'password': settings.PROXY_PASSWORD}}


def greet_user(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Здравствуй, пользователь {context.user_data['emoji']}!")


def conversation(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.text
    update.message.reply_text(f"Он ещё не умеет разговаривать дурила {context.user_data['emoji']}!)")


def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']


def play_random_numbers(user_number):
    bot_number = randint(user_number-10, user_number+10)
    if user_number > bot_number:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, ты выиграл!'
    elif user_number == bot_number:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, ничья!'
    else:
        message = f'Ты загадал {user_number}, я загадал {bot_number}, я выиграл!'
    return message


def guess_numder(update, context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = 'Введите целое число'
    else:
        message = 'Введите число'
    update.message.reply_text(message)


def send_cat_picture(update, context):
    cat_photos_list = glob('images/cat*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))


def planet(update, context):
    date = datetime.date.today()

    print(context.args)

    planeta = context.args

    need_planet = planeta[0].capitalize()

    print(need_planet)

    list_planet = [name for n, m, name in ephem._libastro.builtin_planets()]
    
    if need_planet in list_planet[:8]:
        planet_obj = getattr(ephem, need_planet)(date)
           
        constellation = ephem.constellation(planet_obj)
        
        print(constellation)
        
        update.message.reply_text(f'на {date} планета находится в созвездии {constellation}') 
    else:
        update.message.reply_text(f'планета {need_planet} не найдена')


def wordcount(update, context):
    print(context.args)
    if len(context.args) == 0:
        message = 'Введите слова'
    else:
        message = f'{len(context.args)} слова'    
    update.message.reply_text(message)


def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher

    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', planet))
    dp.add_handler(CommandHandler('guess', guess_numder))
    dp.add_handler(CommandHandler('cat', send_cat_picture))
    dp.add_handler(CommandHandler('wordcount', wordcount))

    dp.add_handler(MessageHandler(Filters.text, conversation))
    
    logging.info("Бот стартовал")

    mybot.start_polling()

    mybot.idle()


if __name__ == "__main__":
    main()
