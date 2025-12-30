import numpy as np
import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

class DQNAgent:
    """Neural network for Q-learning.
    
    Args:

        `state_size`.Size of input state vector

        `hidden_size` .Size of hidden layers

        `action_size` .Number of possible actions
    """
    def __init__(self, state_size, hidden_size, action_size):
        self.state_size = state_size
        self.hidden_size = hidden_size
        self.action_size = action_size
        self.memory = []
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(self.hidden_size , input_dim=self.state_size, activation='relu'))
        model.add(Dense(self.hidden_size//2 , activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))  # Updated here
        return model


    def remember(self, state, action, reward, next_state, game_over):
        """ Store state-action-reward-next_state-game-over in memory"""
        self.memory.append((state, action, reward, next_state, game_over))

    def predict(self, state):
        """Select action using epsilon-greedy policy.
        
        Args:
            `state` .Current state vector

        Returns:
            `int` .Selected action (0-3)
        """
        act_values = self.model.predict(state)
        predict = True
        return np.argmax(act_values[0]), act_values, predict
    
    def act(self, state):
        """Select action using epsilon-greedy policy.
        
        Args:
            `state` .Current state vector

        Returns:
            `int` .Selected action (0-3)
        """
        act_values = []
        predict = False
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size), act_values, predict
        act_values = self.model.predict(state)
        predict = True
        return np.argmax(act_values[0]), act_values, predict

    def replay(self, batch_size):
        """Update network weights using experience replay."""
        # Take a number of examples (batch_size) from memory 
        minibatch = random.sample(self.memory, batch_size)
        #print(minibatch)
        #return
        for state, action, reward, next_state, game_over in minibatch:
            # take reward has dependent variable and state as independent
            target = reward
            #print("REPLAY:",target)
            #return
            if not game_over:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            
            # train model 
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        """Load pretrained model weights.
        Args:
            `path`: Path to model file
        """
        self.model.load_weights(name)

    def save(self, name):
        """Save current model weights.

        Args:
            `path`: Path to save model file
        """
        self.model.save_weights(name)
    
    def get_memory(self):
        return self.memory