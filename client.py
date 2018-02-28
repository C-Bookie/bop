import socket
import threading

import time

global clientsocket

fps = 60
gap = 1/fps
lastCheck = 0

class Player(threading.Thread):
    def __init__(self, conn):
        super(Player, self).__init__()
        self.conn = conn
        self.data = ""

        def run(self):
            while True:
                try:
                    self.data = self.conn.recv(1024).decode()
                except socket.error as e:
#                    if e.errno == errno.ECONNRESET:
                    break
                else:
                    raise()

                rec = []
                for i in self.data.split("|")[-2]:
                    buf = i.split(":")
                    rec = []
                    rec[buf[0]] = buf[1:-1]

                if rec[0]["com"] == "keys":
                    self.key = int(rec["key"])
                if rec[0]["com"] == "exit":
                    close(self)
                    break


        def send_msg(self, msg):
            try:
                self.conn.send(msg)
            except socket.error as e:
#                if e.errno == errno.ECONNRESET:
                close(self)
            else:
                raise ()

        def close(self):
            self.conn.close()

def init():
    global clientsocket
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 8089))

def loop():
    global now
    global wait
    global lastCheck

    now = time.time()
    wait = (lastCheck + gap) - now
    lastCheck = now
    if wait > 0:
        time.sleep(wait)

    temp = {
        "com":["keys"],
        "key":[True, False, False, False]
    }
    data = ""
    for i in temp:
        data += str(i)
        for j in temp[i]:
            data += ":"
            data += str(j)
        data += "|"
    print(data)
    global clientsocket
    clientsocket.send(data.encode())

#    keys = pygame.key.get_pressed()
#    if keys[K_a]:



if __name__ == '__main__':
    init()
    l = True
    while l:
        l = False
        loop()
