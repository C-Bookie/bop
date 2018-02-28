import socket
import threading
import sys
import math
import time
import random

import game


global serversocket

width = 400
height = 300

fps = 60
gap = 1 / fps

drag = 0.4578
size = 10


class Game:
    def __init__(self, screenSize, drag, size, speed):
        self.screenSize = screenSize
        self.drag = drag
        self.size= size
        self.speed = speed
        self.bop = False
        self.players = {}
        self.gold = self.Entity(self)

    def addPlayer(self):
        self.players[len(self.players)] = self.Player(self)


    def loop(self):
        for i in self.players:
            player = self.players[i]
            for j, k in enumerate(player.pos):
                player.vel[j] *= self.drag

                if player.act[j*2]:
                    player.vel[j] -= self.speed
                if player.act[j*2+1]:
                    player.vel[j] += self.speed

                player.pos[j] += player.vel[j]

                if player.pos[j] < 0:
                    player.pos[j] = 0
                    player.vel[j] = abs(player.vel[j])
                if player.pos[j] > self.screenSize[j] - self.size:
                    player.pos[j] = self.screenSize[j] - self.size
                    player.vel[j] = -abs(player.vel[j])

            if self.overlapping(player, self.gold):
                for i, j in enumerate(self.gold.pos):
                    self.gold.pos[i] = random.randint(0, self.screenSize[i] - self.size)
                player.sco += 1
                self.bop = True

    def overlapping(self, e1, e2):
        result = True
        for i, j in enumerate(e1.pos):
            result &= e1.pos[i] + self.size > e2.pos[i] and e1.pos[i] < e2.pos[i] + self.size
        return result

    class Entity():
        def __init__(self, game):
            self.pos = [0]*len(game.screenSize)
            self.vel = [0]*len(game.screenSize)
            for i, j in enumerate(game.screenSize):
                self.pos[i] = random.randint(0, game.screenSize[i] - game.size)
            self.col = (random.randint(128, 192), random.randint(128, 192), random.randint(0, 128))

    class Player(Entity):
        def __init__(self, game):
            super(Game.Player, self).__init__(game)
            self.act = [False]*len(game.screenSize)*2 #left, right, up, down
            self.sco = 0
            self.col = (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))

    class RealPlayer(Player, threading.Thread):
        def __init__(self, game, conn):
            super(Game.RealPlayer, self).__init__(game)
            self.conn = conn
            self.data = ""

            self.daemon = True
            self.start()

        def run(self):
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
                                self.act[i] = j=="True"
                            print(self.act)
                        elif rec["com"][0] == "exit":
                            self.conn.close()
                            break

                except socket.error as e:
#                    if e.errno == errno.ECONNRESET:
                    self.conn.close()
                    break
                except Exception as e:
                    raise (e)

        def send_msg(self, msg):
            try:
                self.conn.send(msg)
            except socket.error as e:
                print("error")
    #                if e.errno == errno.ECONNRESET:
                self.conn.close()



class Host(threading.Thread):
    def __init__(self, s, game):
        super(Host, self).__init__()
        self.s = s
        self.game = game

    def run(self):
        while True:
            conn, address = self.s.accept()
            self.game.players[len(self.game.players)] = self.game.RealPlayer(game, conn)


if __name__ == '__main__':
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', 8089))
    serversocket.listen(5)  # become a server socket, maximum 5 connections

    game = Game([width, height], drag, size, math.ceil(size / 4))

    host = Host(serversocket, game)
    host.daemon = True
    host.start()

    lastCheck = 0

    while True:
        game.loop()

        now = time.time()
        wait = (lastCheck + gap) - now
        lastCheck = now
        if wait > 0:
            time.sleep(wait)


