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

global p
#player[active, position[x,y], velocity[x,y], keys[left, right, up, down], score]
p = []

gx = 50
gy = 50

s = [0, 0]

size = 10
speed = math.ceil(size/4)

drag = 0.2

def addP(id=-1):
    if (id <= -1):
        p[len(p)] = {
            "a":True,
            "p":[10, 10],
            "v":[0, 0],
            "k":[False, False, False, False],
            "s":0
        }
    else:
        p[id]["a"] = True


class eventL(threading.Thread):
    def __init__(self, conn):
        super(eventL, self).__init__()
        self.conn = conn
        self.data = ""

        def run(self):
            while True:
                self.data = self.data + self.conn.recv(1024).decode()

                buf = self.data.split() ##on white space

                if len(buf) > 0:
                        p[id]["k"][data[2]] = data[3]

                if self.data.endswith(u"\r\n"):
                    print(self.data)
                    self.data = ""

        def send_msg(self, msg):
            self.conn.send(msg)

        def close(self):
            self.conn.close()

def init():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', 8089))
    serversocket.listen(5)  # become a server socket, maximum 5 connections






    conn, address = s.accept()
    c = eventL(conn)
    c.start()


def loop():
    connection, address = serversocket.accept()
    event()

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
    c.close()
