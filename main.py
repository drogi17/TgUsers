import tgusers
import config

from tgusers import PostgresAuthData

auth_data = PostgresAuthData(dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD, host=config.DB_HOST, port=config.DB_PORT)
connect = tgusers.Connect(pgData=auth_data,
                          bot_token=config.BOT_TOKEN,
                          message_logging=True)
rooms = connect.rooms


@rooms.add_room("start", content_type=["text", "photo"])
def start(message, tables):
    print("Start_room")


connect.telegram_bot.bot.polling()
