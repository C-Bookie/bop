"""server and game hosting"""

import caduceussocket


class GameServer(caduceussocket.Client):
    def __init__(self, game, addr='127.0.0.1'):
        super().__init__(addr)
        self.game = game

        self.white_list_functions += [
            "keysCom",
            "newIDCom",
            "exitCom",
            "newScreen"
        ]

    def connect(self):
        super().connect()
        self.send_data({
            "type": "register",
            "args": [
                "server",
                "game1"
            ]
        })

    #  called remotely to request a new playerID
    def newIDCom(self):
        newId = 0
        while newId in self.game.data["players"]:
            newId += 1
        self.game.add_player(newId)
        self.toPlayers({
            "type": "freshID",
            "args": [
                newId
            ]
        })

    #  called remotely to request starting game data
    def newScreen(self):
        self.toPlayers({
            "type": "setup",
            "args": [
                self.game.data,
                self.game.screenSize,
                self.game.size,
                self.game.bop
            ]
        })

    #  called remotely to provide recent keyboard/controller activity
    def keysCom(self, player_id, key):
        id = int(player_id)  # fixme JSON converting int keys to string
        self.game.data["players"][id].act = key

    #  called remotely to close the server
    def exitCom(self):
        self.conn.close()

    #  called every frame to prompt the main game loop and distribute new game data
    def tick(self):
        self.game.loop()
        self.toPlayers({
            "type": "dataCom",
            "args": [
                self.game.data
            ]
        })

    # utility function for messaging all players
    def toPlayers(self, msg):
        self.send_data({
            "type": "broadcast",
            "args": [
                msg,
                "player"
            ]
        })

