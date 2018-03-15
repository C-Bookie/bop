import socket
import threading
import math
import time
import struct
import json

from pygame.locals import *

import game, screen


global clientsocket

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
        super(Client, self).__init__()
        self.game = game
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(('localhost', 8089))

        while True:
            self.data = self.recv_msg().decode()
            if self.data != "":
                rec = json.loads(self.data)
                if rec["com"] == "id":
                    break
        self.id = rec["id"]
        self.game.data["players"][self.id] = self.game.Player(self.game)

    def run(self):
        while True:
            try:
                self.data = self.recv_msg().decode()
                if self.data != "":

                    rec = json.loads(self.data)

                    if rec["com"] == "data":
                        self.game.data["gold"].deList(rec["data"]["gold"])
                        for j in rec["data"]["players"]:
                            i = int(j)
                            if i not in self.game.data["players"]:
                                self.game.data["players"][i] = self.game.Player(self.game)
                            self.game.data["players"][i].deList(rec["data"]["players"][j])
                        for j in list(self.game.data["players"]):
                            if str(j) not in rec["data"]["players"]:
                                self.game.data["players"].pop(j)
                    elif rec["com"] == "exit":
                        global loop
                        loop = False
                        self.conn.close()
                        break

            except socket.error as e:
                #if e.errno == errno.ECONNRESET:
                self.conn.close()
                break
            except Exception as e:
                raise (e)

    def send_msg(self, msg):
        try:
            msg = struct.pack('>I', len(msg)) + msg
            self.conn.sendall(msg)
        except socket.error as e:
            print("error")
            #                if e.errno == errno.ECONNRESET:
            global loop
            loop = False
            self.conn.close()

    def send_set(self, s):
        def set_default(obj):
            if isinstance(obj, set):
                return list(obj)
            elif isinstance(obj, game.Game.Entity):
                return obj.list()
            raise TypeError

        data = json.dumps(s, default=set_default)
        self.send_msg(data.encode())

    def recv_msg(self):
        # Read message length and unpack it into an integer
        raw_msglen = self.recvall(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(msglen)

    def recvall(self, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = b''
        while len(data) < n:
            packet = self.conn.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def sync(self):
        temp = {
            "com":"keys",
            "key":self.game.data["players"][self.id].act
        }

        self.send_set(temp)






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
