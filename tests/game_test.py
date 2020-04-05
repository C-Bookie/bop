"""controller/keyboard handling playback and comparison"""

import unittest

from bop.run import *
from bop import __version__

from tests import game_recorder, mock_random

import json
import time


class MyTestCase(unittest.TestCase):
	def setUp(self):
		hosting = True

		ip = "127.0.0.1"

		width = 400
		height = 300
		drag = 0.90
		size = 4
		speed = math.ceil(((1 - drag) * size) / 1000)  # fixme


		sm = SessionManager()
		sm.start()

		self.game = Game([width, height], drag, size, speed, not hosting, mock_random)
		self.host = GameServer(self.game, ip)
		self.host.start()
		self.director = Director(ip)
		self.director.start()

	def test_1(self):
		assert __version__ == '0.1.4'

		with open('test1.json') as json_file:
			recorded = json.load(json_file)

		self.user_playback = game_recorder.UserPlayback(recorded["input"])
		self.director.newUser(self.user_playback)

		time.sleep(1)

		print("Beginning test 1")
		print("Using record:")
		print(recorded)

		encoder = game_recorder.Recorder.Encoder()

		for output in recorded["output"]:
			self.user_playback.next()
			self.host.tick()
			self.director.sync()

			self.assertEqual(output, encoder.encode(self.game.data))


if __name__ == '__main__':
	unittest.main()
