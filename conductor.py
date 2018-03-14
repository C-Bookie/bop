
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
drag = 0.5
size = 4
speed = math.ceil(size / 4)

fps = 60
gap = 1 / fps

def question(msg):
    str = msg + " (y/n): "
    while True:
        result = input(str)
        if result == "y" or result == "n":
            return result == "y"


##test begin

class A():
    def __init__(self, n):
        self.n = n

class Class1(threading.Thread):
    def __init__(self, a):
        threading.Thread.__init__(self)
        self.a = a

    def run(self):
        self.a.n = 1

class Class2(threading.Thread):
    def __init__(self, a):
        threading.Thread.__init__(self)
        self.a = a

    def run(self):
        self.a.n = 2


if __name__ == '__main__':

    a = A(0)

    class1 = Class1(a)
    class1.deamon = True
    class1.run()

    class2 = Class2(a)
    class2.deamon = True
    class2.run()

    raise Exception(str(a.n))

##test end

    print("///Bop\\\\\\")

    hosting = question("Hosting?")

    if hosting:
        headless = question("Headless?")
    else:
        headless = False
        ip = input("Address?")

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
        screen = screen.Screen(game, [client.id])

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


