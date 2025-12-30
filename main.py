
from SNAKE_game import Stage
from SNAKE_Interpreter import SNAKEInterpreter
import os
import pygame as pg
from GameDraw import GameDraw
import torch
import tkinter as tk #for ui https://www.pythontutorial.net/tkinter
from config import CELL_SIZE, GRID_WIDTH, GRID_HEIGHT,STATE_SIZE,HIDDEN_SIZE,ACTION_SIZE,BATCH_SIZE
from random import randint
import numpy as np
from DQN_Agent import DQNAgent
import gymnasium as gym
import argparse
import time

class Ball:
    def __init__(self, canvas, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.canvas = canvas
        self.ball = canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill="red")

    def move_ball(self):
        deltax = randint(0,5)
        deltay = randint(0,5)
        self.canvas.move(self.ball, deltax, deltay)
        self.canvas.after(50, self.move_ball)

# resize gif to cell_size
def resizeImage(img, newWidth, newHeight):
    oldWidth = img.width()
    oldHeight = img.height()
    newPhotoImage = tk.PhotoImage(width=newWidth, height=newHeight)
    for x in range(newWidth):
        for y in range(newHeight):
            xOld = int(x*oldWidth/newWidth)
            yOld = int(y*oldHeight/newHeight)
            rgb = '#%02x%02x%02x' % img.get(xOld, yOld)
            newPhotoImage.put(rgb, (x, y))
    return newPhotoImage

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-se", "--sessions",
                        type=int, default=10,
                        help="Number of sessions to run.")
    parser.add_argument("-v", "--visual",
                        type=str, choices=("on", "off"), default="on",
                        help="Enable or disable game GUI. Default 'on'.")
    parser.add_argument("-l", "--load",
                        type=str, default=None,
                        help="Filename to load model.")
    parser.add_argument("-s", "--save",
                        type=str, default=None,
                        help="Filename to save model.")
    parser.add_argument("-t", "--train",
                        #action="train_true",
                        help="Enable training mode.")
    parser.add_argument("-step-by-step", 
                        #action="store_true",
                        help="Enable step-by-step mode.")
    return parser.parse_args()

def init_pygame():
    pg.init()
    return pg.display.set_mode((WIDTH, HEIGHT))

def main():
    # create path to save models
    try:
        ruta = './models'
        os.makedirs(ruta, exist_ok=True)
        print(f"Directorio listo: {os.path.abspath(ruta)}")
    except PermissionError:
        print(f"Error: No tienes permisos para crear el directorio en '{ruta}'.")
    except OSError as e:
        print(f"Error al crear el directorio '{ruta}': {e}")

    # parsing
    args = None  
    try:
        args = parse_arguments()
        print(args)
        # create pygame screen object
        screen = GameDraw('Learn2Slither', GRID_WIDTH*CELL_SIZE+10+80+CELL_SIZE, GRID_HEIGHT*CELL_SIZE+10+300 + CELL_SIZE+20)       
        # Create SNAKE Game
        game = Stage(GRID_WIDTH, GRID_HEIGHT)
        # create SNAKE interpreter object
        snakeInterpreter = SNAKEInterpreter(game)
        play = False   
        if play:
            # PLAY        
            # create Agent
            agent = DQNAgent(STATE_SIZE, HIDDEN_SIZE, ACTION_SIZE)
            agent.load('models/model_30_ep.weights.h5')
            
            running = True
            game.print()
            while running:
                # Get state
                state_interpreter = np.reshape(snakeInterpreter.get_state(), [1, STATE_SIZE])
                # Get an action from Agent
                action_interpreter, act_values, predict = agent.predict(state_interpreter)
                print(action_interpreter)
                reward_interpreter, game_over_interpreter, game_over_msg_interpreter = snakeInterpreter.get_reward(action_interpreter)
                screen.draw_game(game.grid, action_interpreter, 
                                game_over_interpreter, game_over_msg_interpreter, 
                                state_interpreter[0]) # window print
                if game_over_interpreter == False:
                    game.move(action_interpreter)
                    game.print()
                else:
                    print("GAME OVER")
                    running = False
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False
                pg.time.delay(5000)
            # The argument to the function may be any descriptive text
            input("Press the Enter key to continue: ")
            screen.quit()
            exit()
        else:
            # TRAINING AGENT
            agent = DQNAgent(STATE_SIZE, HIDDEN_SIZE, ACTION_SIZE)
            game_over = False
            batch_size = 32
            EPISODES = 30
            
            for e in range(EPISODES):
                state, grid, game_over, iter, reward, game_over_msg = game.reset()
                #print(state)
                #print(grid)
                
                #screen.draw_game(grid, 0, game_over, game_over_msg)
                
                game.print()
                #state = np.reshape(state, [1, state_size])
                state_interpreter = np.reshape(snakeInterpreter.get_state(), [1, STATE_SIZE])
                #print(e,state)
                for time in range(100):  # 500 timesteps per episode
                    #print("Actual State (game):", state)
                    print("Actual State (interpreter):", state_interpreter)
                    # get an action from agent
                    #action = agent.act(state_interpreter)
                    action_interpreter, act_values, predict = agent.act(state_interpreter)
                    char_actions = ['down', 'up', 'right', 'left']
                    #print(time," --> action from agent (game):", char_actions[action])
                    #print(time," --> action from agent (interpreter):", char_actions[action_interpreter], " values:", act_values, " Predict:", predict)
                    
                    
                    # check proposed action to get new state, rewards, game_over 
                    # get reward from interpreter
                    reward_interpreter, game_over_interpreter, game_over_msg_interpreter = snakeInterpreter.get_reward(action_interpreter)
                    
                    # if collision with wall and snake -> game_over -> don`t make the move???
                    # if len = 0 -> game_over -> don`t make move???
                    game.print()
                    if game_over_interpreter == False:
                        game.move(action_interpreter)
                    
                    #next_state, grid, game_over, iter, reward, game_over_msg = game.step(action)
                    #print(" Reward from Game;",reward, game_over, game_over_msg)
                    # check proposed action to get new state, rewards, game_over 
                    #print(" Reward from Interpreter;",snakeInterpreter.get_reward(action_interpreter))
                    # get reward from interpreter


                    next_state_interpreter = snakeInterpreter.get_state()

                    # show game
                    #game.print()   # console print             
                    #screen.draw_game(game.grid, action, game_over, game_over_msg, state_interpreter[0]) # window print
                    
                    #reward = reward if not game_over else -10
                    
                    #next_state = np.reshape(next_state, [1, state_size])
                    next_state_interpreter = np.reshape(next_state_interpreter, [1, STATE_SIZE])
                    #print("Next State (game):",next_state, " Reward:", reward)
                    #print("Next State (interpreter):", next_state_interpreter)
                    
                    # Save movement in Agent memory
                    agent.remember(state_interpreter, action_interpreter, reward_interpreter, next_state_interpreter, game_over_interpreter)
                    print("State:", state_interpreter, " Action:", action_interpreter, " Reward:", reward_interpreter ,"Next State:", next_state_interpreter, " Game Over:", game_over_interpreter)
                    #state = next_state
                    state_interpreter = next_state_interpreter
                    
                    if game_over_interpreter:
                        print("episode: {}/{}, timesteps: {}, msg: {}, reward: {}, e: {:.2}".format(e+1, EPISODES, time,  game_over_msg, reward_interpreter, agent.epsilon))
                        #screen.draw_game(grid, action, game_over, game_over_msg, state[0])
                        screen.draw_game(game.grid, action_interpreter, game_over_interpreter, game_over_msg_interpreter, state_interpreter[0])
                        pg.time.delay(600)
                        break

                    # When we have enough data in memory (> batch_size) fit the model
                    if len(agent.memory) > BATCH_SIZE:
                        agent.replay(BATCH_SIZE)
                    pg.time.delay(5000)
                
            agent.save('./models/model_'+str(EPISODES)+"_ep.weights.h5")
            
            running = True
            while running:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False   
            screen.quit()


    except AssertionError as e:
        print(f"{e.__class__.__name__}: {e}")
        exit(1)
    except Exception as e:
        print(f"{e.__class__.__name__}: {e}")
        exit(1)
    finally:
        if args is not None and args.visual == "on":
            exit()
    
    
    
    
    
    
    
    
    
    # create models path if not exits
    game = Stage(10)
    game.step(1)
    game.print()
    state_size = 24
    hidden_size = 128
    action_size = 4
    agent = DQNAgent(state_size, hidden_size, action_size)
    print (state_size, hidden_size, action_size)
    game_over = False
    batch_size = 32
    EPISODES = 1

    for e in range(EPISODES):
        state = game.reset()
        state = state[0]
        state = np.reshape(state, [1, state_size])
        print(e,state)
        for time in range(100):  # 500 timesteps per episode
            # get an action from agent
            action = agent.act(state)
            print(time,"action:", action)
            # play action 
            next_state, grid, game_over, iter, reward = game.step(action)
            reward = reward if not game_over else -10
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state, game_over)
            state = next_state
            if game_over:
                print("episode: {}/{}, timesteps: {}, e: {:.2}".format(e, EPISODES, time, agent.epsilon))
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
    agent.save('./models/model_'+str(EPISODES)+"_ep.weights.h5")
    print(agent.get_memory())
    exit()


    env = gym.make('CartPole-v1')
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)
    done = False
    batch_size = 32
    test_games = 1000
    test_moves = 500
    for game in range(test_games):
        state = env.reset()
        print("game:", game, "state:",state[0])
        #state = np.reshape(state, [1, state_size])
        exit()
        for move in range(test_moves):  # 500 timesteps per episode
            #print("game {}, episode: {}/{}".format(game, move, test_moves))
            
            # Predict an action by agent
            action = agent.act(state)
            print(action, state)
            print(env.step(action))
            
            # Get the result of the predicted action: next_state, reward and done
            #next_state, reward, done, _ = env.step(action)
            # reward = reward if not done else -10
            #next_state = np.reshape(next_state, [1, state_size])
            
            # Pass data of state, action, reward and next_state, and done to agent to remember
            #agent.remember(state, action, reward, next_state, done)
            
            #state = next_state
            #if done:
            #    print("episode: {}/{}, score: {}, e: {:.2}".format(e, EPISODES, time, agent.epsilon))
            #    break
            #if len(agent.memory) > batch_size:
            #    agent.replay(batch_size)
    exit()
    # STATE = 20, 
    # W 0 0 G R 0 0 0 H S 0 W W 0 0 0 0 0 0 0 0 0 H W
    # W = Wall
    # H = Snake Head
    # S = Snake body segment
    # G = Green apple
    # R = Red apple
    # 0 = Empty space
    # ACTIONS = 4
    # 0 - UP
    # 1 - LEFT
    # 2 - DOWN
    # 3 - RIGHT
    state_size = 20
    action_size = 4
    agent = DQNAgent(state_size, action_size)
    print (state_size, action_size)
    exit()
    game = Stage(10)
    print(game.reset())
    iter = 0
    while iter < 3:
        status, reward = game.step(1,2)
        grid, score, game_over, iteration =status
        print(grid, reward, "  iter:", iter)
        iter += 1

    exit()
    # initialize root Window and canvas
    root = tk.Tk()
    root.geometry("800x600")
    root.title('Login')
    # place a label on the root window
    message = tk.Label(root, text="Hello, World!")
    message.pack()
    canvas = tk.Canvas(root, width=600, height=400, bg='white')
    canvas.pack(anchor=tk.CENTER, expand=True)
    
    i = 0
    j = 0
    #print(len(grid[0]))
    #print(len(grid))
    greenAppleImage = tk.PhotoImage(file="green_apple.gif") 
    greenAppleImage = resizeImage(greenAppleImage, CELL_SIZE, CELL_SIZE) 
    redAppleImage = tk.PhotoImage(file="red_apple.gif") 
    redAppleImage = resizeImage(redAppleImage, CELL_SIZE, CELL_SIZE) 
    while i < len(grid[0]):
        j = 0
        while j < len(grid):
            color = 'red' if grid[j][i] == 1 else 'green'
            canvas.create_rectangle((10+i*CELL_SIZE, 10+j*CELL_SIZE), (10+(i+1)*CELL_SIZE, 10+(j+1)*CELL_SIZE), fill=color)
            if grid[j][i] > 1:
                canvas.create_image(10+i*CELL_SIZE, 10+j*CELL_SIZE,  anchor=tk.NW, image=redAppleImage if grid[j][i] == 2 else greenAppleImage)
            j +=1
        i +=1

    # create two ball objects and animate them
    ball1 = Ball(canvas, 10, 10, 30, 30)
    ball2 = Ball(canvas, 60, 60, 80, 80)
    ball1.move_ball()
    ball2.move_ball()

    root.mainloop()
    



if __name__ == "__main__":
    main()