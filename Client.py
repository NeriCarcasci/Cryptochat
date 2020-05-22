import zmq
import threading
from queue import Queue
import ClientCryptographer as cc
import sys


class Client():
    protocol_key = "-"

    def connect(self):  # Connect to servers
        print("Connecting to server...")
        context = zmq.Context()

        # Connect to the REP servver
        self.req_socket = context.socket(zmq.REQ)
        self.req_socket.connect("tcp://%s:%s" % (self.glo_ip, self.Servers.get("port1")))

        # Connect to display PUB server
        self.sub_socket = context.socket(zmq.SUB)
        self.sub_socket.connect("tcp://%s:%s" % (self.glo_ip, self.Servers.get("port2")))
        topicfilter = "broadcast"
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)

        # Connect to KEY server
        self.key_socket = context.socket(zmq.SUB)
        self.key_socket.connect("tcp://%s:%s" % (self.glo_ip, self.Servers.get("port2")))

        print("Connection Sucessfull")

    def con_init(self):
        cryptographer = cc.decoder()
        self.key_socket.send_string(cryptographer.public_key)
        encrypted_msg = self.key_socket.recv_string()
        self.symmetric_key = cryptographer.decode(encrypted_msg, cryptographer.private_key)
        print(self.symmetric_key)

    def status_checker(self, reply):
        if reply == "Received":
            return "successful"
        else:
            return "Message Failed to send"

    def msg_send(self, message):
        print("Sending message to  %s …" % self.Servers.get("Server1"))
        msg_to_send = {
            "username": self.username,
            "message": message
        }
        self.req_socket.send_json(msg_to_send)

    def msg_receive(self):
        answer = self.req_socket.recv()
        return self.status_checker(answer)

    def pub_socket_recv(self):
        while True:
            string = self.sub_socket.recv()
            topic, user , msg= string.split("°".encode("utf-8"))
            msg = msg.decode("utf-8")
            user = user.decode("utf-8")
            final_format = "\n" +  user +": "+ msg
            #print works
            self.display_queue.put(final_format)

    def update_displays(self):
        # msg = self.server_messages[0]
        # user = msg["username"]
        # message = msg["message"]
        # print("{}: {}".format(message, user))

        while True:
            line = self.display_queue.get()
            if line is not None:  # simple termination logic
                print(line)

    def mainloop(self):
        try:
            self.connect()
            print("starting listener.thread")
            self.con_init()
            self.display_queue = Queue()  # synchronizes console output
            writer_thread = threading.Thread(target=self.pub_socket_recv)
            screen_printing_thread = threading.Thread(target=self.update_displays)
            writer_thread.start()
            screen_printing_thread.start()

            while True:
                msg = input("You:")
                if len(msg) > 0:
                    self.msg_send(msg)
                    self.msg_receive()


        except:
            print("Internal Error: Mainloop failed to execute")

    def __init__(self, global_ip="127.0.0.1", rep_port="5556", display_port="5555", mode="nonlocal"):
        self.rep_port = rep_port
        self.display_port = display_port
        self.glo_ip = global_ip
        self.key_port = "5557"
        self.Servers = {
            "Server1": "REP Server",
            "port1": self.rep_port,

            "Server2": "DISPLAY Server",
            "port2": self.display_port,

            "Server3": "DISPLAY Server",
            "port3": self.key_port,
        }
        self.username = input("Pick username:")
        self.server_messages = list()
        self.mainloop()



