from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import os
from config import *


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
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join('downloads', '{}.jpg'.format(photo_file.file_id))
    photo_file.download(filename)
    bot.send_message(chat_id=update.message.chat_id, text="Получил скриншот " + filename)

screenshot_handler = MessageHandler(Filters.photo, screenshot_callback)
dispatcher.add_handler(screenshot_handler)

updater.start_polling()
updater.idle()