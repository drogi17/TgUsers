
# TgUsers
<!--ts-->
   * [Main idea](#Main_idea)
   *  [Code run](#Code_run)
   * [Help_TgUsers](#Help_TgUsers)
	   * [Launch](#Launch)
        * [CreateDataBase](#CreateDataBase )
        * [AddColumnDataBase](#AddColumnDataBase)
        * [TgUsers.save_message(message)](#TgUsers.save_message(message))
   * [Help_rooms](#Help_rooms)
	   * [Main Function](#Main_function)
	   * [Room_Creation](#Room_сreation)
	   * [Getting_rooms](#Getting_rooms)
<!--te-->


# Main_idea
Program is based on the idea of user interaction, which can be in one place of the program (room). If a person is in the room (Alpha) and sends some commands to the bot, then these commands will not apply to the rooms of the room (Beta, Gama).
### Example:
Room 1 answers the message "Hello" - "Hi", and the second room - the message "Hello" - "Gladiolus". If the user is in room 1, then the bot will send a “Hello” message to the message with the text “Hi”, and in the second - “Gladiolus”.

# Code_run
```sh
python3 main.py
```
After starting, a database file and a file with contacts will be generated.

# Help_TgUsers
### CreateDataBase
Creating a standard database. 
```python3
CreateDataBase(database)
```
> Arguments: 
> 1. database name

##
### AddColumnDataBase
Adding a column to an existing database
```python3
column = {'name': 'str', 'old': 'int'}
AddColumnDataBase(database, 'users', column)
```
> Arguments: 
> 1. database name
> 2. Table name
> 3. Columns to add
##
### Launch
``` python3
languages = ['ru', 'en']
TgUsers	= TgUsers(database=database, languages=languages)
```
> Arguments: 
> 1. Database file dir
> 2. Languages list
##
### TgUsers.save_message(message)
Function to save message data. If the user is not included in the database, the program automatically writes it.
```python3
TgUsers.save_message(message)
```
> Arguments: 
> 1. Message that the user sent (inoriginal form).
##
### TgUsers.get_user_room_by_telegram_id
Getting the room where user is located.
```python3
TgUsers.get_user_room_by_telegram_id(message=message)
```
or
```python3
TgUsers.get_user_room_by_telegram_id(telegram_id=message.chat.id)
```
> Arguments: 
> 1. User message or user id

# Help_rooms
### Main_function
```python3
def __init__(self, TgUsers, bot, vocabulary):
        self.TgUsers 		 = TgUsers
        self.bot             = bot
        self.vocabulary      = vocabulary
```
##
### Room_сreation
To create a new room, you need to add a new function to the room class.
```python3
def start(self, message):
	lang = self.TgUsers.get_user_language(message)
	self.bot.send_message(message.chat.id, self.vocabulary['start']['1'][lang] % message.from_user.username)
```
> Arguments: 
> 1. Message from user
##
### Getting_rooms
To get a room, you first need to get a function with all the rooms.
```python3
bot	= telebot.TeleBot(api_key, threaded=True)
rooms	= rooms(TgUsers, bot, vocabulary)
```
> Arguments: 
> 1. TgUsers
> 2. bot
> 3. List of translations

Getting rooms
```python3
rooms.function_name(message)
```
> Arguments: 
> 1. Message that the user sent (inoriginal form).
