import socket
import select
import sys
import threading
import os
import zipfile
import pickle
import chat
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

ip_address = '127.0.0.1'

port = 5000

server.bind((ip_address,port))
server.listen(10)

list_of_clients=[]
# list_of_rooms=[]
def broadcast(message, room, conn ):
    for clients in room.get_all_players():
        if(clients!=conn):
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)
                room.removePlayers(conn)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def clienthread(room,conn):
    while True:
        try:
            message = conn.recv(4096)
            message = pickle.loads(message)
            message_to_send = {}
            message_to_send["sender"] = message["sender"]
            message_to_send["body"] = "<" + message["sender"]+ "> : "+ message["body"].strip() 
            message_to_send["type"] = "msg"
            message_to_send = pickle.dumps(message_to_send)
            broadcast(message_to_send,room,conn)
        except:
            continue

chat_service = chat.RoomService()
while True:
    conn,addr = server.accept()
    room_number ,room = chat_service.get_available_room()
    room.add_player(conn)
    list_of_clients.append(conn)
    print(addr[0]+" connected")
    message = {}
    message["sender"] = "admin"
    message["type"] = "msg"
    message["player_name"] = "Player "+ str(room.get_current_player_number())
    message["body"] = "Welcome to Room "+ str(room_number)
    conn.send(pickle.dumps(message))
    # if(not room_number in list_of_rooms):
    #     list_of_rooms.append(room_number)
    t=threading.Thread(target=clienthread,args=(room,conn))
    t.start()

conn.close()
server.close()