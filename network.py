"10.0.0.1"

import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.0.0.15"
        self.port = 6010
        self.addr = (self.server, self.port)
        self.player_color = self.connect()




    def get(self):
        return self.client.recv(2048 * 5)




    def connect(self):
        self.client.connect(self.addr)
        return pickle.loads(self.get())


    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.get())
        except socket.error as e:
            print(e)