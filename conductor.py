
import math
import time

import game, screen, director
import server, user

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
    str = msg + " (Int): "
    while True:
        result = input(str)
        try:
            return int(result)
        except ValueError:
            continue

if __name__ == '__main__':
    print("///Bop\\\\\\")

    ##configuration

    hosting = question("Hosting?")

    if hosting:
        headless = question("Headless?")
    else:
        headless = False
        ip = input("Address?")

    if not headless:
        userControls = []
        joystick = 0
        keyControls = 0
        for i in range(questionInt("No. of players?")):
            controller = question("Controller for player " + str(i+1) + "?")
            if controller:
                userControls.append((controller, joystick))
                joystick+=1
            else:
                userControls.append((controller, keyControls))
                keyControls+=1

    #    botCount = questionInt("No. of Bots?")

    ##initialization

    game = game.Game([width, height], drag, size, speed, not hosting)

    if hosting:
        print("Server starting")
        host = server.Host(game)
        print("Server started")
    else:
        host = None

    if not headless:
        print("Client starting")
        director = director.Director(ip, game)
        for userControl in userControls:
            if userControl[0]:
                director.newUser(user.User(controller=True, joystickID=userControl[1]))
            else:
                director.newUser(user.User(controller=False, controls=user.playerKeys[userControl[1]]))
        print("Client started")
    else:
        director = None

    ##main game loop

    lastCheck = 0

    loop = True
    while loop:
        game.loop()

        if hosting:
            host.sync()

        if not headless:
            director.loop()

        now = time.time()
        wait = (lastCheck + gap) - now
        lastCheck = now
        if wait > 0:
            time.sleep(wait)


