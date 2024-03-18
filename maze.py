import pygame
import pandas as pd
import numpy as np
import random as rd
import time
from tqdm import tqdm

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOAL = (0, 0, 255)

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
                color = BLACK
            elif env[row][col] == 1:
                color = GREEN
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

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not reached_goal:
        # Randomly select a direction
        random_action = rd.choice(list(actions.keys()))

        # Move the player based on the random action
        if random_action == 'left':
            move_player(-1, 0)
        elif random_action == 'down':
            move_player(0, 1)
        elif random_action == 'right':
            move_player(1, 0)
        elif random_action == 'up':
            move_player(0, -1)

    screen.fill(WHITE)
    draw_maze(env)

    if reached_goal:
        pygame.draw.rect(screen, RED, [(MARGIN + BLOCK_SIZE) * 3 + MARGIN,
                                       (MARGIN + BLOCK_SIZE) * 3 + MARGIN,
                                       BLOCK_SIZE, BLOCK_SIZE])
        pygame.display.flip()
        time.sleep(1)  # Pause for 3 seconds
        reached_goal = False
        env = np.array([[1, 0, 0, 0],  # Reset maze to initial state
                        [0, -1, 0, -1],
                        [0, 0, 0, -1],
                        [-1, 0, 0, 2]])

    pygame.display.flip()
    clock.tick(10)  # Adjust the speed as needed

pygame.quit()