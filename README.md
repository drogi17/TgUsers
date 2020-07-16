## Contents
* [About the Project](#about-the-project)
* [How to Install](#how-to-install)
* [Quick Start](#quick-start)
* [TgUsers](#tgusers)
    * [Rooms](#rooms)
    * [RoomsContainer](#roomscontainer)

## About The Project
###### [ru]
Проект создан для упрощения взаимодействия с пользователем, через использование "Комнат".
Основной идеей является то, что пользователь может находится в различных частях программы, на что бот будет отвечать по разному. 
Прмер: 
Вам нужно чтобы программа на сообщение "/get" в одном случае отправляла файл с базой данных Пентагона(только пользователю с полномочиями "root"),
а во втором случае - отправлялась фотогафия кота(обычному пользователю). 

## How to Install
#### Windows: 
```
pip install tgusers
```
#### Unix: 
```
pip3 install tgusers
```

## Quick Start
#### Simple template:
First you must import everything you need:
```python
import tgusers

from aiogram import types
from tgusers import PostgresAuthData
```

Next, you must log in to the database (PostgreSQL) and telegram bot (Get telegram bot token):
```python
# PostgreSQL auth data
auth_data = PostgresAuthData(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
                             host=DB_HOST, port=DB_PORT)
# Make instance of tgusers.Rooms
rooms = tgusers.Rooms(pgData=auth_data, bot_token=BOT_TOKEN, message_logging=True, antispam=True)
```

The next step in creating a bot is to add rooms. There are several types: Callback and Message.
There must always be a "start" room in the program. A new user appears in it.
Function annotations are used to get arguments.
```python
@message_rooms.add_message_room("start", content_type=["text"])
async def start(message: types.Message):
    await message.answer("Start")
```

The arguments to the "add_message_room" function are:
```python
name: str # Name of the room the user will go to. 
content_type: list[str] = [] # The types of messages this room will process
roles: list[str] = ["all"] # roles of users who can visit this room
is_global: bool = False # Does the user need to be in this room to interact with her
```

## TgUsers
### Rooms
 * About: <br>
     The main class.
 * Arguments:
     * bot_token: str
     * pgData: PostgresAuthData
     * message_logging: bool = False
     * get_alerts: bool = False
     * antispam: bool = False
 * @Rooms.add_message_room
     * Arguments:
         * name: str
         * content_type: list = None
         * roles: list = None
         * is_global: bool = False
     * About:<br>
         Adding "message" rooms. Arguments to the function are passed through annotations.
         Room names may be repeated.
 * @Rooms.add_callback_room
     * Arguments:
         * name: str
         * is_global: bool = False
     * About:<br>
         Adding "message" rooms. Arguments to the function are passed through annotations.
         Room names may be repeated.
 * @Rooms.on_join_room
     * Arguments:
         * name: str
     * About:<br>
         This function will be executed when the user switches to a new room.
         Adding "message" rooms. Arguments to the function are passed through annotations.
         Room names may be repeated.
 * Rooms.add_role
     * Arguments:
         * role: str
         * users: list # Telegram id's
     * About:<br>
          Adding roles to users.
 * Rooms.get_user_role
     * Arguments:
         * user_id: int
     * About:<br>
         Get user role by telegram id.
 * Rooms.user_go_to_room
     * Arguments:
         message: types.Message
         room_name: str
     * About:<br>
         Move the user to a room named "room_name".
 * Rooms.go_to_one_of_the_rooms
     * Arguments:
         message: types.Message
         rooms_dict: dict
     * About:<br>
         Move the user to one of the rooms, depending on the message sent. Dict structure: 
         ```python
         go_rooms = {
             "message_text": "rooma_name",
             "/message_text": "rooma_name2",
         }
         ```
 * Rooms.upload_rooms
     * Arguments:
         * rooms_container: RoomsContainer
     * About:<br>
         Load rooms from other files.
### RoomsContainer
 * About:<br>
     Rooms to be connected to the main "Rooms" module.
 * Arguments:
     No arguments
 * @RoomsContainer.add_message_room
     * Arguments:
         * name: str
         * content_type: list = None
         * roles: list = None
         * is_global: bool = False
     * About:<br>
         Adding "message" rooms. Arguments to the function are passed through annotations.
         Room names may be repeated.
 * @RoomsContainer.add_callback_room
     * Arguments:
         * name: str
         * is_global: bool = False
     * About:<br>
         Adding "message" rooms. Arguments to the function are passed through annotations.
         Room names may be repeated.
 * @RoomsContainer.on_join_room
     * Arguments:
         * name: str
     * About:<br>
         This function will be executed when the user switches to a new room.
         Adding "message" rooms. Arguments to the function are passed through annotations.
         Room names may be repeated.
 * Rooms.upload_rooms
     * Arguments:
         * rooms_container: RoomsContainer
     * About:<br>
         Load rooms from other files.
