
import socket

import screen, connection

class Director():
    def __init__(self, ip, game):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((ip, 8089))
        self.connection = connection.Connection(conn)

        self.game = game
        self.screen = screen.Screen(self.game)
        self.users = []

        self.connection.setListener("data", self.dataCom)
#        self.connection.setListener("exit", self.exitCom)
        self.connection.setListener("id", self.freshID)

    def newUser(self, user):
        self.users.append(user)
        temp = {"com": "newID"}
        self.connection.send_set(temp)

    def freshID(self, rec):
        for user in self.users:
            if user.id == -1:
                user.id = rec["id"]
                self.screen.addUser(user)
                self.game.addPlayer(user.id)
                return
        raise Exception

    def dataCom(self, rec):
        self.game.data["gold"].deList(rec["data"]["gold"])  #sync the gold

        for j in rec["data"]["players"]:    #adding online players
            i = int(j)
            if i not in self.game.data["players"]:
                self.game.data["players"][i] = self.game.Player(self.game)
            self.game.data["players"][i].deList(rec["data"]["players"][j])

        for j in list(self.game.data["players"]):   #removing online players
            if str(j) not in rec["data"]["players"]:    #todo replace str(j) with int(j)
                self.game.data["players"].pop(j)

    def exitCom(self, _rec):
        global loop
        loop = False
        self.connection.conn.close()

    def loop(self):
        self.screen.loop()

        for user in self.users:
            if user.id != -1:
                self.connection.send_set({
                    "com": "keys",
                    "id": user.id,
                    "key": self.game.data["players"][user.id].act
                })



