import pygame as pg
from config import CELL_SIZE, GRID_WIDTH, GRID_HEIGHT, STATE_SIZE,HIDDEN_SIZE,ACTION_SIZE
# Game colors from : https://www.color-hex.com/color-palette/61235

class GameDraw:
    def __init__(self, title, width, height):
        pg.init()
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)
        self.screen.fill(pg.Color((44, 124, 51)))
        pg.display.flip()

    def draw_game(self, board, action, game_over, game_over_msg, state):
        self.screen.fill(pg.Color((9, 224, 151)))
        self.draw_grid(board)
        self.draw_state(state)
        self.draw_info(action, game_over, game_over_msg)
        self.draw_network()
        pg.display.flip()

    def draw_grid(self, board):
        for row in range(GRID_HEIGHT):
            for column in range(GRID_WIDTH):
                if (row + column) % 2:
                    color = pg.Color((10, 189, 198))
                else:
                    color = pg.Color((9, 179, 188))
                if board[column][row]==1:
                    color = pg.Color((165, 96, 8))
                if board[column][row]==2:
                    color = pg.Color((226, 159, 94))
                if board[column][row]==3:
                    color = pg.Color((195, 11, 78))
                if board[column][row]==4:
                    color = pg.Color((2, 235, 107))
                pg.draw.rect(self.screen, color, pg.Rect(
                    column * CELL_SIZE + 10,
                    row * CELL_SIZE + 10,
                    CELL_SIZE, CELL_SIZE))

    def draw_state(self, state):
        characters = ['O','H','S','R','G']
        color_text = pg.Color((0, 0, 0))
        font = pg.font.SysFont("arial", CELL_SIZE//2) # Default font with size 24
        cont = 1
        for row in range(GRID_HEIGHT):
            if (row) % 2:
                color = pg.Color((10, 189, 198))
            else:
                color = pg.Color((9, 179, 188))
            pg.draw.rect(self.screen, color, pg.Rect(
                    GRID_WIDTH * CELL_SIZE + 20,
                    row * CELL_SIZE + 10,
                    CELL_SIZE, CELL_SIZE))
            text_surface = font.render(characters[state[cont]], True, color_text)
            self.screen.blit(text_surface, (GRID_WIDTH * CELL_SIZE + 20 + CELL_SIZE//3, row * CELL_SIZE + 10+ CELL_SIZE//3)) 
            cont += 1
        cont = cont + 2 # pass 2 x 'W'
        for column in range(GRID_WIDTH):
            if (column) % 2:
                color = pg.Color((10, 189, 198))
            else:
                color = pg.Color((9, 179, 188))
            pg.draw.rect(self.screen, color, pg.Rect(
                    column * CELL_SIZE + 10,
                    GRID_HEIGHT * CELL_SIZE + 20,
                    CELL_SIZE, CELL_SIZE))
            text_surface = font.render(characters[state[cont]], True, color_text)
            self.screen.blit(text_surface, (column * CELL_SIZE + 10 + CELL_SIZE//3, GRID_HEIGHT * CELL_SIZE + 20 + CELL_SIZE//3)) 
            cont += 1


    def draw_info(self, action, game_over, game_over_msg):
        fonts = pg.font.get_fonts()
        #for f in fonts:
        #    print(f)
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        color = (0, 0, 0)
        x = GRID_WIDTH*CELL_SIZE+10+CELL_SIZE+6+10
        font = pg.font.SysFont("arial", 10) # Default font with size 24
        
        text_surface = font.render('Mode:', True, color)
        self.screen.blit(text_surface, (x, 10)) # Position at (200, 200) 
        text_surface = font.render('Training', True, color)
        self.screen.blit(text_surface, (x+30, 10)) # Position at (200, 200) 
        
        char_actions = ['down', 'up', 'right', 'left']
        status_text = char_actions[action]
        text_surface = font.render('Action:', True, color)
        self.screen.blit(text_surface, (x, 20)) # Position at (200, 200) 
        text_surface = font.render(status_text, True, color)
        self.screen.blit(text_surface, (x+35, 20)) # Position at (200, 200)            

        text_surface = font.render('Reward:', True, color)
        self.screen.blit(text_surface, (x, 30)) # Position at (200, 200) 
        text_surface = font.render("rewar..", True, color)
        self.screen.blit(text_surface, (x+35, 30)) # Position at (200, 200)  

        text_surface = font.render('Finish:', True, color)
        self.screen.blit(text_surface, (x, 40)) # Position at (200, 200) 
        text_surface = font.render(str(game_over), True, color)
        self.screen.blit(text_surface, (x+35, 40)) # Position at (200, 200)            

        text_surface = font.render('Cause:', True, color)
        self.screen.blit(text_surface, (x, 50)) # Position at (200, 200) 
        text_surface = font.render(game_over_msg, True, color)
        self.screen.blit(text_surface, (x+35, 50)) # Position at (200, 200)            
    
    def draw_network(self):
        x0 = 10
        y0 = GRID_HEIGHT*CELL_SIZE+20 + CELL_SIZE+20
        x1 = GRID_WIDTH*CELL_SIZE+70
        y1 = 280
        color_text = pg.Color((0, 0, 0))
        color_bg_light = pg.Color((10, 189, 198))
        color_bg_dark = pg.Color((9, 179, 188))
        # draw background
        pg.draw.rect(self.screen, color_bg_light, pg.Rect(x0,y0,x1,y1))
        # draw input neurons
        for i in range(GRID_WIDTH+GRID_HEIGHT+4):
            x_coord = x0+75
            y_coord = y0 + (i+1) * y1/(GRID_WIDTH+GRID_HEIGHT+4+1)
            font = pg.font.SysFont("arial", 7) # Default font with size 24
            text_surface = font.render(str(i), True, color_text)
            self.screen.blit(text_surface, (x_coord-20, y_coord)) 
            pg.draw.circle(self.screen, pg.Color((0, 0, 0)), (x_coord,y_coord), 3)
            pg.draw.line(self.screen, pg.Color((0, 0, 0)), (x_coord, y_coord),  (x_coord+50, y_coord), 1)
        # draw exit neurons
        for i in range(4):
            x_coord = x1-75
            y_coord = y0 + (i+1) * y1/(4+1)
            font = pg.font.SysFont("arial", 15) # Default font with size 24
            text_surface = font.render(str(i), True, color_text)
            self.screen.blit(text_surface, (x_coord+20, y_coord)) 
            pg.draw.circle(self.screen, pg.Color((0, 0, 0)), (x_coord, y_coord), 5)
            pg.draw.line(self.screen, pg.Color((0, 0, 0)), (x_coord, y_coord),  (x_coord-50, y_coord), 1)
        # draw layer
        pg.draw.rect(self.screen, color_bg_dark, pg.Rect(x0+x1/2+10,y0+5,100,y1-10))
        pg.draw.rect(self.screen, color_bg_dark, pg.Rect(x0+x1/2-110,y0+5,100,y1-10))
        font = pg.font.SysFont("arial", 15) # Default font with size 24
        text_surface = font.render(str(HIDDEN_SIZE), True, color_text)
        self.screen.blit(text_surface, (x0+x1/2-110+100/2, (y0+5)+(y1-10)/2)) 
        text_surface = font.render('NEURONS', True, color_text)
        self.screen.blit(text_surface, (x0+x1/2-110+100/2-25, (y0+25)+(y1-10)/2)) 
        text_surface = font.render(str(HIDDEN_SIZE//2), True, color_text)
        self.screen.blit(text_surface, (x0+x1/2+5+100/2, (y0+5)+(y1-10)/2)) 
        text_surface = font.render('NEURONS', True, color_text)
        self.screen.blit(text_surface, (x0+x1/2+5+100/2-25, (y0+25)+(y1-10)/2)) 

    def quit(self):
        pg.quit()