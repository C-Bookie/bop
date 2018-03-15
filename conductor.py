
import math
import time

import game, screen
import client, server

import threading

hosting = True
headless = False
Bot = False

ip = "127.0.0.1"

width = 400
height = 300
drag = 0.90
size = 4
speed = math.ceil(((1-drag)*size) / 1000)   #fixme

fps = 60
gap = 1 / fps

def question(msg):
    str = msg + " (y/n): "
    while True:
        result = input(str)
        if result == "y" or result == "n":
            return result == "y"


if __name__ == '__main__':

    print("///Bop\\\\\\")

    hosting = question("Hosting?")

    if hosting:
        headless = question("Headless?")
    else:
        headless = False
        ip = input("Address?")

    if not headless:
        controller = question("Controller?")

    #    bot = question("Bot?")


    game = game.Game([width, height], drag, size, speed, not hosting)

    if hosting:
        print("Server starting")
        host = server.Host(game)
        host.daemon = True

        host.start()
        print("server started")

    if not headless:
        print("Client starting")
        client = client.Client(game)
        screen = screen.Screen(game, [client.id], controller)

        client.daemon = True
        print("Client started")

        client.start()

    lastCheck = 0

    loop = True
    while loop:
        game.loop()

        if hosting:
            host.sync()

        if not headless:
            client.game.loop()
            screen.loop()
            client.sync()

        now = time.time()
        wait = (lastCheck + gap) - now
        lastCheck = now
        if wait > 0:
            time.sleep(wait)


