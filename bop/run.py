
import math
import time

from bop.backend.game import Game as Game
from bop.backend.server import Host
from bop.frontend.director import Director
from bop.frontend.user import User, playerKeys

hosting = True
headless = False
players = 2
userControls = []
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

def questionInt(msg):
    str = msg + " (Int): "
    while True:
        result = input(str)
        try:
            return int(result)
        except ValueError:
            continue

def run():
    global userControls
    global ip

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

    game = Game([width, height], drag, size, speed, not hosting)

    if hosting:
        print("Server starting")
        host = Host(game)
        print("Server started")
    else:
        host = None

    if not headless:
        print("Client starting")
        director = Director(ip, game)
        for userControl in userControls:
            if userControl[0]:
                director.newUser(User(controller=True, joystickID=userControl[1]))
            else:
                director.newUser(User(controller=False, controls=playerKeys[userControl[1]]))
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

if __name__ == '__main__':
    run()
