"""client connection and screen setup"""

import caduceussocket
from bop.frontend import screen


class Director(caduceussocket.Client):
    def __init__(self, addr='127.0.0.1'):
        super().__init__(addr)
        self.users = []

        self.screen = screen.Screen()

        #  functions callable remotely
        self.white_list_functions += [
            "dataCom",
            "freshID",
            "setup",
            "exitCom"
        ]

    # called upon connecting
    def connect(self):
        super().connect()
        self.send_data({
            "type": "register",
            "args": [
                "player",
                "game1"
            ]
        })
        self.toServer({"type": "newScreen"})

    # used to setup initial game variables
    def setup(self, data, screenSize, size, bop):
        if not self.screen.ready:
            self.data = data
            self.screenSize = screenSize
            self.size = size
            self.bop = bop

            self.screen.setup(self.screenSize, self.size, self.bop)

    # declares a new user controller and requests a new playerID
    def newUser(self, user):
        self.users.append(user)
        self.toServer({"type": "newIDCom"})

    # assigns new playerID
    def freshID(self, player_id):
        for user in self.users:
            if user.id == -1:
                user.id = player_id
                self.screen.addUser(user)
                # self.game.addPlayer(user.id)
                # self.data["players"][user.id] = self.game.Player(self.random, self.screenSize, self.size)
                return
        raise Exception

    # receiving game data
    def dataCom(self, data):
        self.data = data

    # exits game
    def exitCom(self):
        # global loop
        # loop = False
        self.close()

    # called every frame to update controller events and screen
    def sync(self):
        if self.screen.ready:
            self.data = self.screen.loop(self.data)

            for user in self.users:
                id = str(user.id)  # fixme JSON converting int keys to string
                if id in self.data["players"]:
                    self.toServer({
                        "type": "keysCom",
                        "args": [
                            id,
                            self.data["players"][id]["act"]
                        ]
                    })

    # utility function for communicating to the server
    def toServer(self, msg):
        self.send_data({
            "type": "broadcast",
            "args": [
                msg,
                "server"
            ]
        })



