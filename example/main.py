import callback_rooms
import message_rooms
import tgusers
import config

from tgusers import PostgresAuthData


class Tokens(tgusers.Table):
    pass


# Auth to postgres and telegram
auth_data = PostgresAuthData(dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD,
                             host=config.DB_HOST, port=config.DB_PORT)

rooms = tgusers.Rooms(pgData=auth_data, bot_token=config.BOT_TOKEN, message_logging=True, antispam=True)

# upload rooms (alternative of import)
rooms.upload_rooms(message_rooms.message_rooms)
rooms.upload_rooms(callback_rooms.rooms)

tables = rooms.tables

args = tgusers.ArgumentsContainer()
args.add_arguments_to_room("start",
                           {
                               int: 10
                           })

rooms.upload_external_arguments(args)

# Add roles
rooms.add_role("admin", config.ADMINS)

# Add table to tables
tables.tokens = Tokens("Tokens", rooms.db)

rooms.telegram_bot.polling()
