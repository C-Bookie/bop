
import pygame
from pygame.locals import *

playerKeys = [
    (K_d, K_a, K_s, K_w),
    (K_RIGHT, K_LEFT, K_DOWN, K_UP)
]

class User():
    def __init__(self, controller=False, joystickID=0, controls=playerKeys[0]):
        self.id = -1
        self.controller = controller
        if self.controller:
            self.joystick = pygame.joystick.Joystick(joystickID)
            self.joystick.init()
        else:
            self.controls = controls

