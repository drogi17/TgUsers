import tgusers
import config

from aiogram import types
from tgusers import PostgresAuthData


class Tokens(tgusers.Table):
    pass


# Auth to postgres and telegram
auth_data = PostgresAuthData(dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD,
                             host=config.DB_HOST, port=config.DB_PORT)
connect = tgusers.Connect(pgData=auth_data, bot_token=config.BOT_TOKEN, message_logging=True)
rooms = connect.rooms
tables = connect.tables


# Add roles
admins = ["462969888"]
rooms.add_role("admin", admins)


# Add table to tables
tables.tokens = Tokens("Tokens", connect.data_base)


# The "start" room should be in any program, since this is the default room
@rooms.add_message_room("start", content_type=["text"])
async def start(message: types.Message):
    # command -> room
    go_rooms = {
        "/say_hi": "say_hi",
        "/admin_panel": "admin_panel",
    }
    # walking between rooms
    if connect.telegram_bot.rooms.go_to_one_of_the_rooms(message, go_rooms): return
    await message.answer("Start")


@rooms.add_message_room("say_hi", content_type=["text"])
async def say_hi(message: types.Message):
    go_rooms = {
        "/start": "start"
    }
    if connect.telegram_bot.rooms.go_to_one_of_the_rooms(message, go_rooms): return
    await message.answer("Hi")


@rooms.add_message_room("admin_panel", content_type=["text"], roles=["admin"])
async def say_hi(message: types.Message):
    go_rooms = {
        "/start": "start",
        "/say_hi": "say_hi"
    }
    if connect.telegram_bot.rooms.go_to_one_of_the_rooms(message, go_rooms): return
    await message.answer("Admin")


@rooms.add_message_room("admin_panel", content_type=["text"], roles=["admin"])
async def say_hi(message: types.Message):
    go_rooms = {
        "/start": "start",
        "/say_hi": "say_hi"
    }
    if connect.telegram_bot.rooms.go_to_one_of_the_rooms(message, go_rooms): return
    await message.answer("Admin")



@rooms.add_message_room(content_type=["text"], roles=["admin"], is_global=True)
async def global_hi(message: types.Message):
    await connect.telegram_bot.bot.send_message(message.chat.id, "hi from global")


connect.telegram_bot.polling()