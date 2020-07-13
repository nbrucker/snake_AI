import pygame

from snake import Snake
from apple import Apple

class Game():
	def __init__(self):
		# Initialization
		self.width = 200
		self.height = 200
		self.stop = False
		self.over = False
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.itemSize = 20
		self.snake = Snake(self.itemSize)
		self.apple = Apple(self.itemSize)
		self.apple.getNewPosition(self)
		self.points = 0
	
	def draw(self):
		# Set the black background
		self.screen.fill([0, 0, 0])
		# Draw the apple
		pygame.draw.rect(self.screen, [0, 255, 0], [self.apple.apple[0], self.apple.apple[1], self.itemSize, self.itemSize])
		# Draw the snake
		for item in self.snake.snake:
			pygame.draw.rect(self.screen, [255, 255, 255], [item[0], item[1], self.itemSize, self.itemSize])

	def readInput(self):
		# This function will read the input from the keyboard and set the snake position accordingly
		# The snake can't go in a direction if he is already going in the opposite one
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				self.stop = True
			if (event.type == pygame.KEYDOWN):
				if (event.key == pygame.K_ESCAPE):
					self.stop = True
				elif (event.key == pygame.K_LEFT and self.snake.direction != 'right'):
					self.snake.direction = 'left'
				elif (event.key == pygame.K_RIGHT and self.snake.direction != 'left'):
					self.snake.direction = 'right'
				elif (event.key == pygame.K_UP and self.snake.direction != 'down'):
					self.snake.direction = 'up'
				elif (event.key == pygame.K_DOWN and self.snake.direction != 'up'):
					self.snake.direction = 'down'

	def collision(self):
		head = self.snake.snake[0]
		# Checking the collision with itself
		if (head in self.snake.snake[1:]):
			self.over = True
		# Checking the collision with a wall
		if (head[0] < 0 or head[0] >= self.width or head[1] < 0 or head[1] >= self.height):
			self.over = True
		# Checking the collision with the apple
		if (head == self.apple.apple):
			# If we are on the apple, add a point, extend the snake and set the apple to a new position
			self.points += 1
			self.snake.snake.append(self.snake.ghost)
			self.apple.getNewPosition(self)
