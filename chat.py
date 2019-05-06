class RoomService:
    def __init__(self):
        self.rooms = []
    
    def add_room(self,room):
        self.rooms = room

    def get_available_room(self):
        is_found = False
        selected_room = None
        selected_room_number = 1
        for room in self.rooms:
            is_found = not(room.get_is_full())
            if(is_found):
                selected_room = room
                break
            selected_room_number += 1
        if(is_found == False):
            room = Room()
            selected_room = room
            self.rooms.append(selected_room)
        return (selected_room_number,selected_room)

class Room:
    def __init__(self):
        self.players = []
        self.is_full = False
    
    def add_player(self, address_tuple):
        self.players.append(address_tuple)
        if(len(self.players) >= 4):
            self.is_full = True
    
    def get_all_players(self):
        return self.players

    def get_is_full(self):
        return self.is_full