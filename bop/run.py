"""startup script"""

import math
import time

from bop.backend.game import Game as Game
from bop.backend.server import GameServer
from bop.frontend.director import Director
from bop.frontend.user import User, playerKeys

from caduceussocket import SessionManager

# asks a yes or no question
def question(pre_text):
	message = pre_text + " (y/n): "
	while True:
		result = input(message)
		if result == "y" or result == "n":
			return result == "y"

# asks for an integer
def question_int(pre_text):
	message = pre_text + " (Int): "
	while True:
		result = input(message)
		try:
			return int(result)
		except ValueError:
			continue

# main script
def run():
	user_controls = []

	ip = "127.0.0.1"

	width = 400
	height = 300
	drag = 0.90
	size = 4
	speed = math.ceil(((1 - drag) * size) / 1000)

	fps = 60
	gap = 1 / fps

	print("///Bop\\\\\\")

	#  Configuration

	hosting = question("Hosting?")

	if hosting:
		headless = question("Headless?")
	else:
		headless = False
		ip = input("Address?")

	if not headless:
		joystick = 0
		key_controls = 0
		for i in range(question_int("No. of players?")):
			controller = question("Controller for player " + str(i + 1) + "?")
			if controller:
				user_controls.append((controller, joystick))
				joystick += 1
			else:
				user_controls.append((controller, key_controls))
				key_controls += 1

	#  Initialization

	if hosting:
		print("Server starting")
		sm = SessionManager()
		sm.start()

		game = Game([width, height], drag, size, speed, not hosting)
		host = GameServer(game, ip)
		host.start()
		print("Server started")
	else:
		host = None

	if not headless:
		print("Client starting")
		director = Director(ip)
		for userControl in user_controls:
			if userControl[0]:
				director.newUser(User(controller=True, joystickID=userControl[1]))
			else:
				director.newUser(User(controller=False, controls=playerKeys[userControl[1]]))
		director.start()
		print("Client started")
	else:
		director = None

	#  Main game loop

	last_check = 0

	loop = True
	while loop:
		if hosting:
			host.tick()

		if not headless:
			director.sync()

		# wait until next frame
		now = time.time()
		wait = (last_check + gap) - now
		last_check = now
		if wait > 0:
			time.sleep(wait)


if __name__ == '__main__':
	run()
