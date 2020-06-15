from dataclasses import dataclass


"""
Room content type can be in range of ['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker']
"""


@dataclass
class Room:
    name: str
    content_type: list
    roles: list
    function: any


class RoomsAlerts:
    @staticmethod
    def access_denied():
        return "Access denied"


class Rooms:
    def __init__(self, tables):
        self.rooms = {}
        self.tables = tables

    def add_room(self, name, content_type: list = None, roles: list = None):
        if roles is None:
            roles = ["all"]
        if content_type is None:
            content_type = []

        def append_to_rooms(room_func):
            room = Room(name=name, content_type=content_type, roles=roles, function=room_func)
            self.rooms[name] = room

        return append_to_rooms

    def user_go_to_room(self, message, room_name: str):
        if self.tables.users.get_user_role(message) in self.rooms.get(room_name).roles or "all" in self.rooms.get(room_name).roles:
            if self.tables.users.set_room(message, self.rooms.keys(), room_name):
                return True
            else:
                return False
        else:
            return False

    def go_to_one_of_the_rooms(self, message, rooms_dict: dict):
        get_room = rooms_dict.get(message.text)
        if get_room:
            self.user_go_to_room(message, get_room)
            return True
        else:
            return False

    def show_rooms(self):
        print(self.rooms)
