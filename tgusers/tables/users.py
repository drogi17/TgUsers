import tgusers

from dataclasses import dataclass


@dataclass
class User:
    telegram_id: int
    first_name: str
    last_name: str
    user_name: str
    phone: str
    language: str
    permissions: str
    room: str
    id: int = -1


class Users(tgusers.Table):
    create_table = """
        CREATE TABLE public."Users"
        (
            id SERIAL PRIMARY KEY,
            "telegram_id" integer,
            "first_name" character varying(500),
            "last_name" character varying(500),
            "user_name" character varying(500),
            "phone" character varying(500),
            "language" character varying(500),
            "permissions" character varying(500),
            "room" character varying(500) DEFAULT 'start'
        )

        TABLESPACE pg_default;

        ALTER TABLE public."Users"
            OWNER to "Admin";
    """

    def get_user_room(self, message):
        sql = """
                    SELECT room
                    FROM "Users"
                    WHERE telegram_id = %s;
        """
        return self.db.request(sql, (message.chat.id,))[0].get("room")

    def check_user_for_registration(self, message):
        sql = """
                    SELECT id
                    FROM "Users"
                    WHERE telegram_id = %s;
                """
        if self.db.request(sql, (message.chat.id,)):
            return True
        else:
            return False

    def get_user(self, message):
        sql = """
                    SELECT id, telegram_id, first_name, last_name, user_name, phone, language, permissions, room
                    FROM "Users"
                    WHERE telegram_id = %s;
                """
        response = self.db.request(sql, (message.chat.id,))[0]
        return User(**response)

    def add(self, user: User):
        sql = """   INSERT INTO "Users" (telegram_id, first_name, last_name, user_name, phone, language, permissions, room)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
        """
        response = self.db.request(sql, (
            user.telegram_id, user.first_name, user.last_name, user.user_name, user.phone, user.language,
            user.permissions, user.room))
        self.db.commit()
        return response
