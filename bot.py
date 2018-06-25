from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)
import os, sys
from threading import Thread
import json
from config import *
#from tickets import ocr_tickets, parse_tickets
from functools import wraps

# Список пользователей бота
logging.info('Загружаю список пользователей...')
users = {}
LIST_OF_ADMINS = []
try:
    with open('users.json', 'r') as file:
        json_data = json.load(file)
except IOError as e:
    logging.critical('Не удалось прочитать список пользователей', e)
    exit

try:
    for user in json_data:
        users[user['id']] = {'id': user['id'], 'name': user['name'], 'username': user['username']}
        if user['admin']:
            LIST_OF_ADMINS.append(user['id'])
except Error as e:
    logging.critical('Не удалось загрузить список пользователей', e)
    exit

logging.info('Загружено пользователей %d, администраторов %d' % (len(users), len(LIST_OF_ADMINS)))



def restricted_callback(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Эта команда вам недоступна")

def restricted_admins(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            logging.error("Доступ запрещен для пользователя {}.".format(user_id))
            return restricted_callback(bot, update)
        return func(bot, update, *args, **kwargs)
    return wrapped

def restricted_users(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if users.get(user_id) == None:
            logging.error("Доступ запрещен для пользователя {}.".format(user_id))
            return restricted_callback(bot, update)
        return func(bot, update, *args, **kwargs)
    return wrapped

def broadcast_to_admins(bot, message):
    for admin in LIST_OF_ADMINS:
        bot.send_message(chat_id=admin, text=message)

def broadcast_to_users(bot, message):
    for user in users.keys():
        bot.send_message(chat_id=user, text=message)



logging.info('Инициализирую бота...')
updater = Updater(token=TOKEN)#, request_kwargs=PROXY)
dispatcher = updater.dispatcher



def start_callback(bot, update):
    # Оповестить о новом пользователе
    #if update.effective_user.id in users:
    #    # этот пользователь уже зарегистрирован
    #    logging.info('Old user: ' + str(update.effective_user))
    #    return update.message.reply_text("С возвращением, %s!" % update.effective_user.first_name)
    logging.info('New user: ' + str(update.effective_user))
    # Уведомить админов о новом пользователе
    for admin in LIST_OF_ADMINS:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Разрешить \"%s\" пользоваться ботом" % update.effective_user.first_name,
            callback_data="adduser({})".format(update.effective_user.id))]])
        bot.send_message(chat_id=admin, text='У бота появился новый пользователь:\nid: %d\nname: %s\nlogin: %s'
            % (update.effective_user.id, update.effective_user.first_name, update.effective_user.username),
            reply_markup=keyboard)
    # Вывести приглашение пользователю
    update.message.reply_text("Я бот для гильдии DarkLightCrew.\nДобро пожаловать, %s!\nДождитесь одобрения администратором для использования этого бота."
            % update.effective_user.first_name)

dispatcher.add_handler(CommandHandler('start', start_callback))



def help_callback(bot, update, args):
    if len(args) == 0:
        update.message.reply_text("""Справка по командам бота.
            Для расширенной справки вызовите /help <команда>

            /help - вызов справки этой справки
            /timezone - установка часового пояса
            /adduser - добавление пользователя
            /removeuser - удаление пользователя
            /users - показывает список пользователей
            /promote - добавление администраторских прав пользователю
            /broadcast - отправка сообщения всем пользователям бота""")
    elif args[0] == "timezone":
        update.message.reply_text("""/timezone <смещение относительно GMT>\nУстанавливает часовой пояс пользователя в указанный (смещение в часах относительно GMT)""")
    elif args[0] == "adduser":
        update.message.reply_text("""/adduser <идентификатор пользователя>\nДобавляет в список пользователей указанного пользователя""")
    elif args[0] == "removeuser":
        update.message.reply_text("""/removeuser <идентификатор пользователя>\nУдаляет из списка пользователей указанного пользователя""")
    elif args[0] == "users":
        update.message.reply_text("""Выводит список всех пользователей бота""")
    elif args[0] == "promote":
        update.message.reply_text("""/promote <идентификатор пользователя>\nПовышение пользователя до администратора""")
    elif args[0] == "broadcast":
        update.message.reply_text("""Рассылка сообщения всем пользователям бота.\nТекст сообщения нужно указать через пробел после команды.""")
    else:
        update.message.reply_text("Я не знаю ответа на этот вопрос")


dispatcher.add_handler(CommandHandler('help', help_callback, pass_args=True))



@restricted_admins
def adduser_callback(bot, update, args):
    bot.send_message(chat_id=update.message.chat_id, text="Еще не реализовано, ждите")

dispatcher.add_handler(CommandHandler('adduser', adduser_callback, pass_args=True))

def adduser_button_callback(bot, update):
    query = update.callback_query
    bot.send_message(chat_id=query.message.chat_id, text="Когда-нибудь я научусь добавлять :P")

dispatcher.add_handler(CallbackQueryHandler(adduser_button_callback,  pattern='^adduser'))

@restricted_admins
def removeuser_callback(bot, update, args):
    bot.send_message(chat_id=update.message.chat_id, text="Еще не реализовано, ждите")

dispatcher.add_handler(CommandHandler('removeuser', removeuser_callback, pass_args=True))



@restricted_admins
def users_callback(bot, update):
    userlist = ""
    for user in users.values():
        if user['id'] in LIST_OF_ADMINS:
            userlist = userlist + "* "
        userlist = userlist + user['name'] + "\n"
    bot.send_message(chat_id=update.message.chat_id, text="Список пользователей:\n" + userlist)

dispatcher.add_handler(CommandHandler('users', users_callback))



@restricted_admins
def promote_callback(bot, update, args):
    bot.send_message(chat_id=update.message.chat_id, text="Еще не реализовано, ждите")

dispatcher.add_handler(CommandHandler('promote', promote_callback, pass_args=True))



@restricted_admins
def broadcast_callback(bot, update, args):
    msg = ' '.join(args)
    broadcast_to_admins(bot, msg)

dispatcher.add_handler(CommandHandler('broadcast', broadcast_callback, pass_args=True))



def echo_callback(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Вы написали: " + update.message.text)

dispatcher.add_handler(MessageHandler(Filters.text, echo_callback))


def screenshot_parse(bot, update, photo_file):
    # получить скрин с энкой
    try:        
        filename = os.path.join('downloads', '{}.jpg'.format(photo_file.file_id))
        photo_file.download(filename)
        update.message.reply_text("Получил скриншот, пытаюсь найти в нем результаты энки. Пожалуйста, подождите...")
    except:
        update.message.reply_text("Не удалось получить скриншот: " + repr(sys.exc_info()[0]))
    # распознать
    #try:
    #    text = ocr_tickets(filename)
    #    result = parse_tickets(text)
    #    update.message.reply_text("Содержимое: " + str(result))
    #except:
    #    update.message.reply_text("Не удалось распознать энку: " + repr(sys.exc_info()[0]))


@restricted_users
def screenshot_callback(bot, update):    
    update.message.reply_text(repr(update.message.photo))
    #update.message.reply_text("Скриншотово получено: %d. Начинаю обработку..." % len(update.message.photo))
    #for photo in update.message.photos
    #  screenshot_parse(bot, update, bot.getFile(photo.file_id))

dispatcher.add_handler(MessageHandler(Filters.photo, screenshot_callback))



def stop_and_restart():
    """Gracefully stop the Updater and replace the current process with a new one"""
    updater.stop()
    os.execl(sys.executable, sys.executable, *sys.argv)

def restart(bot, update):
    logging.info('Бот перезапускается...')
    update.message.reply_text('Бот перезапускается...')
    Thread(target=stop_and_restart).start()

dispatcher.add_handler(CommandHandler('restart', restart, filters=Filters.user(username=SUPERUSER)))



def unknown_callback(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Какая-то левая команда, не знаю такую")

dispatcher.add_handler(MessageHandler(Filters.command, unknown_callback))



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



logging.info('Запускаю бота...')
updater.start_polling()
updater.idle()