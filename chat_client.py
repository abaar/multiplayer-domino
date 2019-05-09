import socket
import select
import sys
import msvcrt
import os
import time
import json
import pickle
ipAddress = '127.0.0.1'
port = 5000
address = (ipAddress,port)
class ClientChat:
    def __init__(self, server_address):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(server_address)
        self.player_name = None

    def run(self):
        while True:
            sockets_list = [self.socket]
            read_sockets, write_socket, _ = select.select(sockets_list,[],[],1)
            if msvcrt.kbhit():
                read_sockets.append(sys.stdin)
            for socks in read_sockets:
                if socks == self.socket:
                    message = socks.recv(4096)
                    message = pickle.loads(message)
                    if message["sender"] == "admin" and message.get("player_name",False) != False:
                        self.player_name = message["player_name"]
                    print("<"+ message["sender"]+"> : "+message["body"].strip())
                else:
                    inputs = sys.stdin.readline()
                    message = {}
                    message["sender"] = self.player_name
                    message["type"] = "msg"
                    message["body"] = inputs
                    self.socket.send(pickle.dumps(message))
                    sys.stdout.write("<You> :")
                    sys.stdout.write(inputs.strip())
                    sys.stdout.write("\n")
                    sys.stdout.flush()
            for socks in write_socket:
                if socks == self.socket:
                    message=socks.recv(2048)
                    print("writing")
                    print(message)

client = ClientChat(address)
client.run()