import socket
import threading

import time

global clientsocket

import pygame
import sys
from pygame.locals import *

playerKeys = [
    (K_a, K_d, K_w, K_s),
    (K_LEFT, K_RIGHT, K_UP, K_DOWN)
]

fps = 60
gap = 1/fps
lastCheck = 0

if __name__ == '__main__':
    global clientsocket
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 8089))

    l = True
    while l:
        l = False
        global now
        global wait
        global lastCheck

        now = time.time()
        wait = (lastCheck + gap) - now
        lastCheck = now
        if wait > 0:
            time.sleep(wait)

        temp = {
            "com": ["keys"],
            "key": [True, False, False, False]
        }
        data = ""
        for i in temp:
            data += str(i)
            for j in temp[i]:
                data += ":"
                data += str(j)
            data += "|"
        print(data)
        global clientsocket
        clientsocket.send(data.encode())

        keys = pygame.key.get_pressed()
    #    if keys[K_a]:






class Screen:

    class Game:
        def __init__(self, width, height):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        pygame.init()
        self.surface = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption("bop")
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
#        pygame.mixer.music.load('bop.mp3')

    def loop(self):
        keys = pygame.key.get_pressed()
        self.surface.fill((32, 32, 32))

        for i in self.game.players:
            player = self.game.players[i]
            textsurface = self.font.render(str(player.sco), False, player.col)
            self.surface.blit(textsurface, (10, i*35+5))
            if len(self.game.screenSize) == 1:
                pygame.draw.rect(self.surface, player.col, (player.pos[0], 0, self.game.size, self.height))
            else:
                pygame.draw.rect(self.surface, player.col, (player.pos[0], player.pos[1], self.game.size, self.game.size))
            for j, k in enumerate(playerKeys[i%len(playerKeys)]):
                if j >= len(player.act):
                    break
                player.act[j] = keys[k]
        if len(self.game.screenSize) == 1:
            pygame.draw.rect(self.surface, self.game.gold.col, (self.game.gold.pos[0], 0, self.game.size, self.height))
        else:
            pygame.draw.rect(self.surface, self.game.gold.col, (self.game.gold.pos[0], self.game.gold.pos[1], self.game.size, self.game.size))

        if self.game.bop:
#            pygame.mixer.music.play(0)
            self.game.bop = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()