import json

import pygame

class user():
    def __init__(self, client, id, controller=False, joystickID=0, controls=()):
        self.client = client
        self.id = id
        self.controller = controller
        if self.controller:
            self.joystick = pygame.joystick.Joystick(joystickID)
            self.joystick.init()
        else:
            self.controls = controls

