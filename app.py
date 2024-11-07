import numpy as np
import pygame
import random
import time

# Constants
ROWS = 25
COLS = 25
WINDOW_SIZE = 800
CELL_SIZE = WINDOW_SIZE // max(ROWS, COLS)  # Determine cell size based on the window size

# Colors
WHITE = (255, 255, 255)
BROWN = (92, 64, 51)
LIGHT_PINK = (255, 182, 193)
LIGHT_GREEN = (144, 238, 144)
BLUE = (190, 190, 255)

# Pygame Initialization
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("A* Algorithm")

# Path
path = []

# Spot class
class Spot:
    def __init__(self, i: int, j: int) -> None:
        self.i = i
        self.j = j
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbours = []
        self.previous: Spot = None
        self.wall = True if random.uniform(0, 1) < 0.2 else False
        self.agent = False

    def draw(self) -> None:
        # Drawing each spot as a rectangle
        rect = pygame.Rect(self.i * CELL_SIZE, self.j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface=screen, color=self.color, rect=rect)

    def __str__(self) -> str:
        return f'({self.f},{self.g},{self.h})'
    
    @property
    def color(self) -> None:
        if self.wall:
            return BROWN
        elif self.agent:
            return (255, 165, 0)
        elif self in path:
            return BLUE  # Blue
        else:
            return WHITE  # White


# Grid class to manage spots
class Grid:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.spots = np.full((self.rows, self.cols), Spot, dtype=object)
        self.populate()

    def populate(self) -> None:
        # Fill grid with Spot objects
        for i in range(self.rows):
            for j in range(self.cols):
                self.spots[i][j] = Spot(i, j)

    def compute_and_add_spot_neighbours(self) -> None:
        for i in range(ROWS):
            for j in range(COLS):
                spot = self.spots[i][j]
                if i > 0:  # adding a left neighbour
                    spot.neighbours.append(self.spots[i-1][j])
                if i < COLS - 1:  # adding a right neighbour
                    spot.neighbours.append(self.spots[i+1][j])
                if j > 0:  # adding top neighbour
                    spot.neighbours.append(self.spots[i][j-1])
                if j < ROWS - 1:  # adding bottom neighbour
                    spot.neighbours.append(self.spots[i][j+1])

    def show(self) -> None:
        # Draw each Spot in the grid
        for i in range(self.rows):
            for j in range(self.cols):
                self.spots[i][j].draw()

    def clear(self) -> None:
        for i in range(self.rows):
            for j in range(self.cols):
                spot = self.spots[i][j]
                spot.f = spot.g = spot.h = 0
                spot.previous = None


    @staticmethod
    def heuristic(spot1: Spot, spot2: Spot) -> int:
        return abs(spot1.i - spot2.i) + abs(spot1.j - spot2.j)


class Agent:
    def __init__(self, grid):
        self.i = 0
        self.j = 0
        self.grid = grid
        self.start: Spot = None
        self.destination: Spot = None
        self.path: list = []
        self.open_set = []
        self.closed_set = []

    def get_path(self, start: Spot, destination: Spot):

        print('Get path was called..')

        self.path = []
        self.i = start.i
        self.j = start.j

        self.start = start
        self.destination = destination

        self.open_set = [self.start]
        self.closed_set = []

        self.start.g = 0
        self.start.h = self.grid.heuristic(self.start, self.destination)
        self.start.f = self.start.g + self.start.h

        while self.open_set:
            # Find the spot in open_set with the lowest f value
            current = self.open_set[0]
            for spot in self.open_set:
                if spot.f < current.f:
                    current = spot

            self.open_set.remove(current)

            if current == self.destination:
                # Reconstruct the path by tracing back through previous spots
                self.path = []
                while current:
                    self.path.append(current)
                    current = current.previous
                self.path.reverse()
                return self.path

            self.closed_set.append(current)

            for neighbor in current.neighbours:
                if neighbor not in self.closed_set and not neighbor.wall and not neighbor.agent:
                    temp_g = current.g + 1

                    if neighbor not in self.open_set or temp_g < neighbor.g:
                        neighbor.previous = current
                        neighbor.g = temp_g
                        neighbor.h = self.grid.heuristic(neighbor, self.destination)
                        neighbor.f = neighbor.g + neighbor.h
                        if neighbor not in self.open_set:
                            self.open_set.append(neighbor)

        print("No Path was found... ")
        return []  # Return an empty path if no path is found
    
    def move_one_step(self, step: Spot):
        self.grid.spots[self.i][self.j].agent = False
        self.i = step.i
        self.j = step.j
        self.grid.spots[self.i][self.j].agent = True


'''---------SETUP------------'''
grid: Grid = Grid(rows=ROWS, cols=COLS)  # Initialize the grid once
grid.populate()
grid.compute_and_add_spot_neighbours()

agent1: Agent = Agent(grid)
start1 = grid.spots[random.randint(0, ROWS - 1)][random.randint(0, COLS -1)]
start1.wall = False
end1 = grid.spots[random.randint(0, ROWS - 1)][random.randint(0, COLS - 1)]
end1.wall = False

agent2: Agent = Agent(grid)
start2 = grid.spots[random.randint(0, ROWS - 1)][random.randint(0, COLS - 1)]
start2.wall = False
end2 = grid.spots[random.randint(0, ROWS - 1)][random.randint(0, COLS - 1)]
end2.wall = False


agent3: Agent = Agent(grid)
start3 = grid.spots[random.randint(0, ROWS - 1)][random.randint(0, COLS - 1)]
start3.wall = False
end3 = grid.spots[random.randint(0, ROWS - 1)][random.randint(0, COLS - 1)]
end3.wall = False


agent4: Agent = Agent(grid)
start4 = grid.spots[random.randint(0, ROWS - 1)][random.randint(0, COLS - 1)]
start4.wall = False
end4 = grid.spots[random.randint(0, ROWS - 1)][random.randint(0, COLS - 1)]
end4.wall = False

'''-----------END-------------'''

# Main loop
running = True
turn = 1  # Keep track of whose turn it is
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Check for the quit event
            running = False



    match turn % 4:
        case 1:  # Agent 1's turn
            path = agent1.get_path(start1, end1)
            grid.clear()  # Clear after the path is computed
            if len(agent1.path) > 1:
                start1 = path.pop(0)
                start1 = path.pop(0)
                agent1.move_one_step(start1)  # Move agent 1
                print('Agent 1 moved.')
        case 2:
            path = agent2.get_path(start2, end2)
            grid.clear()  # Clear after the path is computed
            if len(agent2.path) > 1:
                start2 = path.pop(0)
                start2 = path.pop(0)
                agent2.move_one_step(start2)  # Move agent 2
                print('Agent 2 moved.')
        case 3:
            path = agent3.get_path(start3, end3)
            grid.clear()  # Clear after the path is computed
            if len(agent3.path) > 1:
                start3 = path.pop(0)
                start3 = path.pop(0)
                agent3.move_one_step(start3)  # Move agent 2
                print('Agent 3 moved.')     
        case _:
            path = agent4.get_path(start4, end4)
            grid.clear()  # Clear after the path is computed
            if len(agent4.path) > 1:
                start4 = path.pop(0)
                start4 = path.pop(0)
                agent4.move_one_step(start4)  # Move agent 2
                print('Agent 4 moved.')                  

    grid.show()
    pygame.display.update()
    time.sleep(0.1)

    turn += 1  # Switch turns

# Quit Pygame
pygame.quit()
