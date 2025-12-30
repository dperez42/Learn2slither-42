# Learn2slither-42

# About the project

Learn2Slither is a 42 school project focused on implementing a **reinforcement learning** agent for the Snake game.
The project involves creating an AI that learns to navigate through **Q-learning** implementation, enabling the snake to collect apples while avoiding collisions.

## Environment Specifications

- Board size: 10x10 grid
- Two green apples randomly placed (increase snake length)
- One red apple randomly placed (decrease snake length)
- Initial snake length: 3 cells
- Game ending conditions: wall collision, self-collision, or zero length

## States and Actions
The snake agent operates with information from **four directions around its head**, representing its local perception of the environment.




This restriction shapes the state space and decision-making process. The agent's actions are limited to four directional movements: UP, LEFT, DOWN, and RIGHT.

## Neural Architecture

The agent processes information about the game state through a simple **deep neural network (DNN)** with multiple layers. The architecture begins with 20 input neurons that capture essential environmental data, processes this through two hidden layers, and produces action values through the output layer.

### Input Layer (20 neurons)
The input layer consists of two types of environmental sensors:

#### Distance Measurements (16 neurons)
Each direction contains 4 normalized distance values representing:

- Distance to the nearest **wall**
- Distance to the nearest **green apple**
- Distance to the nearest **red apple**
- Distance to the nearest **snake body segment**

#### Danger Detection (4 neurons)
Four binary neurons (0 or 1) detect **immediate collision threats in adjacent cells**. These neurons activate when:

- A wall is directly adjacent in that direction
- A snake body segment is directly adjacent in that direction

### Hidden Layers

The network processes this input through two hidden layers:

- **First hidden layer** contains 128 neurons, allowing for complex pattern recognition
- **Second hidden layer** contains 64 neurons, further refining these patterns

### Output Layer

The final layer consists of 4 neurons, each corresponding to a possible movement direction (UP, DOWN, LEFT, RIGHT). These neurons output **Q-values**, representing the **expected future reward for each action** in the current state.

## Bonus Features
Bonus points are awarded for:

- Achieving snake lengths beyond 10 during sessions (15, 20, 25, 30, 35)
- Creating a polished visual interface
- Enabling the snake to generalize its learning across different grid sizes


# Installation

## Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- git

## Installation instructions

```bash
# Clone repository
git clone h

# Go to directory
cd AI_snake

# Create virtual environnement
python3 -m venv .venv

# Activate virtual environnement
# Linux/macOS:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

# Install required packages in virtual environnement
pip install -r requirements.txt
```

# Usage

The program can be run with various options to control its behavior:

`python3 main.py [options]`

## Available Options

#### Training and Model Management
- `-t, --train`: Enable training mode for the AI agent
- `-e EPISODE, --episode EPISODE`: Specify the number of episodes to run
- `-m MODEL, --model MODEL`: Load a pre-trained model from a specified path

#### Visualization and Debug
- `-v {on,off}, --visual {on,off}`: Enable or disable the GUI (if you want to train your model faster, disable visualization to reduce computational overhead)
- `-step-by-step`: Enable step-by-step mode for detailed observation
- `-plot OUTPUT_FILENAME`: Save training statistics plots to a specified filename

Example of a training statistics plot:

<p align="center">
</p>

#### Game Modes

- `-p, --player`: Enable player mode to play the game manually

## Usage Examples
Train the AI for 1000 episodes with visualization:
```bash
python3 main.py -t -e 1000
```

Load a pre-trained model and watch it play:
```bash
python3 main.py -m model/trained_model.pth
```

Train without visualization for faster processing:
```bash
python3 main.py -t -e 1000 -v off
```

## Settings

You can modify basic parameters in `settings.py` like grid size, fruit population, initial snake length and game speed. Since a model can generalize its learning across different grid sizes, you can experiment with settings like:

```python
# Default game size
GRID_SIZE = 30
CELL_SIZE = 15
...
# Default game settings
SNAKE_SIZE = 3
GREEN_FRUITS_NB = 300
RED_FRUITS_NB = 300
...
# Game speed
FPS = 150
```
Here's what it looks like in action:
<p align="center">
</p>



# Info
Example using Q-tables
https://github.com/yumatsui00/learn2slither/blob/main/main.py

Example with RN
https://github.com/Sleleu/Learn2slither/tree/main/srcs/game

tutorial
https://www.geeksforgeeks.org/deep-learning/how-are-neural-networks-used-in-deep-q-learning/

## Theory
Deep Q-Learning is a subset of reinforcement learning, a branch of artificial intelligence (AI) that focuses on how agents take actions in an environment to maximize cumulative reward. In traditional Q-learning, a table (called the Q-table) is used to store the estimated rewards for each state-action pair, helping an agent choose the best possible actions. However, when dealing with complex environments with large or continuous state spaces, a Q-table becomes impractical. This is where Deep Q-Learning comes into play, utilizing neural networks to approximate the Q-values.

Understanding Q-Learning

https://www.geeksforgeeks.org/machine-learning/q-learning-in-python/


Need for Deep Q-Learning
When the environment has too many possible states (like pixel-level input in a video game or continuous action spaces in robotics), using a Q-table is computationally expensive. Deep Q-Learning overcomes this by using a neural network to approximate the Q-function instead of using a table.

Role of Neural Networks in Deep Q-Learning
In Deep Q-Learning, a neural network, often referred to as a Deep Q-Network (DQN), replaces the Q-table and learns to predict Q-values for given state-action pairs. This allows the agent to generalize and handle environments with large state spaces efficiently.

Structure of a Deep Q-Network (DQN)
The neural network in DQN consists of the following key components:

Input Layer: The input to the network is the current state of the environment, typically represented as a feature vector. For example, in an image-based environment (e.g., a video game), the input might be a pixel representation of the game’s state.

Hidden Layers: The hidden layers in a DQN extract features from the input data. These layers can include fully connected layers, convolutional layers (for image-based input), and activation functions (like ReLU). The neural network learns complex features from the environment through these layers.

Output Layer: The output layer provides the Q-values for all possible actions in the current state. If the agent can choose from n actions, the output layer will have n nodes, each representing the Q-value for a particular action in the given state.

Training the Neural Network
The neural network is trained using a variant of the Q-learning update rule. The key idea is to minimize the temporal difference (TD) error, which represents the difference between the predicted Q-value and the target Q-value. The target Q-value is obtained using the following equation:

Target=R(t+1)+γ⋅maxa′Q(s′,a′)

The loss function for the neural network is computed as:

Loss=[Q(s,a)−(R(t+1)+γ⋅max⁡a′Q(s′,a′))]2

The network parameters (weights and biases) are updated using gradient descent to minimize this loss function.

Exploration vs. Exploitation

In reinforcement learning, an agent needs to balance exploration (trying out new actions) and exploitation (leveraging learned knowledge to maximize rewards). In Deep Q-Learning, this is typically achieved using an epsilon-greedy strategy, where the agent takes random actions with a probability of ϵ and chooses the best-known action with a probability of 
1−ϵ.

As the agent learns, the value of ϵ is gradually decreased to reduce exploration in favor of exploitation.

Define the DQN Agent

Neural Network Construction (_build_model):

- Architecture: Constructs a neural network with two hidden layers, each having 24 neurons with ReLU activation, and an output layer with linear activation, where each output corresponds to an action's Q-value.

- Compilation: The network is compiled with mean squared error loss and the Adam optimizer.

Memory Management (remember):
- Experience Storage: Records experiences defined by the current state, action taken, reward received, next state, and whether the episode has ended (done). This data is essential for training the network via experience replay.

Action Selection (act):
- Exploration vs. Exploitation: Decides on an action based on the current state, using an ε-greedy policy — randomly choosing an action with a probability epsilon or choosing the best-known action based on the neural network's predictions.

Learning from Experience (replay):
- Batch Learning: Randomly samples a batch of experiences from memory to train the network, helping to break correlation between consecutive learning steps and stabilizing learning.
- Target Calculation: Updates the Q-values using the Bellman equation. If an episode is not done, it adjusts the Q-value target with the discounted maximum future reward.
- Network Training: Uses the experiences and target Q-values to train the network, fitting it to better approximate the Q-function.
- Epsilon Decay: Reduces epsilon after each batch to decrease the rate of random actions and increase reliance on the network's learned values.