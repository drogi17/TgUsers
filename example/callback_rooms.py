from aiogram import types
from tgusers import Rooms


rooms = Rooms()


@rooms.add_callback_room("start")
async def start(call: types.CallbackQuery):
    await call.answer("Start CallBack Call_data:" + call.data)


@rooms.add_callback_room("say_hi")
async def start(call: types.CallbackQuery):
    await call.answer("HI CallBack; Call_data:" + call.data)

