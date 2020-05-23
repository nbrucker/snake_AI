import pygame

from snake import *
from apple import *

class Game():
	def __init__(self):
		self.width = 200
		self.height = 200
		self.stop = False
		self.over = False
		# self.screen = pygame.display.set_mode((self.width, self.height))
		self.itemSize = 20
		self.snake = Snake(self.itemSize)
		self.apple = Apple(self.itemSize)
		self.apple.getNewPosition(self)
		self.points = 0
	
	def draw(self):
		self.screen.fill([0, 0, 0])
		pygame.draw.rect(self.screen, [0, 255, 0], [self.apple.apple[0], self.apple.apple[1], self.itemSize, self.itemSize])
		for item in self.snake.snake:
			pygame.draw.rect(self.screen, [255, 255, 255], [item[0], item[1], self.itemSize, self.itemSize])

	def readInput(self):
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
		if (head in self.snake.snake[1:]):
			self.over = True
		if (head[0] < 0 or head[0] >= self.width or head[1] < 0 or head[1] >= self.height):
			self.over = True
		if (head == self.apple.apple):
			self.points += 1
			self.snake.snake.append(self.snake.ghost)
			self.apple.getNewPosition(self)
