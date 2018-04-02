
import math
import time

import game, screen, director
import client, server

import threading

hosting = True
headless = False
players = 2
userControls = []
Bot = False

ip = "localhost"

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

def questionInt(msg):
    str = msg + ": "
    while True:
        result = input(str)
        try:
            return int(result)
        except ValueError:
            continue

if __name__ == '__main__':
    print("///Bop\\\\\\")

    hosting = question("Hosting?")

    if hosting:
        headless = question("Headless?")
    else:
        headless = False
        ip = input("Address?")

    if not headless:
        players = questionInt("No. of players")
        userControls = []
        for i in range(players):
            joystick = 0
            keyControles = 0
            controller = question("Controller for player " + str(i+1) + "?")
            if controller:
                userControls.append((controller, joystick))
                joystick+=1
            else:
                userControls.append((controller, keyControles))
                keyControles+=1

    #    bot = question("Bot?")


    game = game.Game([width, height], drag, size, speed, not hosting)

    if hosting:
        print("Server starting")
        host = server.Host(game)
        print("server started")

    if not headless:
        print("Client starting")

        client = client.Client(game, ip)
        users = []
        for i in range(players):
            users.append(screen.Screen.user(client.id, False, controls=screen.playerKeys[0]))
        screen = screen.Screen(game, users)

        print("Client started")

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


