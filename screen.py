
import pygame, sys
from pygame.locals import *

playerKeys = [
    (K_a, K_d, K_w, K_s),
    (K_LEFT, K_RIGHT, K_UP, K_DOWN)
]

class Screen:

    def __init__(self, game):
        self.game = game
        pygame.init()
        self.surface = pygame.display.set_mode((game.width, game.height), 0, 32)
        pygame.display.set_caption("bop")
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

    def loop(self):
        keys = pygame.key.get_pressed()
        self.surface.fill((32, 32, 32))

        for i in self.game.players:
            player = self.game.players[i]
            textsurface = self.font.render(str(player.sco), False, player.col)
            self.surface.blit(textsurface, (10, i*30+10))
            pygame.draw.rect(self.surface, player.col, (player.pos[0], player.pos[1], self.game.size, self.game.size))
            for j, k in enumerate(playerKeys[i%len(playerKeys)]):
                player.act[j] = keys[k]
        pygame.draw.rect(self.surface, self.game.gold.col, (self.game.gold.pos[0], self.game.gold.pos[1], self.game.size, self.game.size))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


