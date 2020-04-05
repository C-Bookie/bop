"""mocking library for reproducible results"""

class Random:
	def __init__(self):
		self.i = 0

	def seed(self, i):
		self.i = i

	def randint(self, min, max):
		result = ((2 << self.i) % (max - min)) + min
		self.i += 1
		return result


random = Random()
randint = random.randint
seed = random.seed
