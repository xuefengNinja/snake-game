#!/usr/bin/env python3
"""
Snake Game
A simple implementation of the classic Snake game using Pygame.
"""

import pygame
import sys
import random
import time
from collections import namedtuple

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors using namedtuple
Color = namedtuple('Color', ['r', 'g', 'b'])
BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)
GREEN = Color(0, 255, 0)
RED = Color(255, 0, 0)
BLUE = Color(0, 0, 255)

# Rainbow colors
RAINBOW_COLORS = [
    Color(255, 0, 0),      # Red
    Color(255, 127, 0),    # Orange
    Color(255, 255, 0),    # Yellow
    Color(0, 255, 0),      # Green
    Color(0, 0, 255),      # Blue
    Color(75, 0, 130),     # Indigo
    Color(148, 0, 211)     # Violet
]

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.grow = False
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        # Update direction
        self.direction = self.next_direction
        
        # Get current head position
        head = self.get_head_position()
        
        # Calculate new head position
        new_x = (head[0] + self.direction[0]) % GRID_WIDTH
        new_y = (head[1] + self.direction[1]) % GRID_HEIGHT
        new_head = (new_x, new_y)
        
        # Check for collision with self
        if new_head in self.positions[1:]:
            return True  # Game over
        
        # Add new head
        self.positions.insert(0, new_head)
        
        # Remove tail if not growing
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
            self.score += 1
            
        return False  # Game continues

    def change_direction(self, direction):
        # Prevent 180-degree turns
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction

    def grow_snake(self):
        self.grow = True

    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            # Rainbow snake: head is still green, body segments use rainbow colors
            if i == 0:
                color = GREEN  # Head is still green
            else:
                # Use rainbow colors for the body, cycling through the colors
                color = RAINBOW_COLORS[i % len(RAINBOW_COLORS)]
            
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect)

class Food:
    def __init__(self, snake_positions):
        self.position = self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        while True:
            position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if position not in snake_positions:
                return position

    def draw(self, surface):
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, RED, rect)

# Grid drawing function removed as per request

def draw_score(surface, score):
    font = pygame.font.SysFont('Arial', 20)
    text = font.render(f'Score: {score}', True, BLACK)
    surface.blit(text, (5, 5))

def game_over_screen(surface, score):
    surface.fill(WHITE)
    font_large = pygame.font.SysFont('Arial', 50)
    font_small = pygame.font.SysFont('Arial', 30)
    
    game_over_text = font_large.render('GAME OVER', True, RED)
    score_text = font_small.render(f'Final Score: {score}', True, BLACK)
    restart_text = font_small.render('Press SPACE to restart', True, BLACK)
    quit_text = font_small.render('Press ESC to quit', True, BLACK)
    
    surface.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    surface.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    surface.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
    surface.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 100))
    
    pygame.display.update()

def main():
    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()
    
    # Game state
    game_active = True
    
    # Initialize game objects
    snake = Snake()
    food = Food(snake.positions)
    
    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if game_active:
                    if event.key == pygame.K_UP:
                        snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction(RIGHT)
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                else:  # Game over state
                    if event.key == pygame.K_SPACE:
                        # Restart game
                        snake = Snake()
                        food = Food(snake.positions)
                        game_active = True
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
        
        if game_active:
            # Update game state
            game_over = snake.update()
            
            if game_over:
                game_active = False
                continue
                
            # Check for food collision
            if snake.get_head_position() == food.position:
                snake.grow_snake()
                food = Food(snake.positions)
            
            # Draw everything
            screen.fill(WHITE)
            snake.draw(screen)
            food.draw(screen)
            draw_score(screen, snake.score)
            pygame.display.update()
            
            # Control game speed
            clock.tick(FPS)
        else:
            game_over_screen(screen, snake.score)

if __name__ == "__main__":
    main()










