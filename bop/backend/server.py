
import socket
import threading

from bop import connection
from bop.backend import game

global serversocket

width = 400
height = 300

fps = 60
gap = 1 / fps

drag = 0.4578
size = 10

loop = True

class ClientConnection():
    def __init__(self, game, conn):
        self.game = game

        self.connection = connection.Connection(conn)

        self.connection.setListener("keys", self.keysCom)
        #self.connection.setListener("exit", self.exitCom)
        self.connection.setListener("newID", self.newIDCom)

    def newIDCom(self, _rec):
        newId = 0
        while newId in self.game.data["players"]:
            newId += 1
        self.game.data["players"][newId] = game.Game.Player(self.game)  #fixme
        self.connection.send_set({
            "com":"id",
            "id":newId
        })

    def keysCom(self, rec):
        self.game.data["players"][rec["id"]].act = rec["key"]

    def exitCom(self, _rec):
        global loop
        loop = False
        self.connection.close()



class Host(threading.Thread):
    def __init__(self, game):
        super(Host, self).__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('127.0.0.1', 8089))
        self.s.listen(5)  # become a server socket, maximum 5 connections
        self.game = game
        self.connections = []

        self.daemon = True
        self.start()

    def run(self):
        while True:
            conn, address = self.s.accept()
            self.connections.append(ClientConnection(self.game, conn))
            print("Client connected")

    def sync(self):
        for client in self.connections:
            client.connection.send_set({
                "com":"data",
                "data":self.game.data
            })


