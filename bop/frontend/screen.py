"""screen(GUI)"""

import sys

import pygame
from pygame.locals import *


deadzone = 0.25

def correctJoy(n):
    if n < deadzone and n > -deadzone:
        return 0
    if n < 0:
        return -n**2
    return n**2


class Screen:
    def __init__(self):
        self.ready = False
        self.users = {}
        pygame.init()
        self.surface = pygame.display.set_mode((400, 300), 0, 32)
        pygame.display.set_caption("bop")
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

        # pygame.mixer.music.load('bop.wav')

    def setup(self, screenSize, size, bop):
        self.screenSize = screenSize
        self.size = size
        self.bop = bop

        # if len(self.screenSize) == 1:  # fixme
        #     self.surface = pygame.display.set_mode((self.screenSize[0], 300), 0, 32)
        # else:
        #     self.surface = pygame.display.set_mode((self.screenSize[0], self.screenSize[1]), 0, 32)

        self.ready = True

    def addUser(self, user):
        self.users[user.id] = user

    def loop(self, data):
        keys = pygame.key.get_pressed()
        self.surface.fill((32, 32, 32))

        for i in data["players"]:
            player = data["players"][i]
            i = int(i)  # fixme JSON converting int keys to string
            textsurface = self.font.render(str(player["sco"]), False, player["col"])
            self.surface.blit(textsurface, (10, i*35+5))
            if len(self.screenSize) == 1:
                pygame.draw.rect(self.surface, player["col"], (player["pos"][0], 0, self.size, self.screenSize[1]))
            else:
                pygame.draw.rect(self.surface, player["col"], (player["pos"][0], player["pos"][1], self.size, self.size))

            if i in self.users:
                user = self.users[i]
                if user.controller:
                    player["act"][0] = correctJoy(user.joystick.get_axis(0))
                    player["act"][2] = correctJoy(user.joystick.get_axis(1))
                else:
                    for key, val in enumerate(user.controls):
                        player["act"][key] = 1 if keys[val] else 0

        if len(self.screenSize) == 1:
            pygame.draw.rect(self.surface, data["gold"]["col"], (data["gold"]["pos"][0], 0, self.size, self.screenSize[1]))
        else:
            pygame.draw.rect(self.surface, data["gold"]["col"], (data["gold"]["pos"][0], data["gold"]["pos"][1], self.size, self.size))

        if self.bop:
#            pygame.mixer.music.play(0)
            self.bop = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

        return data


