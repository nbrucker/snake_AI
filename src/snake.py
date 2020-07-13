class Snake():
	def __init__(self, size):
		self.direction = 'down'
		self.size = size
		self.snake = [[100, 120], [100, 100], [100, 80]]
		self.ghost = []

	def move(self):
		# This will simply move the snake
		# We get the new position of the head, add it to the beginning of the array and remove the tail to simulate a movement
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
		# The 'ghost' is simply the previous position of the snake's tail, it will be useful to extend the snake when we get an apple
		self.ghost = self.snake.pop()
