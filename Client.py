import zmq
import threading
from queue import Queue
import sys


class Client():
        protocol_key = "-"

            
        def connect(self): # Connect to servers
            print("Connecting to server...")
            context = zmq.Context()
            #Connect to the REP servver
            self.req_socket = context.socket(zmq.REQ)
            self.req_socket.connect("tcp://%s:%s" % (self.glo_ip, self.Servers.get("port1")))
            
            # Connect to display PUB server
            self.sub_socket = context.socket(zmq.SUB)
            self.sub_socket.connect("tcp://%s:%s" % (self.glo_ip, self.Servers.get("port2")))
            print("Connection Sucessfull")

        def con_try(self):
                #  Do 10 requests, waiting each time for a response
            for request in range (1,10):
                print ("Sending request ", request,"...")
                self.msg_send("ScoutConnection")

                #  Get the reply.
                message = self.msg_receive()
                print ("Received reply {}, user: {}, -{}-".format(request, message))
                if len(message) > 0:
                    break
            print("Connection succesful with server")
            return "successful"

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
                msg = self.sub_socket.recv_json()
                #self.server_messages.append(msg)
                self.display_queue.put(msg)


        def update_displays(self):
            #msg = self.server_messages[0]
            #user = msg["username"]
            #message = msg["message"]
            #print("{}: {}".format(message, user))

            while True:
                line = self.display_queue.get()
                if line is None:  # simple termination logic
                    break
                print(line)


        def mainloop(self):
            try:
                    self.connect()
                    print("starting listener.thread")
                    self.display_queue = Queue()

                    threading1 = threading.Thread(target=self.pub_socket_recv)
                    threading1.daemon = True
                    threading1.start()

                    threading2 = threading.Thread(target=self.update_displays)
                    threading2.daemon = True
                    threading2.start()


                    while True:
                        try:
                            self.update_displays()
                        except:
                            msg = input("You:")
                            if len(msg) > 0:
                                self.msg_send(msg)
                                self.msg_receive()
                            else:
                                print('Invalid Input')


            except:
                print("Internal Error: Mainloop failed to execute")

        def __init__(self, global_ip = "127.0.0.1", rep_port = "5556", display_port = "5555", mode = "nonlocal"):
            self.rep_port = rep_port
            self.display_port = display_port
            self.glo_ip = global_ip
            self.Servers = {
                "Server1":"REP Server",
                "port1":self.rep_port,

                "Server2":"DISPLAY Server",
                "port2":self.display_port,
                }
            self.username = input("Pick username:")
            self.server_messages = list()
            self.mainloop()

client = Client()
