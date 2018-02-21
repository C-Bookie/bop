
import math
import random

class Game:
    def __init__(self, width, height, drag, size, speed):
        self.width = width
        self.height = height
        self.drag = drag
        self.size= size
        self.speed = speed
        self.players = {}
        self.gold = self.Entity(self)

    def addPlayer(self):
        self.players[len(self.players)] = self.Player(self)


    def loop(self):
        for i in self.players:
            player = self.players[i]
            player.vel[0] *= self.drag
            player.vel[1] *= self.drag

            if player.act[0]:
                player.vel[0] -= self.speed
            if player.act[1]:
                player.vel[0] += self.speed
            if player.act[2]:
                player.vel[1] -= self.speed
            if player.act[3]:
                player.vel[1] += self.speed

            player.pos[0] += player.vel[0]
            player.pos[1] += player.vel[1]

            if  player.pos[0] < 0:
                player.pos[0] = 0
                player.vel[0] = abs(player.vel[0])
            if player.pos[0] > self.width - self.size:
                player.pos[0] = self.width - self.size
                player.vel[0] = -abs(player.vel[0])
            if player.pos[1] < 0:
                player.pos[1] = 0
                player.vel[1] = abs(player.vel[1])
            if player.pos[1] > self.height - self.size:
                player.pos[1] = self.height - self.size
                player.vel[1] = -abs(player.vel[1])

            if (player.pos[0]+self.size > self.gold.pos[0] and
                    player.pos[0] < self.gold.pos[0]+self.size and
                    player.pos[1]+self.size > self.gold.pos[1] and
                    player.pos[1] < self.gold.pos[1]+self.size):
                self.gold.pos[0] = random.randint(0, self.width - self.size)
                self.gold.pos[1] = random.randint(0, self.height - self.size)
                player.sco += 1

    class Entity():
        def __init__(self, game):
            self.pos = [
                random.randint(0, game.width - game.size),
                random.randint(0, game.width - game.size)
            ]
            self.vel = [0, 0]
            self.col = (random.randint(128, 192), random.randint(128, 192), random.randint(0, 128))


    class Player(Entity):
        def __init__(self, game):
            super(Game.Player, self).__init__(game)
            self.act = [False, False, False, False] #left, right, up, down
            self.sco = 0
            self.col = (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))

