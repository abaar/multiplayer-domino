class RoomService:
    def __init__(self):
        self.rooms = []
    
    def add_room(self,room):
        self.rooms.append(room)

    def join_quick_room(self,conn):
        room = self.get_available_room()
        room.add_player(conn)
        return room

    def create_custom_room(self,conn):
        rom = Room(len(self.rooms)+1)
        self.rooms.append(rom)
        rom.add_player(conn)
        return rom

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

class Room:
    def __init__(self, number):
        self.number = number
        self.players = []
        self.is_full = False
        self.participants = ["1","0","0","0"]
        self.p1=None
        self.p2=None
        self.p3=None
        self.p4=None

    def get_room_number(self):
        return self.number

    def add_player(self, conn):
        self.players.append(conn)
        if(len(self.players) >= 4):
            self.is_full = True
        if(self.p1==None):
            self.p1=conn
            self.participants[0]="1"
        elif(self.p2==None):
            self.p2=conn
            self.participants[1]="1"
        elif(self.p3==None):
            self.p3=conn
            self.participants[2]="1"
        elif(self.p4==None):
            self.p4=conn
            self.participants[3]="1"

    def get_all_players(self):
        return self.players

    def get_current_player_number(self):
        return len(self.players)
        
    def get_is_full(self):
        return self.is_full
    
    def get_participants(self):
        return self.participants

    def remove_player(self,conn):
        self.players.remove(conn)
        if(self.p1==conn):
            self.p1=None
            self.participants[0]="0"
        elif(self.p2==conn):
            self.p2=None
            self.participants[1]="0"
        elif(self.p3==conn):
            self.p3=None
            self.participants[2]="0"
        elif(self.p4==conn):
            self.p4=None 
            self.participants[3]="0"

        if(len(self.players)<4):
            self.is_full=False
    
    def get_my_order(self,conn):
        if(self.p1==conn):
            return "1"
        elif(self.p2==conn):
            return "2"
        elif(self.p3==conn):
            return "3"
        elif(self.p4==conn):
            return "4" 

    def kick_this(self,player):
        try:
            conn=None
            if(player=="2"):
                conn=self.p2
                self.remove_player(self.p2)
                self.p2=None
            elif(player=="3"):
                conn=self.p3
                self.remove_player(self.p3)
                self.p3=None
            elif(player=="4"):
                conn=self.p4
                self.remove_player(self.p4)
                self.p4=None
            return conn
        except:
            return False