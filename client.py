import socket
import threading

import math
import time

global clientsocket

import pygame
import sys
from pygame.locals import *

import json

import game, screen

playerKeys = [
    (K_a, K_d, K_w, K_s),
    (K_LEFT, K_RIGHT, K_UP, K_DOWN)
]

fps = 60
gap = 1/fps
lastCheck = 0
loop = True


class Client(threading.Thread):
    def __init__(self, game):
        threading.Thread.__init__(self)
        self.game = game
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect(('localhost', 8089))

        self.daemon = True
        self.start()

        def run(self):
            while True:
                try:
                    self.data = self.conn.recv(1024).decode()
                    if self.data != "":

                        rec = json.loads(self.data)

                        if rec["com"][0] == "data":
                            self.game.data = rec["data"]
                        elif rec["com"][0] == "exit":
                            self.conn.close()
                            global loop
                            loop = False
                            break

                except socket.error as e:
                    #if e.errno == errno.ECONNRESET:
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

        def sync(self, screen):
            temp = {
                "com":"keys",
                "key":screen.key
            }

            def set_default(obj):
                if isinstance(obj, set):
                    return list(obj)
                raise TypeError

            data = json.dumps(temp, default=set_default)

            print(data)
            self.send_msg(data.encode())



if __name__ == '__main__':
    gameFrame = game = game.Game([300, 400], 0.5, 4, math.ceil(4 / 4))
    screen = screen.Screen(game)
    client = Client(game)

    while loop:
        now = time.time()
        wait = (lastCheck + gap) - now
        lastCheck = now
        if wait > 0:
            time.sleep(wait)
