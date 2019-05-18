class RoomService:
    def __init__(self):
        self.rooms = []
    
    def add_room(self,room):
        self.rooms.append(room)

    def join_quick_room(self,conn):
        room = self.get_available_room()
        room.add_player(conn)
        return room

    def create_custom_room(self,conn,room_number):
        room_found = self.search_room(room_number)
        if (room_found == None):
            room_found = Room(room_number)
            self.rooms.append(room_found)
            room_found.add_player(conn)
            return room_found
        else:
            return None

    def search_room(self, room_number):
        found_room = None
        for room in self.rooms:
            if (room.get_room_number() == room_number):
                found_room = room
                break
        return found_room

    def get_available_room(self):
        is_found = False
        selected_room = None
        selected_room_number = 1
        if(len(self.rooms)):
            for room in self.rooms:
                is_found = not(room.get_is_full())
                if(is_found):
                    selected_room = room
                    return selected_room
                selected_room_number += 1
        room = Room(selected_room_number)
        selected_room = room
        self.rooms.append(selected_room)
        return selected_room
    
    def join_room(self,conn,room_number):
        room = self.search_room(room_number)
        if room == None:
            return None
        roomIsFull = room.get_is_full()
        if roomIsFull:
            return None
        room.add_player(conn)
        return room


    def get_all_player_by_room_number(self,room_number):
        room = self.search_room(room_number)
        players = room.get_all_players()
        return players

    def quit_room(self,conn,room_number):
        room = self.search_room(room_number)
        room.remove_player(conn)
        if(room.get_current_player_number() == 0):
            self.rooms.remove(room)

class Room:
    def __init__(self, number):
        self.number = number
        self.players = []
        self.is_full = False
    
    def get_room_number(self):
        return self.number

    def add_player(self, conn):
        self.players.append(conn)
        if(len(self.players) >= 4):
            self.is_full = True
    
    def get_all_players(self):
        return self.players

    def get_current_player_number(self):
        return len(self.players)
        
    def get_is_full(self):
        return self.is_full

    def remove_player(self,conn):
        self.players.remove(conn)
        if(len(self.players)<4):
            self.is_full=False