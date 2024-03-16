import pygame
import pandas as pd
import numpy as np
import random as rd
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

# Function to move the player
def move_player(dx, dy):
    for row in range(len(env)):
        for col in range(len(env[0])):
            if env[row][col] == 1:
                new_row = row + dy
                new_col = col + dx
                if 0 <= new_row < len(env) and 0 <= new_col < len(env[0]) and env[new_row][new_col] != -1:
                    env[row][col] = 0
                    env[new_row][new_col] = 1
                    if env[new_row][new_col] == -1:
                        return True  # Player reached black box
                return False

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if move_player(0, -1):
                    running = False
            elif event.key == pygame.K_DOWN:
                if move_player(0, 1):
                    running = False
            elif event.key == pygame.K_LEFT:
                if move_player(-1, 0):
                    running = False
            elif event.key == pygame.K_RIGHT:
                if move_player(1, 0):
                    running = False

    screen.fill(WHITE)
    draw_maze(env)
    
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
