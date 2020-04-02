
from bop.run import *

import pygame

import json

from tests import mock_random


class UserPlayback(User):
	def __init__(self, record):
		self.id = -1
		self.controller = True
		self.joystick = self.Joystick()
		self.record = iter(record)

	def next(self):
		self.joystick.values = next(self.record)

	class Joystick:
		def __init__(self):
			self.values = (0, 0)

		def get_axis(self, axis):
			return self.values[axis]

class UserRecorder(User):
	def __init__(self, joystickID=0):
		super().__init__()
		self.id = -1
		self.controller = True
		self.joystick = self.Joystick(joystickID)

	def next(self):
		self.joystick.next()

	class Joystick:
		def __init__(self, joystickID=0):
			self.values = (0, 0)
			self.joystick = pygame.joystick.Joystick(joystickID)
			self.joystick.init()

		def next(self):
			self.values = (self.joystick.get_axis(0), self.joystick.get_axis(1))

		def get_axis(self, axis):
			return self.values[axis]


class Recorder:
	def __init__(self):
		self.recorded_input = []
		self.recorded_output = []

		self.game = Game([width, height], drag, size, speed, not hosting, randomAPI=mock_random)
		self.host = Host(self.game)
		self.director = Director(ip, self.game)

		self.user_recorder = UserRecorder()
		self.director.newUser(self.user_recorder)

		time.sleep(1)

	class Encoder(json.JSONEncoder):
		def default(self, o):
			return str(o)

	def recorder(self, file_path, frames):
		print("Beginning recording")

		encoder = self.Encoder()

		lastCheck = 0

		for _frame in range(frames):
			self.user_recorder.next()
			self.game.loop()
			self.host.sync()
			self.director.loop()

			self.recorded_input.append(self.user_recorder.joystick.values)
			self.recorded_output.append(encoder.encode(self.game.data))

			now = time.time()
			wait = (lastCheck + gap) - now
			lastCheck = now
			if wait > 0:
				time.sleep(wait)

		recorded = {
			"input": self.recorded_input,
			"output": self.recorded_output
		}

		with open(file_path, 'w') as outfile:
			json.dump(recorded, outfile)


if __name__ == "__main__":
	rec = Recorder()
	rec.recorder("test1.json", 600)



