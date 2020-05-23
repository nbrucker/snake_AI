class Snake():
	def __init__(self, size):
		self.direction = 'down'
		self.size = size
		self.snake = [[100, 100], [100, 80], [100, 120]]
		self.ghost = self.snake[0]

	def move(self):
			head = self.snake[0]
			new = []
			if (self.direction == 'left'):
				new = [head[0] - self.size, head[1]]
			elif (self.direction == 'right'):
				new = [head[0] + self.size, head[1]]
			elif (self.direction == 'up'):
				new = [head[0], head[1] - self.size]
			elif (self.direction == 'down'):
				new = [head[0], head[1] + self.size]
			self.snake.insert(0, new)
			self.ghost = self.snake.pop()
