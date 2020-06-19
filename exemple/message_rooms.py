from aiogram import types
from tgusers import Rooms


rooms = Rooms()


@rooms.add_message_room("start", content_type=["text"])
async def start(message: types.Message):
    # command -> room
    go_rooms = {
        "/say_hi": "say_hi",
        "/admin_panel": "admin_panel",
    }
    # walking between rooms
    if await rooms.go_to_one_of_the_rooms(message, go_rooms): return
    await message.answer(", ".join(go_rooms.keys()) + "\nStart")
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("Keyboard", callback_data="111111"),
    )
    await message.answer("Markup", reply_markup=markup)


@rooms.add_message_room("say_hi", content_type=["text"])
async def say_hi(message: types.Message):
    go_rooms = {
        "/start": "start"
    }
    if await rooms.go_to_one_of_the_rooms(message, go_rooms): return
    await message.answer(", ".join(go_rooms.keys()) + "\nHi")
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("Keyboard", callback_data="222222"),
    )
    await message.answer("Markup", reply_markup=markup)


@rooms.add_message_room("admin_panel", content_type=["text"], roles=["admin"])
async def admin_panel(message: types.Message):
    go_rooms = {
        "/start": "start",
        "/say_hi": "say_hi"
    }
    if await rooms.go_to_one_of_the_rooms(message, go_rooms): return
    await message.answer(", ".join(go_rooms.keys()) + "\nAdmin text")


@rooms.add_message_room("admin_panel", content_type=["photo"], roles=["admin"])
async def admin_panel(message: types.Message):
    go_rooms = {
        "/start": "start",
        "/say_hi": "say_hi"
    }
    if await rooms.go_to_one_of_the_rooms(message, go_rooms): return
    await message.answer(", ".join(go_rooms.keys()) + "\nAdmin photo")


@rooms.on_join_room("start")
async def start(chat_id):
    await rooms.telegram_bot.bot.send_message(chat_id, "HELLO IN START")


@rooms.add_message_room(content_type=["text"], is_global=True)
async def global_hi(message: types.Message):
    await rooms.telegram_bot.bot.send_message(message.chat.id, "Hi from global")
