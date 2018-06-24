from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
import os, sys
from config import *
from tickets import ocr_tickets, parse_tickets


updater = Updater(token=TOKEN, request_kwargs=PROXY)
dispatcher = updater.dispatcher

def start_callback(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Я бот для гильдии DarkLightCrew. Добро пожаловать!")

start_handler = CommandHandler('start', start_callback)
dispatcher.add_handler(start_handler)

def help_callback(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Справка еще не готова")

echo_handler = CommandHandler('help', help_callback)
dispatcher.add_handler(echo_handler)

def unknown_callback(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Какая-то левая команда, не знаю такую")

unknown_handler = MessageHandler(Filters.command, unknown_callback)
dispatcher.add_handler(unknown_handler)

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Your bunny wrote: " + update.message.text)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

def screenshot_callback(bot, update):
    # получить скрин с энкой
    try:
        photo_file = bot.getFile(update.message.photo[-1].file_id)
        filename = os.path.join('downloads', '{}.jpg'.format(photo_file.file_id))
        photo_file.download(filename)
        bot.send_message(chat_id=update.message.chat_id, text="Получил скриншот, пытаюсь найти в нем результаты энки. Пожалуйста, подождите...")
    except:
        bot.send_message(chat_id=update.message.chat_id, text="Не удалось получить скриншот: " + repr(sys.exc_info()[0]))
    # распознать
    try:
        text = ocr_tickets(filename)
        result = parse_tickets(text)
        bot.send_message(chat_id=update.message.chat_id, text="Содержимое: " + str(result))
    except:
        bot.send_message(chat_id=update.message.chat_id, text="Не удалось распознать энку: " + repr(sys.exc_info()[0]))


screenshot_handler = MessageHandler(Filters.photo, screenshot_callback)
dispatcher.add_handler(screenshot_handler)

# def error_callback(bot, update, error):
#     try:
#         raise error
#     except Unauthorized:
#         # remove update.message.chat_id from conversation list
#     except BadRequest:
#         # handle malformed requests - read more below!
#     except TimedOut:
#         # handle slow connection problems
#     except NetworkError:
#         # handle other connection problems
#     except ChatMigrated as e:
#         # the chat_id of a group has changed, use e.new_chat_id instead
#     except TelegramError:
#         # handle all other telegram related errors

# dispatcher.add_error_handler(error_callback)

updater.start_polling()
updater.idle()