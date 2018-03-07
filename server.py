import socket
import threading
import sys
import math
import time
import random

import game

import json


global serversocket

width = 400
height = 300

fps = 60
gap = 1 / fps

drag = 0.4578
size = 10



class RealPlayer(game.Game.Player, threading.Thread):
    def __init__(self, _game, conn):
        threading.Thread.__init__(self)
        super(RealPlayer, self).__init__(game)
        #game.Game.Player.__init__(self, _game)
        self.conn = conn
        self.data = ""

        self.daemon = True
        self.start()

    def run(self):
        while True:
            try:
                self.data = self.conn.recv(1024).decode()
                if self.data != "":

                    rec = json.loads(self.data)

                    if rec["com"][0] == "keys":
                        self.act = rec["key"]
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
            self.game.data["players"][len(self.game.data["players"])] = RealPlayer(game, conn)

    def sync(self):
        for i in self.game.data["players"]:
            def set_default(obj):
                if isinstance(obj, set):
                    return list(obj)
                raise TypeError #fixme returns RealPlayer

            data = json.dumps(self.game.data, default=set_default)

            print(data)
            i.send_msg(data.encode())



if __name__ == '__main__':
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', 8089))
    serversocket.listen(5)  # become a server socket, maximum 5 connections

    game = game.Game([width, height], drag, size, math.ceil(size / 4))

    host = Host(serversocket, game)
    host.daemon = True
    host.start()

    lastCheck = 0

    while True:
        game.loop()
        host.sync()

        now = time.time()
        wait = (lastCheck + gap) - now
        lastCheck = now
        if wait > 0:
            time.sleep(wait)


