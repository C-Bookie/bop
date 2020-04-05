
import caduceussocket
from bop.frontend import screen


class Director(caduceussocket.Client):
    def __init__(self):
        super().__init__()
        self.users = []

        self.screen = screen.Screen()

        self.white_list_functions += [
            "dataCom",
            "freshID",
            "setup",
            "exitCom"
        ]

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

    def setup(self, data, screenSize, size, bop):
        if not self.screen.ready:
            self.data = data
            self.screenSize = screenSize
            self.size = size
            self.bop = bop

            self.screen.setup(self.screenSize, self.size, self.bop)

    def newUser(self, user):
        self.users.append(user)
        self.toServer({"type": "newIDCom"})

    def freshID(self, player_id):
        for user in self.users:
            if user.id == -1:
                user.id = player_id
                self.screen.addUser(user)
                # self.game.addPlayer(user.id)
                # self.data["players"][user.id] = self.game.Player(self.random, self.screenSize, self.size)
                return
        raise Exception

    def dataCom(self, data):
        self.data = data

        # self.data["gold"].deList(data["gold"])  #sync the gold
        #
        # for j in data["players"]:    #adding online players
        #     i = int(j)
        #     if i not in self.data["players"]:
        #         self.data["players"][i] = self.game.Player(self.game)
        #     self.data["players"][i].deList(data["players"][j])
        #
        # for j in list(self.data["players"]):   #removing online players
        #     if str(j) not in data["players"]:    #todo replace str(j) with int(j)
        #         self.data["players"].pop(j)

    def exitCom(self, _rec):
        # global loop
        # loop = False
        self.close()

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

    def toServer(self, msg):
        self.send_data({
            "type": "broadcast",
            "args": [
                msg,
                "server"
            ]
        })



