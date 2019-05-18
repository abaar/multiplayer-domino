import socket
import select
import sys
import msvcrt
import os
import time
import pickle
class ClientChat:
    def __init__(self, server_address):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(server_address)
        self.player_name = None
        self.room_number = None
        self.socket.recv(4096)

    def join_quick_room(self):
        message = self.make_message("cmd","quick_room")
        self.socket.send(pickle.dumps(message))
        self.socket.recv(4096)

    def create_custom_room(self, room_number):
        message = self.make_message("cmd","create_custom_room "+room_number)
        self.socket.send(message)

    def join_custom_room(self, room_number):
        message = self.make_message("cmd","join_custom_room "+room_number)
        self.socket.send(message)

    def quit(self):
        message = self.make_message("cmd","quit")
        self.socket.send(message)

    def make_message(self,message_type,message_body):
        message = {}
        message["sender"] = self.player_name
        message["type"] = message_type
        message["body"] = message_body
        message["room_number"] = self.room_number
        return message

    # def run(self):
    #     while True:
    #         sockets_list = [self.socket]
    #         read_sockets, write_socket, _ = select.select(sockets_list,[],[],1)
    #         if msvcrt.kbhit():
    #             read_sockets.append(sys.stdin)
    #         for socks in read_sockets:
    #             if socks == self.socket:
    #                 message = socks.recv(4096)
    #                 message = pickle.loads(message)
    #                 if message["sender"] == "admin" and message.get("player_name",False) != False:
    #                     self.player_name = message["player_name"]
    #                 if message["sender"] == "admin" and message.get("room_number",False) != False:
    #                     self.room_number = message["room_number"]
    #                 print("<"+ message["sender"]+"> : "+message["body"].strip())
    #             else:
    #                 inputs = sys.stdin.readline()
    #                 message = {}
    #                 message["sender"] = self.player_name
    #                 message["type"] = "msg"
    #                 message["body"] = inputs
    #                 message["room_number"] = self.room_number
    #                 self.socket.send(pickle.dumps(message))
    #                 sys.stdout.write("<You> :")
    #                 sys.stdout.write(inputs.strip())
    #                 sys.stdout.write("\n")
    #                 sys.stdout.flush()
    #         for socks in write_socket:
    #             if socks == self.socket:
    #                 message=socks.recv(2048)
    #                 print("writing")
    #                 print(message)