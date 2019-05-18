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
# list_of_clients = []
# def broadcast(message, conn):
#     for client in list_of_clients:
#         if(client != conn):
#             try:
#                 client.send(message)
#             except:
#                 client.close()
#                 remove(client)

# def remove(connection):
#     if connection in list_of_clients:
#         list_of_clients.remove(connection)

def broadcast_room(message,conn,theroom=False,room_number=False,ttype=False):
    if(room_number):
        room = room_service.search_room(room_number)
        if(ttype=="notify_quit"):
            message['body']=str(room.get_current_player_number())
            message['response']="qroom_update_players"
            message=pickle.dumps(message)
    if(theroom):
        room = theroom
    for client in room.get_all_players():
        if client != conn:
            client.send(message)

def clienthread(addr,conn):
    while True:
        try:
            message = conn.recv(4096)
            message = pickle.loads(message)
            print(message)
            message_to_send = {}
            message_to_send["sender"] = message["sender"]
            message_to_send["body"] = message["body"].strip()
            if message['type']=="exit":
                room_service.quit(conn,message['room_number'])
                conn.close()
                continue
            
            if message.get("room_number",None) != None:
                if message["body"].strip().lower() == "quit":
                    room_service.quit_room(conn,message["room_number"])
                    message_to_send['response']="quit_succeed"
                    message_to_send["room_number"] = "None"
                    message_to_send["body"] = "quit"
                    message_to_send_pickle = pickle.dumps(message_to_send) 
                    conn.send(message_to_send_pickle)
                broadcast_room(message_to_send,conn,room_number=message["room_number"],ttype="notify_quit")
                continue
            else:    
                if message["body"].strip().lower() == "quick_room":
                    message_to_send["sender"] = "admin"
                    room = room_service.join_quick_room(conn)
                    players = room.get_current_player_number()
                    message_to_send['response']="quick_room_joined"
                    message_to_send["body"] = players
                    message_to_send["room_number"] = room.get_room_number()
                    message_to_send_pickle = pickle.dumps(message_to_send)
                    conn.send(message_to_send_pickle)
                    
                    message_to_send['response']="qroom_update_players"
                    message_to_send['body']=str(players)
                    message_to_send_pickle = pickle.dumps(message_to_send)
                    broadcast_room(message_to_send_pickle,conn,theroom=room)
                    continue
                elif message["body"].strip().split()[0].lower() == "create_custom_room":
                    message_to_send["sender"] = "admin"
                    room_number = int(message["body"].strip().split()[1])
                    room = room_service.create_custom_room(conn)
                    message_to_send["body"] = "create_custom_room"
                    message_to_send['response'] = "create_custom_room_succeed"
                    message_to_send["room_number"] = room.get_room_number()
                    message_to_send = pickle.dumps(message_to_send)
                    conn.send(message_to_send)     
                    continue
                elif message["body"].strip().split()[0].lower() == "join_custom_room":
                    message_to_send["sender"] = "admin"
                    room_number = int(message["body"].strip().split()[1])
                    room = room_service.join_room(conn, room_number=room_number)
                    if room == None:
                        message_to_send['response'] = "join_custom_room_failed"
                        message_to_send["body"] = "Sorry, Cant Join Room Number "+str(room_number)
                    else:
                        message_to_send['response'] = "join_custom_room_succeed"
                        message_to_send["body"] = "Welcome to Room Number "+str(room_number)
                        message_to_send["room_number"] = room_number
                    message_to_send = pickle.dumps(message_to_send)
                    conn.send(message_to_send)
                    continue
        except:
            continue


while True:
    conn,addr = server.accept()
    # list_of_clients.append(conn)
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