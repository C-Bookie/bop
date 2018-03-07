
import pygame
import sys
from pygame.locals import *

playerKeys = [
    (K_a, K_d, K_w, K_s),
    (K_LEFT, K_RIGHT, K_UP, K_DOWN)
]

class Screen:

    def __init__(self, game):
        self.game = game
        pygame.init()
        if len(self.game.screenSize) == 1:
            self.surface = pygame.display.set_mode((game.screenSize[0], 300), 0, 32)
        else:
            self.surface = pygame.display.set_mode((game.screenSize[0], game.screenSize[1]), 0, 32)
        pygame.display.set_caption("bop")
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

#        pygame.mixer.music.load('bop.wav')

    def loop(self):
        keys = pygame.key.get_pressed()
        self.surface.fill((32, 32, 32))

        for i in self.game.data["players"]:
            player = self.game.data["players"][i]
            textsurface = self.font.render(str(player.sco), False, player.col)
            self.surface.blit(textsurface, (10, i*35+5))
            if len(self.game.screenSize) == 1:
                pygame.draw.rect(self.surface, player.col, (player.pos[0], 0, self.game.size, self.game.screenSize[1]))
            else:
                pygame.draw.rect(self.surface, player.col, (player.pos[0], player.pos[1], self.game.size, self.game.size))
            for j, k in enumerate(playerKeys[i%len(playerKeys)]):
                if j >= len(player.act):
                    break
                player.act[j] = keys[k]
        if len(self.game.screenSize) == 1:
            pygame.draw.rect(self.surface, self.game.data["gold"].col, (self.game.data["gold"].pos[0], 0, self.game.size, self.game.screenSize[1]))
        else:
            pygame.draw.rect(self.surface, self.game.data["gold"].col, (self.game.data["gold"].pos[0], self.game.data["gold"].pos[1], self.game.size, self.game.size))

        if self.game.bop:
#            pygame.mixer.music.play(0)
            self.game.bop = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


