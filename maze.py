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
BLOCK_SIZE = 60
MARGIN = 10

# Define the maze
env = np.array([[1, 0, 0, 0],
                [0, -1, 0, -1],
                [0, 0, 0, -1],
                [-1, 0, 0, 2]])

# Initialize pygame
pygame.init()

# Set the screen dimensions
WINDOW_SIZE = [env.shape[1] * (BLOCK_SIZE + MARGIN), env.shape[0] * (BLOCK_SIZE + MARGIN)]
screen = pygame.display.set_mode(WINDOW_SIZE)

pygame.display.set_caption("Maze Game")

clock = pygame.time.Clock()

# Function to draw the maze
def draw_maze(env):
    for row in range(len(env)):
        for col in range(len(env[0])):
            color = WHITE
            if env[row][col] == -1:
                color = WALL
            elif env[row][col] == 1:
                color = PLAYER
            elif env[row][col] == 2:
                color = GOAL
            pygame.draw.rect(screen, color, [(MARGIN + BLOCK_SIZE) * col + MARGIN,
                                             (MARGIN + BLOCK_SIZE) * row + MARGIN,
                                             BLOCK_SIZE, BLOCK_SIZE])

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
                if 0 <= new_row < len(env) and 0 <= new_col < len(env[0]) and env[new_row][new_col] != -1:
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


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not reached_goal:
        action = rd.choice([0,1,2,3])        
        # Move the player based on the random action
        if action_map[action] == 'left':
            move_player(-1, 0)
        elif action_map[action] == 'down':
            move_player(0, 1)
        elif action_map[action] == 'right':
            move_player(1, 0)
        elif action_map[action] == 'up':
            move_player(0, -1)



    screen.fill(WHITE)
    draw_maze(env)
    if reached_goal:
        pygame.display.flip()
        time.sleep(1)  # Pause for 3 seconds
        reached_goal = False
        env = np.array([[1, 0, 0, 0],  # Reset maze to initial state
                        [0, -1, 0, -1],
                        [0, 0, 0, -1],
                        [-1, 0, 0, 2]])

    pygame.display.flip()
    clock.tick(60)  # Adjust the speed as needed

pygame.quit()