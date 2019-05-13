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
room_service = chat.RoomService()
list_of_clients=[]

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

def broadcast_room(message,conn,room_number):
    room = room_service.search_room(room_number)
    for client in room.get_all_players():
        if client != conn:
            client.send(message)

def clienthread(addr,conn):
    while True:
        try:
            message = conn.recv(4096)
            message = pickle.loads(message)
            # print(message)
            message_to_send = {}
            message_to_send["sender"] = message["sender"]
            message_to_send["body"] = message["body"].strip()
            if message.get("room_number",None) != None:
                print("debug")
                message_to_send = pickle.dumps(message_to_send) 
                broadcast_room(message_to_send,conn,message["room_number"])
                continue    
            if message["body"].strip().lower() == "quick_room":
                message_to_send["sender"] = "admin"
                room = room_service.join_quick_room(conn)
                message_to_send["body"] = "Welcome to Room Number "+str(room.get_room_number())
                message_to_send["room_number"] = room.get_room_number()
                message_to_send = pickle.dumps(message_to_send)
                list_of_clients.remove(conn)
                conn.send(message_to_send)
                continue
            elif message["body"].strip().split()[0].lower() == "create_custom_room":
                message_to_send["sender"] = "admin"
                room_number = int(message["body"].strip().split()[1])
                room = room_service.create_custom_room(conn,room_number)
                if room == None:
                    message_to_send["body"] = "Sorry, Currently Room Number "+str(room_number)+" is Already Exist"
                else:
                    message_to_send["body"] = "Welcome to Room Number "+str(room_number)
                    message_to_send["room_number"] = room_number
                    list_of_clients.remove(conn)
                message_to_send = pickle.dumps(message_to_send)
                conn.send(message_to_send)     
                continue
            message_to_send = pickle.dumps(message_to_send)
            broadcast(message_to_send,conn)
        except:
            continue


while True:
    conn,addr = server.accept()
    list_of_clients.append(conn)
    print(addr[0]+" connected")
    message = {}
    message["sender"] = "admin"
    player_name = "Player"+ str(random.randint(100000,999999))
    message["player_name"] = player_name
    message["body"] = "\n quick_room = to join random room \n create_custom_room <int> = to create custom room \nWelcome "+player_name
    conn.send(pickle.dumps(message))
    t=threading.Thread(target=clienthread,args=(addr,conn))
    t.start()

conn.close()
server.close()