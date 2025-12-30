import numpy as np
import random
import time
from collections import deque
from config import MOVE_PENALTY, GREEN_APPLE_REWARD, RED_APPLE_PENALTY, GAME_OVER_PENALTY, APPROACH_PENALTY, APPROACH_GREEN_APPLE_REWARD, MOVE_AWAY_GREEN_APPLE_PENALTY, APPROACH_RED_APPLE_PENALTY,GRID_WIDTH,GRID_HEIGHT 

class Stage:
    def __init__(self, width = 10, height = 10):
        self.state = [] # snake views
        self.width = width
        self.height = height
        self.red_apple = None
        self.green_apples = []
        self.snake = None
        self.grid = None
        self.iteration = 0
        self.reward = 0
        self.reset()
        #head = self.snake[0]
        #print(head[0], head[1])
        #self.print()
        print(self.state)

    def reset(self):
        """reset game """
        snake_head_x = np.random.randint(1, self.width - 2)
        snake_head_y = np.random.randint(1, self.height - 2)
        
        # generate snake body horizontal? in a queue
        self.snake = deque([(snake_head_x, snake_head_y)])
        for i in range(2):
            self.snake.append((snake_head_x, snake_head_y + i + 1))
        
        #generate new apples
        self.red_apple = self._generate_apple()
        self.green_apples = [self._generate_apple(), self._generate_apple()]
        self.score = 0
        self.game_over = False
        self.game_over_msg = ''
        self.iteration = 0
        self.reward = 0
        return self._get_state()

    def _update_grid(self):
        """Draw snake and apples in board 1 y 2  for snake, 3 for red apple and 4 for green"""
        self.grid = np.zeros((self.width, self.height))
        for pos in self.snake:
            self.grid[pos] = 2
        head = self.snake[0]
        self.grid[head[0], head[1]] = 1
        self.grid[self.red_apple] = 3
        for pos in self.green_apples:
            self.grid[pos] = 4

    def _update_state(self):
        self.state=[]
        #characters = ['O','H','S','R','G']
        characters = [0,1,2,3,4]
        head = self.snake[0]
        headX = head[0]
        headY= head[1]
        print(headX, headY)
        # Vertical seeing
        i = -1
        while i <= self.height:
            if (i < 0 or i >=  self.height):
                self.state.append(10)
            else: 
                self.state.append(characters[int(self.grid[headX][i])])
            i += 1
        # Horizontal seeing
        i = -1
        while i <= self.width:
            if (i < 0 or i >=  self.width):
                self.state.append(10)
            else: 
                self.state.append(characters[int(self.grid[i][headY])])
            i += 1

    def _get_state(self):
        """get current game state"""
        self._update_grid()
        self._update_state()
        return self.state,self.grid,self.game_over,self.iteration,self.reward,self.game_over_msg

    def _generate_apple(self):
        """generate a random position for an apple that is not in the snake, and not the same as the apples"""
        while True:
            pos = (random.randint(0, self.width-1), random.randint(0, self.height-1))
            # check if in snake
            if pos in self.snake:
                continue
            # check if in red apple position
            if self.red_apple and pos == self.red_apple:
                continue
            # check if in green apple position
            if self.green_apples and pos in self.green_apples:
                continue
            return pos

    def move(self, action):
        """move snake only if not game over by interpreter"""
        direction = [(0, 1),(0, -1),(1, 0),(-1, 0)] #down, up, right, left
        dx, dy = direction[action]
        #print( "move:", dx, dy)
        #1.- move snake head
        head = self.snake[0]
        new_head = (head[0] + dx, head[1] + dy)

        # Make the move
        self.snake.appendleft(new_head)
        # Get a reward or penalty for eating an apple
        if new_head in self.green_apples:
            # apple eat -> remove apple
            self.green_apples.remove(new_head)
            # create new apple green
            self.green_apples.append(self._generate_apple())
            # don´t make pop in snake 
        elif new_head == self.red_apple:
            # red apple eat & substract one segment from snake queue
            self.snake.pop()
            # create new red apple
            self.red_apple = self._generate_apple()
            # check if len of snake is zero-> game over -> check by interpreter
        else:
            # not eating -> just move
            self.snake.pop()
        # Update all
        self._get_state() 
        return self._get_state()


    def step(self, action):
        """step the game forward"""
        direction = [(0, 1),(0, -1),(1, 0),(-1, 0)] #down, up, right, left
        dx, dy = direction[action]
        #print( "move:", dx, dy)
        #1.- move snake head
        head = self.snake[0]
        new_head = (head[0] + dx, head[1] + dy)
        
        #2.- Check if gameover
        #Reset reward
        self.reward = 0 
        #Add to reward a penalty for a move. MOVE_PENALTY
        self.reward = MOVE_PENALTY

        #print(snake_vision)

        # Collision penalty with wall or snake body -> Add a game over penalty if so and return
        if new_head[0] < 0 or new_head[0] >= self.width or new_head[1] < 0 or new_head[1] >= self.height:
            self.reward += GAME_OVER_PENALTY
            self.game_over = True
            self.game_over_msg = 'Hit wall'
            return self._get_state()
        elif new_head in self.snake:
            self.reward += GAME_OVER_PENALTY
            self.game_over = True
            self.game_over_msg = 'Hit snake'
            return self._get_state()

        # Get a penalty for approaching snake body 
        for segment in list(self.snake)[1:]:
            if abs(new_head[0] - segment[0]) + abs(new_head[1] - segment[1]) == 1:
                self.reward += APPROACH_PENALTY

        #Get a reward or penalty for approaching green apple or red apple
        # Check if green apple in sight and add reward if approaching
        print("In reward",self.state)
        
        ejeY = self.state[:(GRID_HEIGHT+2)]
        ejeX = self.state[(GRID_HEIGHT+2):]
        #if "G" in self.state[:12]:
        if 4 in ejeY:
            print("hay una verde en el eje Y:")
            #index_H = self.state[:12].index('H')
            #index_G = [i for i,x in enumerate(self.state[:12]) if x=='G']
            #index_R = next((i for i, x in enumerate(self.state[:12]) if x == 'R'),9999)
            index_H = ejeY.index(1)
            index_G = [i for i,x in enumerate(ejeY) if x==4]
            index_R = next((i for i, x in enumerate(ejeY) if x == 3),9999)
            print("hay una verde en Y:", index_H, index_G, index_R)
            # best move and check if it is the choose
            nb_greens = len(index_G)
            # check dist 
            i = 0
            d_min = 1000
            mov = 0
            while i < nb_greens:
                if d_min > abs(index_H - index_G[i]):
                    d_min = abs(index_H - index_G[i])
                    mov = 1 if index_H - index_G[i] < 0 else -1
                i += 1
            print ("the best move in Y. nb_greens:", nb_greens," index green:", index_G, " best move in y:", mov, "distance:",d_min)
            print( head, "->", new_head)
            if new_head[1] == head[1] + mov:
                print("good move get reward:", APPROACH_GREEN_APPLE_REWARD * (10/d_min)/10)
                self.reward += APPROACH_GREEN_APPLE_REWARD * (10/d_min)/10 # more reward for nearest
            else:
                print("bad move get penalty:", MOVE_AWAY_GREEN_APPLE_PENALTY *(10/d_min)/10)
                self.reward += MOVE_AWAY_GREEN_APPLE_PENALTY * (10/d_min)/10 # more penalty for nearest
        
        #if "G" in self.state[12:24]:
        if 4 in ejeX:
            print("hay una verde en el eje X:",ejeX)
            #index_H = self.state[12:24].index('H')
            #index_G = [i for i,x in enumerate(self.state[12:24]) if x=='G']
            #index_R = next((i for i, x in enumerate(self.state[12:24]) if x == 'R'),9999)
            index_H =  ejeX.index(1)
            index_G = [i for i,x in enumerate(ejeX) if x==4]
            index_R = next((i for i, x in enumerate(ejeX) if x == 3),9999)
            print("hay una verde en X:", index_H, index_G, index_R)
            # check dist 
            nb_greens = len(index_G)
            i = 0
            d_min = 1000
            mov = 0
            while i < nb_greens:
                if d_min > abs(index_H - index_G[i]):
                    d_min = abs(index_H - index_G[i])
                    mov = 1 if index_H - index_G[i] < 0 else -1
                i += 1
            print ("the best move in X. nb_greens:", nb_greens," index green:", index_G, " best move in X:", mov, "distance:",d_min)
            print( head, "->", new_head)
            if new_head[0] == head[0] + mov:
                print("good move get reward:", APPROACH_GREEN_APPLE_REWARD *(10/d_min)/10)
                self.reward += APPROACH_GREEN_APPLE_REWARD *(10/d_min)/10 # more reward for nearest
            else:
                print("bad move get penalty:", MOVE_AWAY_GREEN_APPLE_PENALTY*(10/d_min)/10)
                self.reward += MOVE_AWAY_GREEN_APPLE_PENALTY *(10/d_min)/10 # more penalty for nearest
            # get dista
        
        
        
        if "R" in  ejeY:
            print("hay una roja en Y")
        if "R" in  ejeX:
            print("hay una roja en X")
        #for i, vision in enumerate(snake_vision):
        #    if "G" in vision:
        #        if i == 0 and new_head[1] == head[1] + 1:
        #            reward += APPROACH_GREEN_APPLE_REWARD
        #        elif i == 1 and new_head[1] == head[1] - 1:
        #            reward += APPROACH_GREEN_APPLE_REWARD
        #        elif i == 2 and new_head[0] == head[0] + 1:
        #            reward += APPROACH_GREEN_APPLE_REWARD
        #        elif i == 3 and new_head[0] == head[0] - 1:
        #            reward += APPROACH_GREEN_APPLE_REWARD
        #    elif "R" in vision:
        #        if i == 0 and new_head[1] == head[1] + 1:
        #            reward += APPROACH_RED_APPLE_PENALTY
        #        elif i == 1 and new_head[1] == head[1] - 1:
        #            reward += APPROACH_RED_APPLE_PENALTY
        #        elif i == 2 and new_head[0] == head[0] + 1:
        #            reward += APPROACH_RED_APPLE_PENALTY
        #        elif i == 3 and new_head[0] == head[0] - 1:
        #            reward += APPROACH_RED_APPLE_PENALTY

        # Make the move
        self.snake.appendleft(new_head)
        
        # Get a reward or penalty for eating an apple
        if new_head in self.green_apples:
            # green apple eat add reward
            self.reward += GREEN_APPLE_REWARD
            # apple eat -> remove apple
            self.green_apples.remove(new_head)
            # create new apple green
            self.green_apples.append(self._generate_apple())
            # don´t make pop in snake 
        elif new_head == self.red_apple:
            # red apple eat add penalty & substract one segment from snake queue
            self.reward += RED_APPLE_PENALTY
            self.snake.pop()
            # create new red apple
            self.red_apple = self._generate_apple()
            # check if len of snake is zero-> game over -> add penalty
            if len(self.snake) == 0:
                self.reward += GAME_OVER_PENALTY
                self.game_over = True
                return self._get_state()
        else:
            # not eating -> just move
            self.snake.pop()

        return self._get_state()

    def print(self):
        i = 0
        j = 0
        while i < self.height:
            j = 0
            while j < self.width:
                print(int(self.grid[j][i]),end="")
                j+=1
            print("")
            i += 1
        #print(self.grid)