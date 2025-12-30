from config import MOVE_PENALTY, GREEN_APPLE_REWARD, RED_APPLE_PENALTY, GAME_OVER_PENALTY, APPROACH_PENALTY, APPROACH_GREEN_APPLE_REWARD, MOVE_AWAY_GREEN_APPLE_PENALTY, APPROACH_RED_APPLE_PENALTY,MOVE_AWAY_RED_APPLE_REWARD, GRID_WIDTH,GRID_HEIGHT 

class SNAKEInterpreter:
    """Interpreter of state and reward of SNAKE game.
    
    Args:

        `state_size`.Size of input state vector

        `hidden_size` .Size of hidden layers

        `action_size` .Number of possible actions
    """
    def __init__(self, game):
        self.state = []
        self.game = game
    
    def get_state(self):
        self.state=[]
        #characters = ['O','H','S','R','G']
        characters = [0,1,2,3,4]
        head = self.game.snake[0]
        headX = head[0]
        headY= head[1]
        width = len(self.game.grid)
        height = len(self.game.grid[0])
        # Vertical seeing
        i = -1
        while i <= height:
            if (i < 0 or i >=  height):
                self.state.append(10)
            else: 
                self.state.append(characters[int(self.game.grid[headX][i])])
            i += 1
        # Horizontal seeing
        i = -1
        while i <= width:
            if (i < 0 or i >=  width):
                self.state.append(10)
            else: 
                self.state.append(characters[int(self.game.grid[i][headY])])
            i += 1
        # return state of game
        return self.state
    
    def get_reward(self, action):
        """step the game forward"""
        direction = [(0, 1),(0, -1),(1, 0),(-1, 0)] #down, up, right, left
        dx, dy = direction[action]
        #print( "move:", dx, dy)

        #1.- move snake head
        head = self.game.snake[0]
        new_head = (head[0] + dx, head[1] + dy)
        
        #2.- Check if gameover
        #Reset reward
        reward = 0 
        #Add to reward a penalty for just do a move. MOVE_PENALTY
        reward = MOVE_PENALTY
        game_over = False
        game_over_msg = ''

        # Collision penalty with wall or snake body -> Add a game over penalty if so and return
        if new_head[0] < 0 or new_head[0] >= self.game.width or new_head[1] < 0 or new_head[1] >= self.game.height:
            reward += GAME_OVER_PENALTY
            game_over = True
            game_over_msg = 'Hit wall'
            return reward, game_over, game_over_msg
        elif new_head in self.game.snake:
            reward += GAME_OVER_PENALTY
            game_over = True
            game_over_msg = 'Hit snake'
            return reward, game_over, game_over_msg

        # Get a penalty for approaching snake body 
        for segment in list(self.game.snake)[1:]:
            if abs(new_head[0] - segment[0]) + abs(new_head[1] - segment[1]) == 1:
                reward += APPROACH_PENALTY

        # Get a reward or penalty for approaching green apple or red apple
        ejeY = self.get_state()[:(GRID_HEIGHT+2)]
        ejeX = self.get_state()[(GRID_HEIGHT+2):]

        # Check if GREEN apple in vertical sight ad reward if approching
        if 4 in ejeY:
            print("hay una verde en el eje Y:")
            index_H = ejeY.index(1)   # Position of head
            index_G = [i for i,x in enumerate(ejeY) if x==4] # Positons of green apple
            nb_greens = len(index_G)
            # check nearest green apple
            i = 0
            d_min = 1000
            mov = 0             # store best posible move
            while i < nb_greens:
                if d_min > abs(index_H - index_G[i]):
                    d_min = abs(index_H - index_G[i])
                    mov = 1 if index_H - index_G[i] < 0 else -1
                i += 1
            # Compare best move with proposed move and give reward or penalty
            if new_head[1] == head[1] + mov:
                #print("good move get reward:", APPROACH_GREEN_APPLE_REWARD * (10/d_min)/10)
                reward += APPROACH_GREEN_APPLE_REWARD #* (10/d_min)/10 # more reward for nearest
            else:
                #print("bad move get penalty:", MOVE_AWAY_GREEN_APPLE_PENALTY *(10/d_min)/10)
                reward += MOVE_AWAY_GREEN_APPLE_PENALTY #* (10/d_min)/10 # more penalty for nearest
        # Check if GREEN apple in horizonal sight ad reward if approching
        if 4 in ejeX:
            print("hay una verde en el eje Y:")
            index_H = ejeX.index(1)   # Position of head
            index_G = [i for i,x in enumerate(ejeX) if x==4] # Positons of green apple
            nb_greens = len(index_G)
            i = 0
            d_min = 1000
            mov = 0
            while i < nb_greens:
                if d_min > abs(index_H - index_G[i]):
                    d_min = abs(index_H - index_G[i])
                    mov = 1 if index_H - index_G[i] < 0 else -1
                i += 1
            #print ("the best move in X. nb_greens:", nb_greens," index green:", index_G, " best move in X:", mov, "distance:",d_min)
            #print( head, "->", new_head)
            if new_head[0] == head[0] + mov:
                #print("good move get reward:", APPROACH_GREEN_APPLE_REWARD *(10/d_min)/10)
                reward += APPROACH_GREEN_APPLE_REWARD #*(10/d_min)/10 # more reward for nearest
            else:
                #print("bad move get penalty:", MOVE_AWAY_GREEN_APPLE_PENALTY*(10/d_min)/10)
                reward += MOVE_AWAY_GREEN_APPLE_PENALTY #*(10/d_min)/10 # more penalty for nearest           
        
        # Check if RED apple in vertical sight add penalty if approaching
        if 3 in ejeY:
            print("hay una RED en el eje y:",ejeY)
            index_H =  ejeY.index(1)
            index_R = ejeY.index(3)
            d_min = 1000
            mov = 0
            if d_min > abs(index_H - index_R):
                d_min = abs(index_H - index_R)
                mov = 1 if index_H - index_R < 0 else -1
            if new_head[1] == head[1] + mov:
                # print("BAD move get get penalty:", APPROACH_RED_APPLE_REWARD * (10/d_min)/10)
                reward += APPROACH_RED_APPLE_PENALTY #* (10/d_min)/10 # more reward for nearest
            else:
                #print("GOOD move get reward:", MOVE_AWAY_RED_APPLE_REWARD #*(10/d_min)/10)
                reward += MOVE_AWAY_RED_APPLE_REWARD # * (10/d_min)/10 # more penalty for nearest
        # Check if RED apple in horizontal sight add penalty if approaching
        if 3 in ejeX:
            print("hay una RED en el eje x:",ejeX)
            index_H =  ejeX.index(1)
            index_R = ejeX.index(3)
            d_min = 1000
            mov = 0
            if d_min > abs(index_H - index_R):
                d_min = abs(index_H - index_R)
                mov = 1 if index_H - index_R < 0 else -1
            if new_head[0] == head[0] + mov:
                # print("BAD move get get penalty:", APPROACH_RED_APPLE_REWARD * (10/d_min)/10)
                reward += APPROACH_RED_APPLE_PENALTY #* (10/d_min)/10 # more reward for nearest
            else:
                #print("GOOD move get reward:", MOVE_AWAY_RED_APPLE_REWARD #*(10/d_min)/10)
                reward += MOVE_AWAY_RED_APPLE_REWARD # * (10/d_min)/10 # more penalty for nearest

        # Get a reward or penalty for eating an apple
        if new_head in self.game.green_apples:
            # green apple eat add reward
            reward += GREEN_APPLE_REWARD
        elif new_head == self.game.red_apple:
            # red apple eat add penalty 
            reward += RED_APPLE_PENALTY
            # check if len of snake is zero-> game over -> add penalty
            if (len(self.game.snake)-1) == 0:
                reward += GAME_OVER_PENALTY
                game_over = True
                game_over_msg = 'Snake dissapear'
                return reward, game_over, game_over_msg 
        
        return reward, game_over, game_over_msg 