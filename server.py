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
p = {}

gx = 50
gy = 50

s = [0, 0]

size = 10
speed = math.ceil(size/4)

drag = 0.2



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
        print("moo")
        while True:
            try:
                self.data = self.conn.recv(1024).decode()
                if self.data != "":

                    rec = {}
                    raw = self.data.split("|")[:-1]
                    for i in raw:
                        buf = i.split(":")
                        rec[buf[0]] = buf[1:]

                    if rec["com"][0] == "keys":
                        for i, j in enumerate(rec["key"]):
                            self.key[i] = j=="True"
                        print(self.key)
                    elif rec["com"][0] == "exit":
                        #                    close(self)
                        break

            except socket.error as e:
#                    if e.errno == errno.ECONNRESET:
#                close(self)
                break
            except Exception as e:
                raise (e)

    def send_msg(self, msg):
        try:
            self.conn.send(msg)
        except socket.error as e:
            print("error")
#                if e.errno == errno.ECONNRESET:
#            close(self)
        else:
            raise ()

    def close(self):
        self.act = False
        self.conn.close()


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

    for i in p:
        player = p[i]
        player.vel[0]*=drag
        player.vel[1]*=drag


        if player.key[0]:
            player.vel[0] -= speed
        if player.key[1]:
            player.vel[0] += speed
        if player.key[2]:
            player.vel[1] -= speed
        if player.key[3]:
            player.vel[1] += speed

        player.pos[0] += player.vel[0]
        player.pos[1] += player.vel[1]

        if  player.pos[0] < 0:
            player.pos[0] = 0
            player.vel[0] = abs(player.vel[0])
        if player.pos[0] > width - size:
            player.pos[0] = width - size
            player.vel[0] = -abs(player.vel[0])
        if player.pos[1] < 0:
            player.pos[1] = 0
            player.vel[1] = abs(player.vel[1])
        if player.pos[1] > height - size:
            player.pos[1] = height - size
            player.vel[1] = -abs(player.vel[1])

        global gx
        global gy
        if player.pos[0]+size > gx and player.pos[0] < gx+size and player.pos[1]+size > gy and player.pos[1] < gy+size:
            gx = random.randint(0, width - size)
            gy = random.randint(0, height - size)
            player.sco += 1
            print(str(p[0].sco)+":"+str(p[1].sco))



if __name__ == '__main__':
    init()
    while True:
        loop()

