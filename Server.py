import zmq
import time
import sys
from datetime import datetime
import threading
import ServerCryptographer as sc

class Server():
    protocol_key = "-"
    now = datetime.now()

    def bind_ports(self):
        self.symmetric_key = None

        self.rep_socket_port = "5556"
        self.rep_socket_ip = "127.0.0.1"

        self.key_socket_port = "5557"
        self.key_socket_ip = "127.0.0.1"

        self.display_socket_ip = "127.0.0.1"
        self.display_socket_port = "5555"

        context = zmq.Context()
        self.rep_socket = context.socket(zmq.REP)
        #self.rep_socket.bind("tcp://*:%s" % port)
        rep_socket_bind = 'tcp://{}:{}'.format(self.rep_socket_ip, self.rep_socket_port)
        self.rep_socket.bind(rep_socket_bind)

        self.key_socket = context.socket(zmq.REP)
        key_socket_bind = 'tcp://{}:{}'.format(self.key_socket_ip, self.key_socket_port)
        self.key_socket.bind(key_socket_bind)

        self.display_socket = context.socket(zmq.PUB)
        display_socket_bind = 'tcp://{}:{}'.format(self.display_socket_ip, self.display_socket_port)
        self.display_socket.bind(display_socket_bind)

    def broadcast_messages(self, user, msg):
        print("Broadcasting Received Messages")
        topic = "broadcast"
        msg_to_send = topic + "°" + user + "°"+ msg
        self.display_socket.send_string(msg_to_send)

    def receive_message(self):
        msg = self.rep_socket.recv_json()
        print(msg)
        user = msg["username"]
        message = msg["message"]
        self.rep_socket.send_string("succesful")
        return [user, message]

    def key_socket_recv(self):
        key_generator = sc.symmetric_key_generator()
        self.symmetric_key = key_generator.glob_key
        while True:
            public_key = self.key_socket.recv_string()
            self.key_socket.send_string(sc.coder.encrypt(text=self.symmetric_key, pub_key=public_key))


    def __init__(self):
        self.bind_ports()
        recv_thread = threading.Thread(target=self.key_socket_recv)
        recv_thread.start()
        while True:
            username, message = self.receive_message()
            self.broadcast_messages(username, message)



server = Server()
