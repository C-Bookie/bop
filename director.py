
import json

import client, screen, user

class director():
    def __init__(self, ip, game=None):
        if game == None:
            self.game = game.Game
        else:
            self.game = game
        self.client = client.Client(game, ip)
        self.client.daemon = True
        self.client.start()

        self.users = []
        for i in range(players):
            pass

        self.screen = screen.Screen

    def newUser(self):
        while True:
            self.data = self.client.recv_msg().decode()  #fixme
            if self.data != "":
                rec = json.loads(self.data)
                if rec["com"] == "id":
                    break
        self.id = rec["id"]
        #self.game.data["players"][self.id] = self.game.Player(self.game)
        self.client.game.addPlayer(self.id)
        self.users.append(screen.Screen.user(id, False, controls=screen.playerKeys[0]))


