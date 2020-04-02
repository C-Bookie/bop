import unittest

from conductor import *
from game import Game
from director import Director

import game_recorder

import json
import time

import mock_random

class MyTestCase(unittest.TestCase):
	def setUp(self):
		self.game = Game(mock_random, [width, height], drag, size, speed, not hosting)
		self.host = server.Host(self.game)
		self.director = Director(ip, self.game)

	def test_1(self):
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
			self.game.loop()
			self.host.sync()
			self.director.loop()

			self.assertEqual(output, encoder.encode(self.game.data))


if __name__ == '__main__':
	unittest.main()
