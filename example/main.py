import message_rooms
import tgusers
import config

from aiogram import types
from tgusers import PostgresAuthData


class Tokens(tgusers.Table):
    pass


# Auth to postgres and telegram
auth_data = PostgresAuthData(dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD,
                             host=config.DB_HOST, port=config.DB_PORT)

rooms = tgusers.Rooms(pgData=auth_data, bot_token=config.BOT_TOKEN, message_logging=True, antispam=True)

# upload rooms (alternative of import)
rooms.upload_rooms(message_rooms.message_rooms)

tables = rooms.tables

# Add roles
rooms.add_role("admin", config.ADMINS)

# Add table to tables
tables.tokens = Tokens("Tokens", rooms.db)

# import rooms from file
import callback_rooms



rooms.telegram_bot.polling()
