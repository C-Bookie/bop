
import caduceussocket


class GameServer(caduceussocket.Client):
    def __init__(self, game):
        super().__init__()
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

    def newIDCom(self):
        newId = 0
        while newId in self.game.data["players"]:
            newId += 1
        self.game.addPlayer(newId)
        self.toPlayers({
            "type": "freshID",
            "args": [
                newId
            ]
        })

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

    def keysCom(self, player_id, key):
        id = int(player_id)  # fixme JSON converting int keys to string
        self.game.data["players"][id].act = key

    def exitCom(self):
        self.conn.close()

    def tick(self):
        self.game.loop()
        self.toPlayers({
            "type": "dataCom",
            "args": [
                self.game.data
            ]
        })

    def toPlayers(self, msg):
        self.send_data({
            "type": "broadcast",
            "args": [
                msg,
                "player"
            ]
        })

