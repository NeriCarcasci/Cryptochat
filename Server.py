import zmq
import time
import sys
from datetime import datetime

class Server():
    protocol_key = "-"
    now = datetime.now()

    def bind_ports(self):
        self.rep_socket_port = "5556"
        self.rep_socket_ip = "*"
        self.display_socket_ip = "*"
        self.display_socket_port = "5555"

        context = zmq.Context()
        self.rep_socket = context.socket(zmq.REP)
        #self.rep_socket.bind("tcp://*:%s" % port)
        rep_socket_bind = 'tcp://{}:{}'.format(self.rep_socket_ip, self.rep_socket_port)
        self.rep_socket.bind(rep_socket_bind)

        self.display_socket = context.socket(zmq.PUB)
        display_socket_bind = 'tcp://{}:{}'.format(self.display_socket_ip, self.display_socket_port)
        self.display_socket.bind(display_socket_bind)

    def broadcast_messages(self, user, msg):
        print("Broadcasting Received Messages")
        update = {
            "username": user,
            "message" : msg
        }

        self.display_socket.send_json(update)

    def receive_message(self):
        msg = self.rep_socket.recv_json()
        print(msg)
        user = msg["username"]
        message = msg["message"]
        self.rep_socket.send_string("succesful")
        return [user, message]

    def __init__(self):
        self.bind_ports()
        while True:
            username, message = self.receive_message()
            self.broadcast_messages(username, message)



server = Server()
