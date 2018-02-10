import socket
import threading

global clientsocket

class client(threading.Thread):
    def __init__(self, conn):
        super(client, self).__init__()
        self.conn = conn
        self.data = ""

        def run(self):
            while True:
                self.data = self.data + self.conn.recv(1024)
                if self.data.endswith(u"\r\n"):
                    print(self.data)
                    self.data = ""

        def send_msg(self, msg):
            self.conn.send(msg)

        def close(self):
            self.conn.close()

def init():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 8089))

def loop():
    clientsocket.send(({"moo", 1}).encode())

    keys = pygame.key.get_pressed()
    if keys[K_a]:



if __name__ == '__main__':
    init()
    while 1:
        loop()
