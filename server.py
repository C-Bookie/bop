
import socket
import threading

import game, connection

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
        self.game.players[newId] = self.game.Player(self.game)  #fixme
        self.connection.send_set({
            "com":"id",
            "id":newId
        })

    def keysCom(self, rec):
        self.game.players[rec["id"]].act = rec["key"]

    def exitCom(self, _rec):
        global loop
        loop = False
        self.connection.close()



class Host(threading.Thread):
    def __init__(self, game):
        super(Host, self).__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('localhost', 8089))
        self.s.listen(5)  # become a server socket, maximum 5 connections
        self.game = game
        self.connections = []
#        self.lock = threading.Lock()

        self.daemon = True
        self.start()

    def run(self):  #fixme
        while True:
            conn, address = self.s.accept()
            self.connections.append(ClientConnection(self.game, conn))
            print("Client connected")
#            self.sync()

    def sync(self):
        for i in list(self.game.data["players"]):
            self.game.data["players"][i].send_set({
                "com":"data",
                "data":self.game.data
            })



