import random
import math

class AI():
	def __init__(self, layers, activations):
		self.layers = [[0] * layer for layer in layers]
		self.weights = []
		if (len(activations) != len(layers) - 1):
			raise Exception('Error')
		self.activations = activations
		self.maxSteps = 100
		self.stepsSinceLastApple = 0
		self.steps = 0
		self.apples = 0
		self.fitness = 0
	
	def reset(self):
		self.stepsSinceLastApple = 0
		self.steps = 0
		self.apples = 0
		self.fitness = 0

	def initWeights(self):
		weights = []
		for index in range(len(self.layers) - 1):
			layer = []
			for _ in self.layers[index + 1]:
				neuron = []
				for _ in self.layers[index]:
					neuron.append(random.uniform(-1, 1))
				layer.append(neuron)
			weights.append(layer)
		self.weights = weights

	def mutate(self):
		for i in range(len(self.weights)):
			for j in range(len(self.weights[i])):
				for k in range(len(self.weights[i][j])):
					if (random.randint(1, 100) <= 1):
						x = self.weights[i][j][k] + random.uniform(-0.1, 0.1)
						x = max(min(x, 1), -1)
						self.weights[i][j][k] = x

	def setInputs(self, inputs):
		if (len(inputs) != len(self.layers[0])):
			raise Exception('Error')
		self.layers[0] = inputs.copy()

	def forwardPropagation(self):
		for layerIndex in range(1, len(self.layers)):
			for neuronIndex in range(len(self.layers[layerIndex])):
				value = 0
				for previousNeuronIndex in range(len(self.layers[layerIndex - 1])):
					value += self.layers[layerIndex - 1][previousNeuronIndex] * self.weights[layerIndex - 1][neuronIndex][previousNeuronIndex]
				if (self.activations[layerIndex - 1] == 'sigmoid'):
					self.layers[layerIndex][neuronIndex] = self.sigmoid(value)
				else:
					self.layers[layerIndex][neuronIndex] = self.relu(value)
		return self.layers[len(self.layers) - 1].copy()

	def relu(self, x):
		return max(0, x)

	def sigmoid(self, x):
		return 1 / (1 + math.exp(-x))
