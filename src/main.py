import sys
import math
import pygame
import random
from copy import deepcopy

from game import Game
from ai import AI

def printOutput(generation, fitness, apples, steps):
	# Prints in a nice format
	print('-' * 20)
	print('Best Of Generation {}'.format(generation))
	print('Fitness: {}'.format(fitness))
	print('Apples: {}'.format(apples))
	print('Steps: {}'.format(steps))

def selectParent(ais, fitnessSum):
	# This function allows us to randomly pick a parent, the chances of each individual to be picked are based on their fitness
	rand = random.uniform(0, fitnessSum)
	currentSum = 0
	for ai in ais:
		currentSum += ai.fitness
		if (currentSum > rand):
			return (ai)

def getFitnessSum(ais):
	# Returns the sum of every individual's fitness
	fitnessSum = 0
	for ai in ais:
		fitnessSum += ai.fitness
	return fitnessSum

def mixWeights(a, b):
	# Mixes the parents weights to create the child
	# Creates a copy of the weights of parentA in order to have the same structure
	weights = deepcopy(a)
	for i in range(len(weights)):
		for j in range(len(weights[i])):
			for k in range(len(weights[i][j])):
				# Each weight is randomly copied from one of the 2 parents
				weights[i][j][k] = (a[i][j][k] if random.randint(0, 1) == 0 else b[i][j][k])
	return weights

def getInputsAI(game):
	# Returns an array of values that will then be fed into the neural network, the values are described in the README
	head = game.snake.snake[0]
	inputs = []

	# This part allows us to see in 8 directions around the car
	views = [
		[
			0, # Step to take in the X axis
			-1 # Step to take in the Y axis
		],
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
		# For each direction we basically cast a ray to find the closest wall
		# On the way to find the wall we also look if we can find the apple and/or the snake's body
		while (tmp[0] >= 0 and tmp[0] < game.width and tmp[1] >= 0 and tmp[1] < game.height):
			tmp[0] += view[0] * game.itemSize
			tmp[1] += view[1] * game.itemSize
			distanceToWall += 1
			if (distanceToSnake == math.inf and tmp in game.snake.snake):
				distanceToSnake = distanceToWall
			elif (distanceToApple == math.inf and tmp == game.apple.apple):
				distanceToApple = distanceToWall
		# We add the distance to the wall, the snake and the apple in the inputs
		inputs += [1 / distanceToWall, 1 / distanceToSnake, 1 / distanceToApple]
		# By doing `1 / value` we ensure that every value in the array is between -1 and 1

	# The direction of the snake is also added to the inputs
	directions = [
		1 if game.snake.direction == 'up' else 0,
		1 if game.snake.direction == 'right' else 0,
		1 if game.snake.direction == 'down' else 0,
		1 if game.snake.direction == 'left' else 0
	]
	inputs += directions

	# We add the direction of the snake's tail to the inputs
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
	pygame.init()
	stop = False

	# Create 500 individuals and randomly initialize their weights
	ais = []
	for i in range(500):
		ai = AI([32, 20, 12, 4], ['relu', 'relu', 'sigmoid'])
		ai.initWeights()
		ais.append(ai)

	generation = 0
	while (not stop):
		for ai in ais:
			# We reset the AI's state before it plays
			ai.reset()
			game = Game()
			while (not game.stop and not game.over):
				game.draw()
				pygame.display.flip()

				# We get the inputs and set them in the neural network
				inputs = getInputsAI(game)
				ai.setInputs(inputs)
				# We start the forward propagation!
				outputs = ai.forwardPropagation()
				# This block is used to translate the neural network's output into an action for the snake
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

				# Exit if the pygame window is closed or if escape is pressed
				for event in pygame.event.get():
					if (event.type == pygame.QUIT):
						game.stop = True
						stop = True
					if (event.type == pygame.KEYDOWN):
						if (event.key == pygame.K_ESCAPE):
							game.stop = True
							stop = True

				game.snake.move()

				ai.steps += 1
				ai.stepsSinceLastApple += 1
				if (game.snake.snake[0] == game.apple.apple):
					ai.stepsSinceLastApple = 0
				if (ai.stepsSinceLastApple > ai.maxSteps):
					# The snake dies if it hasn't eaten an apple in a while
					game.over = True

				game.collision()

			# When an individual dies, we calculate its fitness
			ai.apples = game.points
			ai.fitness = ai.steps + (2**ai.apples + ai.apples**2.1 * 500) - (ai.apples**1.2 * (0.25 * ai.steps)**1.3)
			ai.fitness = max(ai.fitness, 0.1)

			if (stop):
				break
		if (not stop):
			fitnessSum = getFitnessSum(ais)
			# The new generation is made of children whose weights are a mix of the 2 parents, some of those children will also randomly mutate
			children = []
			for _ in range(len(ais) - 1):
				parentA = selectParent(ais, fitnessSum)
				parentB = selectParent(ais, fitnessSum)
				child = deepcopy(parentA)
				child.weights = mixWeights(parentA.weights, parentB.weights)
				if (random.randint(1, 100) <= 20):
					child.mutate()
				children.append(child)
			# We sort the old generation by it's members individual fitness, print the best individual and add it in the next generation
			ais.sort(key=lambda x: x.fitness, reverse=True)
			printOutput(generation, ais[0].fitness, ais[0].apples, ais[0].steps)
			ais = [ais[0]] + children
			generation += 1
	pygame.quit()

def mainPlay():
	# Main for the game
	pygame.init()
	clock = pygame.time.Clock()
	fps = 10

	game = Game()

	# Pretty self explanatory
	while (not game.stop and not game.over):
		clock.tick(fps)
		game.draw()
		pygame.display.flip()

		game.readInput()

		game.snake.move()
		game.collision()
	pygame.quit()

if (__name__ == "__main__"):
	# If the option '-ai' is passed then we want to see the AI play, else we want to play
	if (len(sys.argv) == 2 and sys.argv[1] == '-ai'):
		mainAI()
	else:
		mainPlay()
