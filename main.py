import telebot, os, sqlite3
from datetime import datetime
from telebot import types
from languages.data import vocabulary
from TgUsers.TgUsers import TgUsers, CreateDataBase, AddColumnDataBase
from config.config import config_const
from rooms.rooms import rooms


if not os.path.exists(config_const.data_base_file):
    CreateDataBase(config_const.data_base_file)

api_key             = config_const.api_key
bot                 = telebot.TeleBot(api_key, threaded=True)
TgUsers             = TgUsers(bot, vocabulary, database=config_const.data_base_file, languages=config_const.languages)
rooms               = rooms(TgUsers, bot, vocabulary)


@bot.message_handler(content_types=['text'])
def contact_handler(message):
    TgUsers.save_message(message)
    if TgUsers.get_user_room_by_telegram_id(message=message) == 'start':
        rooms.start(message)




print('STARTED')
if __name__ == '__main__':
    bot.polling()
