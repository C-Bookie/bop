
import sys

import pygame
from pygame.locals import *

import math

playerKeys = [
    (K_d, K_a, K_s, K_w),
    (K_RIGHT, K_LEFT, K_DOWN, K_UP)
]

deadzone = 0.25

def correctJoy(n):
    if n < deadzone and n > -deadzone:
        return 0
    if n < 0:
        return -n**2
    return n**2


class Screen:

    def __init__(self, game, users, controller):
        self.game = game
        self.users = users
        pygame.init()
        if len(self.game.screenSize) == 1:
            self.surface = pygame.display.set_mode((game.screenSize[0], 300), 0, 32)
        else:
            self.surface = pygame.display.set_mode((game.screenSize[0], game.screenSize[1]), 0, 32)
        pygame.display.set_caption("bop")
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

        self.joyStick = controller
        if self.joyStick:
            self.joystickO = pygame.joystick.Joystick(0)
            self.joystickO.init()

#        pygame.mixer.music.load('bop.wav')

    def loop(self):
        keys = pygame.key.get_pressed()
        self.surface.fill((32, 32, 32))

        l = 0
        tempData = self.game.data
        for i in tempData["players"]:
            player = tempData["players"][i]
            textsurface = self.font.render(str(player.sco), False, player.col)
            self.surface.blit(textsurface, (10, i*35+5))
            if len(self.game.screenSize) == 1:
                pygame.draw.rect(self.surface, player.col, (player.pos[0], 0, self.game.size, self.game.screenSize[1]))
            else:
                pygame.draw.rect(self.surface, player.col, (player.pos[0], player.pos[1], self.game.size, self.game.size))
            if i in self.users:
                if self.joyStick:
                    player.act[0] = correctJoy(self.joystickO.get_axis(0))
                    player.act[2] = correctJoy(self.joystickO.get_axis(1))
                else:
                    for j, k in enumerate(playerKeys[l%len(playerKeys)]):
                        if j >= len(player.act):
                            break
                        player.act[j] = 1*keys[k]

                l+=1
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


