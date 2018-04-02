
import socket
import threading
import math
import time
import struct
import json

from pygame.locals import *

import game, screen, connection


global clientsocket


fps = 60
gap = 1/fps
lastCheck = 0
loop = True


class Client():
    def __init__(self, game, ip):
#        super(Client, self).__init__()
        self.game = game
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((ip, 8089))
        self.connection = connection.Connection(conn)

        self.connection.setListener("data", self.dataCom)
        self.connection.setListener("exit", self.exitCom)

        while True:    #to be removed
            self.data = self.connection.recv_msg().decode()
            if self.data != "":
                rec = json.loads(self.data)
                if rec["com"] == "id":
                    break
        self.id = rec["id"]
#        self.game.data["players"][self.id] = self.game.Player(self.game)
        self.game.addPlayer(self.id)

    def dataCom(self, rec):
        self.game.data["gold"].deList(rec["data"]["gold"])
        for j in rec["data"]["players"]:
            i = int(j)
            if i not in self.game.data["players"]:
                self.game.data["players"][i] = self.game.Player(self.game)
            self.game.data["players"][i].deList(rec["data"]["players"][j])
        for j in list(self.game.data["players"]):
            if str(j) not in rec["data"]["players"]:
                self.game.data["players"].pop(j)

    def exitCom(self, _rec):
        global loop
        loop = False
        self.connection.conn.close()

    def sync(self):
        temp = {
            "com":"keys",
            "key":self.game.data["players"][self.id].act
        }

        self.connection.send_set(temp)


if __name__ == '__main__':
    gameFrame = game = game.Game([400, 300], 0.5, 4, math.ceil(4 / 4), True)
    client = Client(game)
    screen = screen.Screen(game, [client.id])

    client.daemon = True
    client.start()

    while loop:
        client.game.loop()
        screen.loop()
        client.sync()

        now = time.time()
        wait = (lastCheck + gap) - now
        lastCheck = now
        if wait > 0:
            time.sleep(wait)
