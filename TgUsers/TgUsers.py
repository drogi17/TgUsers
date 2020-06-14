import telebot
from datetime import datetime
import sqlite3
import os.path
import sys

def CreateDataBase(database):
    ADD_messages_table = '''CREATE TABLE "messages" (
                            "id"    INTEGER,
                            "id_user"   INTEGER,
                            "message"   TEXT,
                            "message_id"  TEXT,
                            "time"  TEXT,
                            PRIMARY KEY("id")
                        );'''
    ADD_users_table = '''CREATE TABLE "users" (
                        "id"    INTEGER,
                        "t_id"  INTEGER,
                        "f_name"    TEXT,
                        "l_name"    TEXT,
                        "u_name"    TEXT,
                        "phone"     TEXT,
                        "language"  TEXT,
                        "status"    TEXT,
                        "room"      TEXT DEFAULT "start",
                        PRIMARY KEY("id")
                    );'''
    if '/' in database:
        database_dir = database.split('/')
        add_dir = ''
        num_b = 0
        while num_b <= len(database_dir)-2:
            os.makedirs(add_dir + database_dir[num_b], exist_ok=True)
            add_dir += database_dir[num_b] + '/'
            num_b += 1
    conn_n = sqlite3.connect(database, check_same_thread=False)
    cursor_n = conn_n.cursor()
    cursor_n.execute(ADD_messages_table)
    cursor_n.execute(ADD_users_table)
    conn_n.commit()
    conn_n.close()

def AddColumnDataBase(database, table, columns): #str str dict
    conn_n = sqlite3.connect(database, check_same_thread=False)
    cursor_n = conn_n.cursor()
    types = {   'TEXT': 'TEXT', 
                'text': 'TEXT', 
                'str': 'TEXT',  
                'INTEGER': 'INTEGER', 
                'integer': 'INTEGER', 
                'int': 'INTEGER'}
    for column in columns:
        try:
            ADD_column = 'ALTER TABLE "%s" ADD COLUMN "%s" %s' % ( table, column, types.get(columns.get(column)) )
            cursor_n.execute(ADD_column)
        except sqlite3.OperationalError:
            pass
    conn_n.commit()
    conn_n.close()



class TgUsers:
    __version__ = '3'
    __name__ = 'TgUsers'
    def __init__(self, bot, vocabulary, database=None, languages=None):
        if not database and not languages:
            database = None
            languages = None
        if not database:
                database = 'data/data.db'
        if not languages or not isinstance(languages, list):
            languages = ['en']
        if not os.path.exists(database):
            print('Database not found, use CreateDataBase to create the base database structure.')
            sys.exit()
        # elif not database and os.path.exists('data/data.db'):
        #     database = 'data/data.db'
        self.conn = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.languages = languages
        self.bot = bot
        self.vocabulary = vocabulary


    def sql_request(self, request, args=None):
        if args:
            request_data = self.cursor.execute(request, args).fetchall()
        else:
            request_data = self.cursor.execute(request).fetchall()
        self.conn.commit()
        return request_data


    def register_in_system(self, message):  #reg_on_system
        if not self.user_is_reged_in_system(message):
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name
            username = message.from_user.username
            self.add_user(message)
        return True

    def add_user(self, message):            #Добавить пользователя в базу
        user_id = message.chat.id
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        username = message.from_user.username
        try:
            self.cursor.execute(""" INSERT INTO users (t_id, f_name, l_name, u_name, language, status)
                                    VALUES (?,?,?,?, 'en', 'user');""",
                                    (user_id, first_name, last_name, username))
            self.conn.commit()
            return True
        except TypeError:
            return False


    def user_is_reged_in_system(self, message):                                   #Добавить сообщение в базу # is_reged_on_system
        if message.content_type == 'text':
            user_id = message.chat.id
            id_game = self.cursor.execute("""   SELECT id
                                                FROM users
                                                WHERE t_id = ?;""", (user_id, )).fetchall()
            if id_game:
                return True
        elif message.content_type == 'contact':
            user_id = message.from_user.id
            id_game = self.cursor.execute("""   SELECT id
                                                FROM users
                                                WHERE t_id = ?;""", (user_id, )).fetchall()
            if id_game:
                return True
        else:
            return False

    def message_log(self, message):                       #Запись данных в log
        try:
            if message.content_type == 'text':
                log_s = str(message.chat.id) + ': ' + str(message.text) + '  --  ' + str(datetime.now().strftime("%d.%m.%Y"))

                user_id = """   SELECT id
                                FROM users
                                WHERE t_id = ?;"""

                id_user = self.cursor.execute(user_id, (message.chat.id, )).fetchall()
                if not id_user:
                    id_user = 0
                else:
                    id_user = id_user[0][0]
                self.cursor.execute(""" INSERT INTO messages (id_user, message, message_id, time)
                                        VALUES (?,?,?,?);""",
                                        (id_user, message.text, message.message_id, datetime.now().strftime("%d.%m.%Y")))
                self.conn.commit()
                print(log_s)
                return True
            elif message.content_type == 'contact':
                log_s = str(message.from_user.id) + ': ' + 'contact' + '  --  ' + str(datetime.now().strftime("%d.%m.%Y"))

                user_id = """   SELECT id
                                FROM users
                                WHERE t_id = ?;"""

                id_user = self.cursor.execute(user_id, (message.from_user.id, )).fetchall()
                if not id_user:
                    id_user = 0
                else:
                    id_user = id_user[0][0]
                self.cursor.execute(""" INSERT INTO messages (id_user, message, time)
                                        VALUES ( ?, 'contact', ?);""",
                                        (id_user, datetime.now().strftime("%d.%m.%Y")))
                self.conn.commit()
                print(log_s)
                return True
        except TypeError:
            return False


    def get_user_staus(self, message, status_list):                                     #Проверка на админа  have_status
        if self.user_is_reged_in_system(message.chat.id):
            admin = self.cursor.execute(""" SELECT status
                                            FROM users
                                            WHERE t_id = ?;""", (message.chat.id, )).fetchall()
            if str(admin[0][0]) in status_list:
                return (True, str(admin[0][0]))
            else:
                return (False, 'Incorrect_status')
        else:
            return (False, 'not_reg')

    def set_user_language(self, message, lang): # set_language
        if lang in self.languages:
            sql =   """ UPDATE users 
                        SET language = ?
                        WHERE t_id = ?;"""

            self.cursor.execute(sql, (lang, message.chat.id))
            self.conn.commit()
            return True
        else:
            return False


    def get_user_language(self, message):                                         #Получить язык пользователя #get_usr_lang
        lang = self.cursor.execute("""  SELECT language
                                        FROM users
                                        WHERE t_id = ?;""", (message.chat.id, )).fetchall()
        return lang[0][0]

    def is_reged_on_telegram(self, message_contact):                               #Проверить то, регестриован человек в телеграмме
        reg_status = {}
        if message_contact.user_id:
            reg_status['status'] = True
            reg_status['user_id'] = str(message_contact.user_id)
            reg_status['phone_number'] = str(message_contact.phone_number)
            reg_status['first_name'] = str(message_contact.first_name)
            reg_status['last_name'] = str(message_contact.last_name)
        else:
            reg_status['status'] = False
        return reg_status

    def add_phone(self, message):                                     #Проверка на админа
        if self.user_is_reged_in_system(message):
            message_contact = message.contact
            sql = """   UPDATE users 
                        SET phone = ?
                        WHERE t_id = ?;"""
            self.cursor.execute(sql, (message_contact.phone_number, message_contact.user_id))
            self.conn.commit()
            return [True]
        else:
            return [False, 'not_reg']

    def save_message(self, message):
        self.register_in_system(message)
        self.message_log(message)
        return True

    def get_user_by_telegram_id(self, message=None, telegram_id=None):
        list_data = []
        for name in self.cursor.execute("PRAGMA table_info(users);").fetchall():
            list_data.append(name[1])
        if message and not telegram_id:
            telegram_id = message.chat.id
        user_data_sql = """ SELECT *
                            FROM users
                            WHERE t_id = ?;"""
        user_data = self.cursor.execute(user_data_sql, (telegram_id, )).fetchall()
        if user_data:
            return dict(zip(list_data, list(user_data[0])))
        else:
            return False

    def get_user_room_by_telegram_id(self, message=None, telegram_id=None):
        if message and not telegram_id:
            telegram_id = message.chat.id
        user_data_sql = """ SELECT room
                            FROM users
                            WHERE t_id = ?;"""
        user_data = self.cursor.execute(user_data_sql, (telegram_id, )).fetchall()
        if user_data:
            return user_data[0][0]
        else:
            return False

    def go_to_room(self, message, room, keyboard=None):
        if self.user_is_reged_in_system(message):
            sql =   """ UPDATE users 
                        SET room = ?
                        WHERE t_id = ?;"""
            self.cursor.execute(sql, (room, message.chat.id))
            self.conn.commit()
            lang = self.get_user_language(message)
            if keyboard:
                self.bot.send_message(message.chat.id, str(self.vocabulary.get(room).get('1').get(lang)), reply_markup=keyboard)
            else:
                self.bot.send_message(message.chat.id, str(self.vocabulary.get(room).get('1').get(lang)))
            return True
        else:
            return False


try:
    if not os.path.exists('rooms/'):
        room_example = '''class rooms(object):
        def __init__(self, TgUsers, bot, vocabulary):
            self.TgUsers = TgUsers
            self.bot             = bot
            self.vocabulary      = vocabulary

        def start(self, message):
            lang = self.TgUsers.get_user_language(message)
            self.bot.send_message(message.chat.id, self.vocabulary['start']['1'][lang] % message.from_user.username)'''
        os.makedirs('rooms/')
        with open('rooms/rooms.py', 'w') as f:
            f.write(room_example)
except FileExistsError:
    pass
