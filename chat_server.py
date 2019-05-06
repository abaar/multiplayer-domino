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
def broadcast(message, conn ):
    for clients in list_of_clients:
        if(clients!=conn):
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def clienthread(conn,addr):
    while True:
        try:
            message = conn.recv(4096)
            message = message.decode('utf-8')
            print("<" + str(addr[1]) +"> "+message.strip())
            message_to_send = "<" + str(addr[1]) +"> " + message
            broadcast(message_to_send, conn)            
        except:
            continue
chat_service = chat.RoomService()
while True:
    conn,addr = server.accept()
    room_number ,room = chat_service.get_available_room()
    room.add_player((conn,addr))
    # list_of_clients.append(conn)
    print(addr[0]+" connected")
    message = {}
    message["type"] = "msg"
    message["cache"] = str(room_number)
    message["body"] = "Welcome to Room "+ str(room_number)
    conn.send(pickle.dumps(message))
    t=threading.Thread(target=clienthread,args=(conn,addr,))
    t.start()

conn.close()
server.close()