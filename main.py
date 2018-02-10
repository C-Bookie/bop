
import pygame, sys
from pygame.locals import *

import time
import math
import random

fps = 60
gap = 1/fps
lastCheck = 0

cycle = 0

change = 3
changeCycle = fps * change

#true if player 1
state = True

width = 400
height = 300

px1 = 10
py1 = 10

px2 = 90
py2 = 10


vx1 = 0
vy1 = 0

vx2 = 0
vy2 = 0

gx = 50
gy = 50

s1 = 0
s2 = 0

size = 10
speed = math.ceil(size/4)

def init():
    pygame.init()
    global surface
    surface = pygame.display.set_mode((width, height), 0, 32)
    pygame.display.set_caption("bop")

def draw():
    global surface
    surface.fill((32, 32, 32))

    pygame.draw.rect(surface, (128, 128, 224), (px1, py1, size, size))
#    pygame.draw.rect(surface, (224, 224, 128) if state else (128, 224, 224), (px1, py1, size, size), math.ceil(size/4))
    pygame.draw.rect(surface, (224, 128, 128), (px2, py2, size, size))
#    pygame.draw.rect(surface, (224, 224, 128) if not state else (128, 224, 224), (px2, py2, size, size), math.ceil(size/4))
    pygame.draw.rect(surface, (224, 128, 128), (px2, py2, size, size))
    pygame.draw.rect(surface, (224, 224, 128), (gx, gy, size, size))

def loop():
    global px1
    global py1
    global px2
    global py2

    global vx1
    global vy1
    global vx2
    global vy2

    drag = 0.4578

    vx1*=drag
    vy1*=drag
    vx2*=drag
    vy2*=drag

    keys = pygame.key.get_pressed()
    if keys[K_a]:
        vx1 -= speed
    if keys[K_d]:
        vx1 += speed
    if keys[K_w]:
        vy1 -= speed
    if keys[K_s]:
        vy1 += speed

    if keys[K_LEFT]:
        vx2 -= speed
    if keys[K_RIGHT]:
        vx2 += speed
    if keys[K_UP]:
        vy2 -= speed
    if keys[K_DOWN]:
        vy2 += speed

    px1+=vx1
    py1+=vy1
    px2+=vx2
    py2+=vy2

    if  px1 < 0:
        px1 = 0
        vx1 = abs(vx1)
    if px1 > width - size:
        px1 = width - size
        vx1 = -abs(vx1)
    if py1 < 0:
        py1 = 0
        vy1 = abs(vy1)
    if py1 > height - size:
        py1 = height - size
        vy1 = -abs(vy1)

    if  px2 < 0:
        px2 = 0
        vx2 = abs(vx2)
    if px2 > width - size:
        px2 = width - size
        vx2 = -abs(vx2)
    if py2 < 0:
        py2 = 0
        vy2 = abs(vy2)
    if py2 > height - size:
        py2 = height - size
        vy2 = -abs(vy2)

    global gx
    global gy
    global s1
    global s2

    if px1+size > gx and px1 < gx+size and py1+size > gy and py1 < gy+size:
        gx = random.randint(0, width - size)
        gy = random.randint(0, height - size)
        s1 += 1
        print(str(s1)+":"+str(s2))
    if px2 + size > gx and px2 < gx + size and py2 + size > gy and py2 < gy + size:
        gx = random.randint(0, width - size)
        gy = random.randint(0, height - size)
        s2 += 1
        print(str(s1) + ":" + str(s2))



def paint():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()



if __name__ == '__main__':
    init()
    while 1:
        loop()
        draw()
        paint()

        now = time.time()
        wait = (lastCheck + gap) - now
        lastCheck = now
        if wait > 0:
            time.sleep(wait)
