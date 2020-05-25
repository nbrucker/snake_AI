# import pygame
import sys
from copy import deepcopy
import random

from game import *
from ai import *

def getInputsAI(game):
	head = game.snake.snake[0]
	inputs = []

	views = [
		[0, -1],
		[1, -1],
		[1, 0],
		[1, 1],
		[0, 1],
		[-1, 1],
		[-1, 0],
		[-1, -1]
	]
	for view in views:
		tmp = head.copy()
		distanceToWall = 0
		distanceToSnake = math.inf
		distanceToApple = math.inf
		while (tmp[0] >= 0 and tmp[0] < game.width and tmp[1] >= 0 and tmp[1] < game.height):
			tmp[0] += view[0] * game.itemSize
			tmp[1] += view[1] * game.itemSize
			distanceToWall += 1
			if (distanceToSnake == math.inf and tmp in game.snake.snake):
				distanceToSnake = distanceToWall
			elif (distanceToApple == math.inf and tmp == game.apple.apple):
				distanceToApple = distanceToWall
		inputs += [1 / distanceToWall, 1 / distanceToSnake, 1 / distanceToApple]
	
	directions = [
		1 if game.snake.direction == 'up' else 0,
		1 if game.snake.direction == 'right' else 0,
		1 if game.snake.direction == 'down' else 0,
		1 if game.snake.direction == 'left' else 0
	]
	inputs += directions

	tailIndex = len(game.snake.snake) - 1
	tail = game.snake.snake[tailIndex]
	beforeTail = game.snake.snake[tailIndex - 1]
	inputs += [
		1 if tail[1] > beforeTail[1] else 0,
		1 if tail[0] < beforeTail[0] else 0,
		1 if tail[1] < beforeTail[1] else 0,
		1 if tail[0] > beforeTail[0] else 0
	]

	return inputs

def mainAI():
	# pygame.init()
	# clock = pygame.time.Clock()
	fps = 30
	stop = False

	ais = []
	for i in range(500):
		ai = AI([32, 20, 12, 4], ['relu', 'relu', 'sigmoid'])
		ai.initWeights()
		ais.append(ai)

	generation = 0

	while (not stop):
		for ai in ais:
			ai.reset()
			game = Game()
			while (not game.stop and not game.over):
				# clock.tick(fps)
				# game.draw()
				# pygame.display.flip()
				
				inputs = getInputsAI(game)
				ai.setInputs(inputs)
				outputs = ai.forwardPropagation()
				directions = ['up', 'right', 'down', 'left']
				newDirection = directions[outputs.index(max(outputs))]
				if (newDirection == 'up' and game.snake.direction != 'down'):
					game.snake.direction = newDirection
				if (newDirection == 'right' and game.snake.direction != 'left'):
					game.snake.direction = newDirection
				if (newDirection == 'down' and game.snake.direction != 'up'):
					game.snake.direction = newDirection
				if (newDirection == 'left' and game.snake.direction != 'right'):
					game.snake.direction = newDirection

				# for event in pygame.event.get():
				# 	if (event.type == pygame.QUIT):
				# 		game.stop = True
				# 		stop = True
				# 	if (event.type == pygame.KEYDOWN):
				# 		if (event.key == pygame.K_ESCAPE):
				# 			game.stop = True
				# 			stop = True

				game.snake.move()

				ai.steps += 1
				ai.stepsSinceLastApple += 1
				if (game.snake.snake[0] == game.apple.apple):
					ai.stepsSinceLastApple = 0
				if (ai.stepsSinceLastApple > ai.maxSteps):
					game.over = True

				game.collision()

			ai.apples = game.points
			ai.fitness = ai.steps + (2**ai.apples + ai.apples**2.1 * 500) - (ai.apples**1.2 * (0.25 * ai.steps)**1.3)
			ai.fitness = max(ai.fitness, 0.1)

			if (stop):
				break
		if (not stop):
			fitnessSum = getFitnessSum(ais)
			children = []
			for _ in range(len(ais) - 1):
				parentA = selectParent(ais, fitnessSum)
				parentB = selectParent(ais, fitnessSum)
				child = deepcopy(parentA)
				child.weights = mixWeights(parentA.weights, parentB.weights)
				if (random.randint(1, 100) <= 20):
					child.mutate()
				children.append(child)
			ais.sort(key=lambda x: x.fitness, reverse=True)
			print([generation, ais[0].fitness, ais[0].apples, ais[0].steps])
			ais = [ais[0]] + children
			generation += 1
	# pygame.quit()

def selectParent(ais, fitnessSum):
	rand = random.uniform(0, fitnessSum)
	currentSum = 0
	for ai in ais:
		currentSum += ai.fitness
		if (currentSum > rand):
			return (ai)

def getFitnessSum(ais):
	fitnessSum = 0
	for ai in ais:
		fitnessSum += ai.fitness
	return fitnessSum

def mixWeights(a, b):
	weights = deepcopy(a)
	for i in range(len(weights)):
		for j in range(len(weights[i])):
			for k in range(len(weights[i][j])):
				weights[i][j][k] = (a[i][j][k] if random.randint(0, 1) == 0 else b[i][j][k])
	return weights

def mainPlay():
	pygame.init()
	clock = pygame.time.Clock()
	fps = 10

	game = Game()

	while (not game.stop and not game.over):
		clock.tick(fps)
		game.draw()
		pygame.display.flip()

		game.readInput()

		game.snake.move()
		game.collision()
	pygame.quit()

if __name__ == "__main__":
	if (len(sys.argv) == 2 and sys.argv[1] == '-ai'):
		mainAI()
	else:
		mainPlay()
