
import math
import random

class Game:
    def __init__(self, screenSize, drag, size, speed):
        self.screenSize = screenSize
        self.drag = drag
        self.size= size
        self.speed = speed
        self.bop = False
        self.players = {}
        self.gold = self.Entity(self)

    def addPlayer(self):
        self.players[len(self.players)] = self.Player(self)


    def loop(self):
        for i in self.players:
            player = self.players[i]
            for j, k in enumerate(player.pos):
                player.vel[j] *= self.drag

                if player.act[j*2]:
                    player.vel[j] -= self.speed
                if player.act[j*2+1]:
                    player.vel[j] += self.speed

                player.pos[j] += player.vel[j]

                if player.pos[j] < 0:
                    player.pos[j] = 0
                    player.vel[j] = abs(player.vel[j])
                if player.pos[j] > self.screenSize[j] - self.size:
                    player.pos[j] = self.screenSize[j] - self.size
                    player.vel[j] = -abs(player.vel[j])

            if self.overlapping(player, self.gold):
                for i, j in enumerate(self.gold.pos):
                    self.gold.pos[i] = random.randint(0, self.screenSize[i] - self.size)
                player.sco += 1
                self.bop = True

    def overlapping(self, e1, e2):
        result = True
        for i, j in enumerate(e1.pos):
            result &= e1.pos[i] + self.size > e2.pos[i] and e1.pos[i] < e2.pos[i] + self.size
        return result

    class Entity():
        def __init__(self, game):
            self.pos = [0]*len(game.screenSize)
            self.vel = [0]*len(game.screenSize)
            for i, j in enumerate(game.screenSize):
                self.pos[i] = random.randint(0, game.screenSize[i] - game.size)
            self.col = (random.randint(128, 192), random.randint(128, 192), random.randint(0, 128))


    class Player(Entity):
        def __init__(self, game):
            super(Game.Player, self).__init__(game)
            self.act = [False]*len(game.screenSize)*2 #left, right, up, down
            self.sco = 0
            self.col = (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))

