import socket
import threading
import math
import time
import struct
import json

import game
import connection

global serversocket

width = 400
height = 300

fps = 60
gap = 1 / fps

drag = 0.4578
size = 10

loop = True

class RealPlayer(game.Game.Player):
    def __init__(self, game, conn, newId):
        super(RealPlayer, self).__init__(game)
        self.connection = connection.Connection(conn)

        self.connection.setListener("keys", self.keysCom)
        self.connection.setListener("exit", self.exitCom)

        self.id = newId
        self.data = ""

        self.connection.send_set({
            "com":"id",
            "id":newId
        })

    def keysCom(self, rec):
        self.act = rec["key"]

    def exitCom(self, rec):
        global loop
        loop = False
        self.conn.close()


class Host(threading.Thread):
    def __init__(self, game):
        super(Host, self).__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('localhost', 8089))
        self.s.listen(5)  # become a server socket, maximum 5 connections
        self.game = game
        self.lock = threading.Lock()

        self.daemon = True
        self.start()

    def run(self):  #fixme
        while True:
            conn, address = self.s.accept()
            newId = 0
            while newId in self.game.data["players"]:
                newId+=1
            self.game.data["players"][newId] = RealPlayer(self.game, conn, newId)
            print("Connected: " + str(newId))
            self.sync()

    def sync(self):
        for i in list(self.game.data["players"]):
            temp = {
                "com":"data",
                "data":self.game.data
            }

            self.game.data["players"][i].send_set(temp)


if __name__ == '__main__':
    game = game.Game([width, height], drag, size, math.ceil(size / 2**3))

    host = Host(game)

    lastCheck = 0

    while loop:
        game.loop()
        host.sync()

        now = time.time()
        wait = (lastCheck + gap) - now
        lastCheck = now
        if wait > 0:
            time.sleep(wait)


