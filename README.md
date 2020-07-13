# Snake AI

The goal of this project was to create an AI that would learn how to play Snake.

The AI is using a genetic algorithm to evolve. Each generation is composed of 500 individuals.
The neural network is made up of:
- An input layer of 32 neurons.
- An hidden layer of 20 neurons with a relu activation.
- Another hidden layer of 12 neurons also with a relu activation.
- An output layer of 4 neurons with a sigmoid activation.

The snake sees in 8 directions around itself.
The neural network is fed:
- 24 values for the distance to the wall, to itself and to the apple in each of those 8 directions.
- 4 values for the direction of the snake's head
- 4 values for the direction of the snake's tail

The snake has then 4 possible actions since the neural network has an output layer of 4 neurons: go up, down, left or right.
We will execute the action of the neuron with the highest value.

All the 500 individuals will play one after another and each will die if they hit a wall or do not eat an apple within 100 steps.
When an individual dies we calculate its fitness.
Here's the fitness calculation function:
```python
steps + (2**apples + apples**2.1 * 500) - (apples**1.2 * (0.25 * steps)**1.3)
```
'steps' is the number of steps the snake did before dying.\
'apples' is the number of apples that the snake ate.

We put such a big emphasis on apples to entice the snake to eat them as fast as possible.

When each individual in the current generation is done playing we create 499 children.
For each child we choose 2 parents from the previous generation.
Here comes in play our genetic algorithm.
The parents are chosen randomly but the higher the fitness of an individual is, the higher chances are for him to be picked as a parent.
The weights of the child are a mix of the weights of both of his parents, each child then has an 20% chances to mutate.
If the child mutates every single one of his weights has a 1% chances to be modified to a new, random value.

The 499 children are then put in the next generation along with the best individual from the previous one (The individual with the highest fitness).

## Installation

Use the package manager pip to install pygame

```bash
pip install pygame
```

## Usage

To simply play
```bash
python src/main.py
```

To watch the AI learn
```bash
python src/main.py -ai
```
