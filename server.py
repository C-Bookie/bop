import socket
import threading
import math
import time
import struct
import json

import game


global serversocket

width = 400
height = 300

fps = 60
gap = 1 / fps

drag = 0.4578
size = 10

loop = True

class RealPlayer(game.Game.Player, threading.Thread):
    def __init__(self, game, conn, newId):
        threading.Thread.__init__(self)
        super(RealPlayer, self).__init__(game)
        self.conn = conn
        self.id = newId
        self.data = ""

        self.send_set({
            "com":"id",
            "id":newId
        })

        self.daemon = True
        self.start()

    def run(self):
        while True:
            try:
                self.data = self.recv_msg().decode()
                if self.data != "":

                    rec = json.loads(self.data)

                    if rec["com"] == "keys":
                        self.act = rec["key"]
                    elif rec["com"] == "exit":
                        global loop
                        loop = False
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
            msg = struct.pack('>I', len(msg)) + msg
            self.conn.sendall(msg)
        except socket.error as e:
            print("disconnected: " + str(self.id))
            #                if e.errno == errno.ECONNRESET:
            self.game.data["players"].pop(self.id)
            self.conn.close()

    def send_set(self, s):
        def set_default(obj):
            if isinstance(obj, set):
                return list(obj)
            elif isinstance(obj, game.Entity):
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



class Host(threading.Thread):
    def __init__(self, game):
        super(Host, self).__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('localhost', 8089))
        self.s.listen(5)  # become a server socket, maximum 5 connections
        self.game = game
        self.lock = threading.Lock()

    def run(self):
        while True:
            conn, address = self.s.accept()
            newId = 0
            while newId in self.game.data["players"]:
                newId+=1
            self.game.data["players"][newId] = RealPlayer(game, conn, newId)
            host.sync()

    def sync(self):
        for i in list(self.game.data["players"]):
            temp = {
                "com":"data",
                "data":self.game.data
            }

            self.game.data["players"][i].send_set(temp)



if __name__ == '__main__':
    game = game.Game([width, height], drag, size, math.ceil(size / 4))

    host = Host(game)
    host.daemon = True
    host.start()

    lastCheck = 0

    while loop:
        game.loop()
        host.sync()

        now = time.time()
        wait = (lastCheck + gap) - now
        lastCheck = now
        if wait > 0:
            time.sleep(wait)


