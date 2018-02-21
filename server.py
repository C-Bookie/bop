import socket
import threading
import sys

import time
import math
import random


global serversocket

fps = 60
gap = 1/fps
lastCheck = 0

cycle = 0

change = 3
changeCycle = fps * change

state = True

width = 400
height = 300


#player[active, position[x,y], velocity[x,y], keys[left, right, up, down], score]
p = []

gx = 50
gy = 50

s = [0, 0]

size = 10
speed = math.ceil(size/4)

drag = 0.2

class Host(threading.Thread):
    def __init__(self, s):
        super(Host, self).__init__()
        self.s = s

    def run(self):
        while True:
            conn, address = self.s.accept()
#            if (id <= -1):
            p[len(p)] = Player(conn)
            p[len(p) - 1].daemon = True
            p[len(p) - 1].start()
#            else:
#                p[id].act = True
#                p[id].start()


class Player(threading.Thread):
    def __init__(self, conn):
        super(Player, self).__init__()
        self.conn = conn
        self.data = ""

        self.act = True
        self.pos = [10, 10]
        self.vel = [0, 0]
        self.col = (255, 255, 255)
        self.key = [False, False, False, False]
        self.sco = 0

        def run(self):
            while True:
                try:
                    self.data = self.conn.recv(1024).decode()

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

                except socket.error as e:
#                    if e.errno == errno.ECONNRESET:
                    close(self)
                    break
                else:
                    raise()

        def send_msg(self, msg):
            try:
                self.conn.send(msg)
            except socket.error as e:
#                if e.errno == errno.ECONNRESET:
                close(self)
            else:
                raise ()

        def close(self):
            self.act = False
            self.conn.close()

def init():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', 8089))
    serversocket.listen(5)  # become a server socket, maximum 5 connections

    host = Host(serversocket)
    host.daemon = True
    host.start()

def loop():
    global now
    global wait
    global lastCheck

    now = time.time()
    wait = (lastCheck + gap) - now
    lastCheck = now
    if wait > 0:
        time.sleep(wait)

    for player in p:
        player["v"][0]*=drag
        player["v"][1]*=drag


        if player["k"][0]:
            player["v"][0] -= speed
        if player["k"][1]:
            player["v"][0] += speed
        if player["k"][2]:
            player["v"][1] -= speed
        if player["k"][3]:
            player["v"][1] += speed

        player["p"][0] += player["v"][0]
        player["p"][1] += player["v"][1]

        if  player["p"][0] < 0:
            player["p"][0] = 0
            player["v"][0] = abs(player["v"][0])
        if player["p"][0] > width - size:
            player["p"][0] = width - size
            player["v"][0] = -abs(player["v"][0])
        if player["p"][1] < 0:
            player["p"][1] = 0
            player["v"][1] = abs(player["v"][1])
        if player["p"][1] > height - size:
            player["p"][1] = height - size
            player["v"][1] = -abs(player["v"][1])

        if player["p"][0]+size > gx and player["p"][0] < gx+size and player["p"][1]+size > gy and player["p"][1] < gy+size:
            gx = random.randint(0, width - size)
            gy = random.randint(0, height - size)
            player["s"] += 1
            print(str(p[0]["s"])+":"+str(p[1]["s"]))



if __name__ == '__main__':
    init()
    while True:
        loop()

