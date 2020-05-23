import random

class Apple():
	def __init__(self, size):
		self.size = size
		self.apple = [0, 0]

	def getNewPosition(self, game):
		freePositions = []
		for x in range(int(game.width / game.itemSize)):
			for y in range(int(game.height / game.itemSize)):
				position = [x * game.itemSize, y * game.itemSize]
				if (position not in game.snake.snake):
					freePositions.append(position)
		number = random.randint(0, len(freePositions) - 1)
		self.apple = freePositions[number]
