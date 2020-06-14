from dataclasses import dataclass


"""
Room content type can be in range of ['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker']
"""


@dataclass
class Room:
    name: str
    content_type: list
    permissions: list
    function: any


class Rooms:
    def __init__(self):
        self.rooms = {}

    def add_room(self, name, content_type: list = None, permissions: list = None):
        if permissions is None:
            permissions = []
        if content_type is None:
            content_type = []

        def append_to_rooms(room_func):
            room = Room(name=name, content_type=content_type, permissions=permissions, function=room_func)
            self.rooms[name] = room

        return append_to_rooms

    def show_rooms(self):
        print(self.rooms)
