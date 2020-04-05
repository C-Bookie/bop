"""game logic"""

import random

class Game:
    def __init__(self, screen_size, drag, size, speed, frame=False, random_api=random):
        self.random = random_api
        self.screenSize = screen_size
        self.drag = drag  # physical drag on a player
        self.size = size  # size of a player
        self.speed = speed  # speed of a player
        self.bop = False  # enable sound
        self.data = {
            "players": {},
            "gold": self.Entity(self)
        }
        self.frame = frame

    #  adds a playerID to the game data
    def add_player(self, player_id):
        self.data["players"][player_id] = self.Player(self)

    # main game loop for physics engine
    def loop(self):
        for i in self.data["players"]:
            player = self.data["players"][i]
            for j, k in enumerate(player.pos):
                player.vel[j] *= self.drag

                player.vel[j] += self.speed*player.act[j*2]
                player.vel[j] -= self.speed*player.act[j*2+1]

                player.pos[j] += player.vel[j]

                if player.pos[j] < 0:
                    player.pos[j] = 0
                    player.vel[j] = abs(player.vel[j])
                if player.pos[j] > self.screenSize[j] - self.size:
                    player.pos[j] = self.screenSize[j] - self.size
                    player.vel[j] = -abs(player.vel[j])

            if not self.frame:
                if self.overlapping(player, self.data["gold"]):
                    for i, j in enumerate(self.data["gold"].pos):
                        self.data["gold"].pos[i] = self.random.randint(0, self.screenSize[i] - self.size)
                    player.sco += 1
                    self.bop = True

    #  detects if two enteritis are overlapping
    def overlapping(self, e1, e2):
        result = True
        for i, j in enumerate(e1.pos):
            result &= e1.pos[i] + self.size > e2.pos[i] and e1.pos[i] < e2.pos[i] + self.size
        return result

    class Entity:
        def __init__(self, game):
            self.pos = [0]*len(game.screenSize)
            self.vel = [0]*len(game.screenSize)
            for i, j in enumerate(game.screenSize):
                self.pos[i] = game.random.randint(0, game.screenSize[i] - game.size)
            self.col = (game.random.randint(128, 192), game.random.randint(128, 192), game.random.randint(0, 128))

        #  pickle
        def list(self):
            return {
                "pos": self.pos,
                "vel": self.vel,
                "col": self.col,
            }

        # unpickle
        def deList(self, l):
            self.pos = l["pos"]
            self.vel = l["vel"]
            self.col = l["col"]

        def __str__(self):
            return str({
                "pos": self.pos,
                "vel": self.vel,
                "col": self.col
            })

    class Player(Entity):
        def __init__(self, game):
            super().__init__(game)
            self.act = [0]*len(game.screenSize)*2 #left, right, up, down
            self.sco = 0
            self.col = (game.random.randint(128, 255), game.random.randint(128, 255), game.random.randint(128, 255))

        def list(self):
            result = super(Game.Player, self).list()
            result.update({
                "act": self.act,
                "sco": self.sco
            })
            return result

        def deList(self, l):
            super(Game.Player, self).deList(l)
            self.act = l["act"]
            self.sco = l["sco"]

