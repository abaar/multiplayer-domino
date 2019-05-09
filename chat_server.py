import socket
import select
import sys
import threading
import os
import zipfile
import pickle
import chat
import random

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

ip_address = '127.0.0.1'

port = 5000

server.bind((ip_address,port))
server.listen(10)

list_of_clients=[]
def broadcast_room(message,room, conn ):
    for clients in room.get_all_players():
        if(clients!=conn):
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)
                room.removePlayers(conn)

def broadcast(message, conn):
    for client in list_of_clients:
        if(client != conn):
            try:
                client.send(message)
            except:
                client.close()
                remove(client)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def clienthread(addr,conn):
    while True:
        try:
            message = conn.recv(4096)
            message = pickle.loads(message)
            print(message)
            message_to_send = {}
            message_to_send["sender"] = message["sender"]
            message_to_send["body"] = message["body"].strip() 
            message_to_send["type"] = "msg"
            if message["body"].strip().lower() == "quick":
                print("quick")
                message_to_send["sender"] = "admin"
                room_number = quick_room(conn)
                message_to_send["body"] = "Welcome to Room Number "+str(room_number)
                message_to_send = pickle.dumps(message_to_send)
                conn.send(message_to_send)
                continue
            message_to_send = pickle.dumps(message_to_send)
            broadcast(message_to_send,conn)
        except:
            continue

def quick_room(conn):
    room_number ,room = chat_service.get_available_room()
    room.add_player(conn)
    return room_number

def create_room():
    print("World")

chat_service = chat.RoomService()
while True:
    conn,addr = server.accept()
    list_of_clients.append(conn)
    print(addr[0]+" connected")
    message = {}
    message["sender"] = "admin"
    message["type"] = "msg"
    player_name = "Player"+ str(random.randint(100000,999999))
    message["player_name"] = player_name
    message["body"] = "Welcome "+player_name
    conn.send(pickle.dumps(message))
    t=threading.Thread(target=clienthread,args=(addr,conn))
    t.start()

conn.close()
server.close()