import pygame
import pandas as pd
import numpy as np
import random as rd
import time
from tqdm import tqdm

# Define colors
WALL = (220, 118, 51)
WHITE = (255, 255, 255)
PLAYER = (142, 68, 173)
RED = (255, 0, 0)
GOAL = (46, 134, 193)

# Define constants
BLOCK_SIZE = 80
MARGIN = 20

# Define the maze
env = np.array([[1, 0, 0, 0],
                [0, -1, 0, -1],
                [0, 0, 0, -1],
                [-1, 0, 0, 2]])

class Env:
    def __init__(self):
        self.env = np.array([[0,0,0,0],
                            [0,-1,0,-1],
                            [0,0,0,-1],
                            [-1,0,0,2]])
        self.current_state = (0,0)
        self.shape = self.env.shape
        self.done = False
        self.reward = 0

    def terminate_state(self):
        row,col = self.current_state
        if self.env[row][col] == 2:
            self.done = True
            self.reward = 10
        elif self.env[row][col] == -1:
            self.done = True
            self.reward = -10
        else:
            self.done = False
            self.reward = 0
    def reset(self):
        self.env = np.array([[0,0,0,0],
                            [0,-1,0,-1],
                            [0,0,0,-1],
                            [-1,0,0,2]])
        self.current_state = (0,0)
        self.shape = self.env.shape
        self.done = False
        self.reward = 0
        

    def step(self,action):
        row,col = self.current_state
        if action == 2:
            if col+1 < self.shape[1]:
                self.current_state = (row,col+1)
        if action == 0:
            if col-1 >= 0:
                self.current_state = (row,col-1)
        if action == 1:
            if row-1 >= 0:
                self.current_state = (row-1,col)
        if action == 3:
            if row+1 < self.shape[0]:
                self.current_state = (row+1,col)

        self.terminate_state()
        return self.current_state , self.done , self.reward


    def render(self):
        row,col = self.env.shape
        env_rend = ''
        for i in range(row):
            for j in range(col):
                state = self.env[i][j]
                if self.current_state == (i,j):
                    env_rend += 'S'
                elif state == 0:
                    env_rend += 'F'
                elif state == -1:
                    env_rend += 'H'
                else:
                    env_rend += 'G'
            env_rend += '\n'
        print(env_rend)



# Initialize pygame
pygame.init()

# Set the screen dimensions
WINDOW_SIZE = [env.shape[1] * (BLOCK_SIZE + MARGIN), env.shape[0] * (BLOCK_SIZE + MARGIN)]
screen = pygame.display.set_mode(WINDOW_SIZE)

pygame.display.set_caption("Maze Game")
font = pygame.font.Font(pygame.font.get_default_font(), 36)


clock = pygame.time.Clock()

# Function to draw the maze
def draw_maze(env):
    for row in range(len(env)):
        for col in range(len(env[0])):
            color = WHITE
            if env[row][col] == -1:
                color = WALL
                wall_image = pygame.image.load("wall.png")
                x = (MARGIN + BLOCK_SIZE) * col + MARGIN
                y = (MARGIN + BLOCK_SIZE) * row + MARGIN
                screen.blit(wall_image, (x, y))
            elif env[row][col] == 1:
                color = PLAYER
                if (row,col) in holes:
                    player_image = pygame.image.load("cowboy_dead.png")
                    x = (MARGIN + BLOCK_SIZE) * col + MARGIN
                    y = (MARGIN + BLOCK_SIZE) * row + MARGIN
                    screen.blit(player_image, (x, y))
                else:
                    player_image = pygame.image.load("cowboy.png")
                    x = (MARGIN + BLOCK_SIZE) * col + MARGIN
                    y = (MARGIN + BLOCK_SIZE) * row + MARGIN
                    screen.blit(player_image, (x, y))
            elif env[row][col] == 2:
                color = GOAL
                goal_image = pygame.image.load("gift.png")
                x = (MARGIN + BLOCK_SIZE) * col + MARGIN
                y = (MARGIN + BLOCK_SIZE) * row + MARGIN
                screen.blit(goal_image, (x, y))

                # pygame.draw.rect(screen, color, [(MARGIN + BLOCK_SIZE) * col + MARGIN,
                #                                 (MARGIN + BLOCK_SIZE) * row + MARGIN,
                #                                 BLOCK_SIZE, BLOCK_SIZE])

            if env[row][col] == -1:
                color = WALL
                wall_image = pygame.image.load("wall.png")
                x = (MARGIN + BLOCK_SIZE) * col + MARGIN
                y = (MARGIN + BLOCK_SIZE) * row + MARGIN
                screen.blit(wall_image, (x, y))

            # text = font.render("5", True, color)
            # screen.blit(text, (10, 10))
                

# Define a variable to track if the player reached the goal
reached_goal = False

# Function to move the player
def move_player(dx, dy):
    global env, reached_goal
    for row in range(len(env)):
        for col in range(len(env[0])):
            if env[row][col] == 1:
                new_row = row + dy
                new_col = col + dx
                if 0 <= new_row < len(env) and 0 <= new_col < len(env[0]):
                    if env[new_row][new_col] == 2:  # Check if the blue box (goal) is reached
                        env[row][col] = 0
                        env[new_row][new_col] = 1
                        reached_goal = True
                        return True
                    env[row][col] = 0
                    env[new_row][new_col] = 1
                    return False
    return False





actions = {
    'left':0,
    'down':1,
    'right':2,
    'up':3
}

# Define the action map
action_map = {0: 'left',
              1: 'down',
              2: 'right',
              3: 'up'}

def getHoles(matrix):
    holes = []
    for i,row in enumerate(matrix):
        for j,col in enumerate(row):
            if matrix[i][j] == -1:
                holes.append((i,j))
    return holes

holes = getHoles(env)

def setRMatrix(matrix,win,loss):
    for state,action in win:
        matrix[state][action] = 10
    for state,action in loss:
        matrix[state][action] = -10
    return matrix

qmatrix = np.zeros((16,4))
rmatrix = np.zeros((16,4))

loss = [(1,3),(3,3),(4,2),(6,0),(6,2),(8,3),(9,1),(10,2),(13,0)]
win = [(14,2)]

rmatrix = setRMatrix(rmatrix,win,loss)
print(rmatrix)

def max_random(lst):
    ix = []
    for i,v in enumerate(lst):
        if v == max(lst):
            ix.append(i)
    return rd.choice(ix)

maze = Env()
state1 = 0
explore = 80
mtime = 30

# Load the background image
background_image = pygame.image.load("grass.png").convert()
discount_factor = 0.8

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not reached_goal:
        action = max_random(qmatrix[state1])

        obs,end,reward = maze.step(action)
        state2 = (obs[0]*4)+obs[1]
        qmatrix[state1][action] = rmatrix[state1][action] + discount_factor * max(qmatrix[state2][a] for a in range(4))
        state1 = state2
        # maze.render()
        # Move the player based on the random action
        if action_map[action] == 'left':
            move_player(-1, 0)
        elif action_map[action] == 'up':
            move_player(0, 1)
        elif action_map[action] == 'right':
            move_player(1, 0)
        elif action_map[action] == 'down':
            move_player(0, -1)

        if reward < 0:
            reached_goal = True

        if reward > 0:
            reached_goal = True
            mtime = 10
            clock.tick(mtime)  # Adjust the speed as needed
        
        print(qmatrix)


    # Fill the screen with the background image
    screen.blit(background_image, (0, 0))

    # screen.fill()
    draw_maze(env)
    if reached_goal:
        pygame.display.flip()
        time.sleep(1)  # Pause for 3 seconds
        reached_goal = False
        env = np.array([[1, 0, 0, 0],  # Reset maze to initial state
                        [0, -1, 0, -1],
                        [0, 0, 0, -1],
                        [-1, 0, 0, 2]])
        maze.reset()

    pygame.display.flip()
    clock.tick(mtime)  # Adjust the speed as needed

pygame.quit()