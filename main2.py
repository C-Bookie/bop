
import game
import screen

import math
import time

width = 400
height = 300

fps = 60
gap = 1 / fps

drag = 0.4578
size = 10

if __name__ == '__main__':
    game = game.Game(width, height, drag, size, math.ceil(size / 4))
    screen = screen.Screen(game)

    game.addPlayer()
    game.addPlayer()

    lastCheck = 0

    while True:
        game.loop()
        screen.loop()

        now = time.time()
        wait = (lastCheck + gap) - now
        lastCheck = now
        if wait > 0:
            time.sleep(wait)

