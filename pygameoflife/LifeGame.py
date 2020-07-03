import sys, pygame
import random
import numpy as np
random.seed = 42


class Lifegame ():
    
    def __init__(self, screen_width = 800, screen_height=600, cell_size = 10, alive_color = (255,0,0), fps = 30):
        """init Lifegame Class

        Args:
            screen_width (int, optional):  Defaults to 800.
            screen_height (int, optional):  Defaults to 600.
            cell_size (int, optional): Circle diameter. Defaults to 10.
            alive_color (tuple, optional): Color of alive cells. Defaults to (255,0,0).
            fps (int, optional): frames per seconds. Defaults to 30.
        """
        self.game_over = False
        self.FPS = fps
        self.BOARDER_SIZE  =  self.WIDTH, self.HEIGHT = screen_width, screen_width
        self.CELL_SIZE = cell_size
        self.DEAD_COLOR = 0, 0, 0
        self.ALIVE_COLOR = alive_color
        self.COLORS = {0 : self.DEAD_COLOR, 1: self.ALIVE_COLOR}
        pygame.init()
        self.screen = pygame.display.set_mode(self.BOARDER_SIZE)
        self.init_grids()
        self.clear_screen()
        self.clock = pygame.time.Clock()
        self.paused = False
        pygame.display.flip()

    def init_grids(self):
        """initilize the defalut grid to inactive cells
        """
        self.num_cols = self.WIDTH // self.CELL_SIZE
        self.num_rows = self.HEIGHT // self.CELL_SIZE
        print (f'Columns: {self.num_cols}, Rows: {self.num_rows}')
        self.grids =  ([[0 for x in range(self.num_cols)] for y in range (self.num_rows)],
                        [[0 for x in range(self.num_cols)] for y in range (self.num_rows)])
        self.active_grid = 0
        self.game_grid_inactive = []
        self.set_grid()

    
    def set_grid (self,value = None):
        """
        set an entire grid at once, wither single value or random 0/1
        example : 
        set_grid(0) - All dead
        set_grid(1) - All alive
        set_grid() - all random

        Args:
            value ([int], optional): [set the value of the grid]. Defaults to None.
        """        
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                if value == None :
                    cell_value = random.choice([0,1])
                else :
                    cell_value = value
                self.grids[self.active_grid][row][col] = cell_value
    def clear_screen (self):
        """Clear current screen
        """
        self.screen.fill(self.DEAD_COLOR) 
    
    def check_cell_neighbors (self,row,col,grid):
        """Check the status of nearby cells.

        Args:
            row ([int]): [index of current row]
            col ([int]): [index of current col]
            grid ([list]): [current active grid]

        Returns:
            [int]: [number of alive nighbors]
        """
        x_min = max (0,col-1)
        x_max = min (self.num_cols-1,col+1)
        y_min = max (0,row-1)
        y_max = min (self.num_rows-1,row+1)
        return (np.sum([grid[a][x_min:x_max+1] for a in range (y_min,y_max+1)]) - grid[row][col])
        
    def update_generation(self):
        '''
        Inspect the current active generation
        Update the inactive grid to store the next gen
        swap out the active grid
        '''
        #  Inspect the current active generation, prepare the next generation
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                nighbors = self.check_cell_neighbors (row,col,self.grids[self.active_grid])
                status = 0 if nighbors < 2 or nighbors >3 else 1
                if self.grids[self.active_grid][row][col]==0 and nighbors == 2: status = 0
                self.grids[self.inactive_grid()][row][col] = status
        self.active_grid= self.inactive_grid()
        
    def inactive_grid(self):
        """inactive current grid

        Returns:
            [int]: [index of the current inactive grid (0,1)]
        """
        return (self.active_grid+1) %2

    def draw_grid(self):
        """Draw the grid by grids status
        """
        for c in range (self.num_cols):
            for r in range (self.num_rows):       
                pygame.draw.circle(self.screen, 
                                    self.COLORS[self.grids[self.active_grid][r][c]], 
                                    (c* self.CELL_SIZE + self.CELL_SIZE//2, r * self.CELL_SIZE + self.CELL_SIZE//2), 
                                    self.CELL_SIZE//2, 
                                    0)
        pygame.display.flip()


    def handle_events(self):
        """handle games events
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode == 'p':
                    if self.paused:
                        self.paused=False
                    else:
                        self.paused=True
                        
                elif event.unicode =='r':
                    self.set_grid()
                elif  event.unicode =='q':
                    self.game_over = True
                    
            #if event is keypressed of "p" then toggle game pause
            #if event is keypressed of "r" then randomize grid
            #if event is keypressed of "q" then quit

            if event.type == pygame.QUIT: 
                self.game_over = True
                # sys.exit()

        self.screen.fill(self.DEAD_COLOR)
            # screen.blit(ball, ballrect)
            
    def run(self):
        """Run the game
        """

        while True:
            if self.game_over: return
            self.clock.tick(self.FPS)
            self.handle_events()
            if self.paused : continue
            self.draw_grid()
            self.update_generation()
            # print (self.grids[self.active_grid][0][:30])



if __name__=="__main__":
    game = Lifegame()
    game.run()

