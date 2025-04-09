#!/usr/bin/env python3
"""
Snake Game
A simple implementation of the classic Snake game using Pygame.
Now with an enemy snake that you need to avoid!
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
PURPLE = Color(128, 0, 128)

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

# Enemy snake colors
ENEMY_COLORS = [
    Color(128, 0, 128),    # Purple
    Color(75, 0, 130),     # Indigo
    Color(0, 0, 139)       # Dark Blue
]

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
ALL_DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.grow = False
        self.score = 0
        self.is_dead = False

    def get_head_position(self):
        return self.positions[0]

    def get_all_positions(self):
        return self.positions

    def update(self, enemy_positions=None):
        if self.is_dead:
            return True
            
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
            self.is_dead = True
            return True  # Game over
            
        # Check for collision with enemy snake if provided
        if enemy_positions and new_head in enemy_positions:
            self.is_dead = True
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
            
class EnemySnake:
    def __init__(self, player_positions):
        # Start the enemy snake at a random position away from the player
        self.positions = self._get_initial_position(player_positions)
        self.direction = random.choice(ALL_DIRECTIONS)
        self.length = 5  # Initial length
        self.move_counter = 0
        self.move_delay = 2  # Move every N frames (slower than player)
        
    def _get_initial_position(self, player_positions):
        # Start with a single position for the head
        while True:
            head_pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            # Make sure it's far enough from the player (at least 5 grid cells away)
            if head_pos not in player_positions and all(
                abs(head_pos[0] - p[0]) + abs(head_pos[1] - p[1]) > 5 
                for p in player_positions
            ):
                # Generate a body based on the head position
                positions = [head_pos]
                curr_pos = head_pos
                # Choose a random direction for the body
                body_dir = random.choice(ALL_DIRECTIONS)
                for _ in range(self.length - 1):
                    next_x = (curr_pos[0] - body_dir[0]) % GRID_WIDTH
                    next_y = (curr_pos[1] - body_dir[1]) % GRID_HEIGHT
                    curr_pos = (next_x, next_y)
                    positions.append(curr_pos)
                return positions
    
    def get_head_position(self):
        return self.positions[0]
        
    def get_all_positions(self):
        return self.positions
        
    def update(self, player_positions):
        self.move_counter += 1
        if self.move_counter < self.move_delay:
            return
            
        self.move_counter = 0
        
        # Occasionally change direction randomly
        if random.random() < 0.2:  # 20% chance to change direction
            possible_directions = [d for d in ALL_DIRECTIONS 
                                  if (d[0] * -1, d[1] * -1) != self.direction]
            self.direction = random.choice(possible_directions)
        
        # Get current head position
        head = self.get_head_position()
        
        # Calculate new head position
        new_x = (head[0] + self.direction[0]) % GRID_WIDTH
        new_y = (head[1] + self.direction[1]) % GRID_HEIGHT
        new_head = (new_x, new_y)
        
        # If new head would collide with itself, change direction
        if new_head in self.positions:
            # Try to find a direction that doesn't cause collision
            for test_dir in ALL_DIRECTIONS:
                if (test_dir[0] * -1, test_dir[1] * -1) == self.direction:
                    continue  # Skip 180-degree turn
                    
                test_x = (head[0] + test_dir[0]) % GRID_WIDTH
                test_y = (head[1] + test_dir[1]) % GRID_HEIGHT
                test_head = (test_x, test_y)
                
                if test_head not in self.positions:
                    self.direction = test_dir
                    new_x, new_y = test_x, test_y
                    new_head = test_head
                    break
        
        # Add new head
        self.positions.insert(0, new_head)
        
        # Keep the snake at a fixed length
        while len(self.positions) > self.length:
            self.positions.pop()
            
    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            if i == 0:
                color = PURPLE  # Head is purple
            else:
                # Use enemy colors for the body
                color = ENEMY_COLORS[i % len(ENEMY_COLORS)]
            
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect)

class Food:
    def __init__(self, snake_positions, enemy_positions=None):
        all_positions = snake_positions.copy()
        if enemy_positions:
            all_positions.extend(enemy_positions)
        self.position = self.randomize_position(all_positions)

    def randomize_position(self, occupied_positions):
        while True:
            position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if position not in occupied_positions:
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
    
    # Add a message about the enemy snake
    enemy_text = font_small.render('Watch out for the purple enemy snake!', True, PURPLE)
    
    surface.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    surface.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    surface.blit(enemy_text, (WIDTH // 2 - enemy_text.get_width() // 2, HEIGHT // 2 + 30))
    surface.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 70))
    surface.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 110))
    
    pygame.display.update()

def main():
    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake Game with Enemy')
    clock = pygame.time.Clock()
    
    # Game state
    game_active = True
    
    # Initialize game objects
    snake = Snake()
    enemy_snake = EnemySnake(snake.get_all_positions())
    food = Food(snake.get_all_positions(), enemy_snake.get_all_positions())
    
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
                        enemy_snake = EnemySnake(snake.get_all_positions())
                        food = Food(snake.get_all_positions(), enemy_snake.get_all_positions())
                        game_active = True
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
        
        if game_active:
            # Update enemy snake first
            enemy_snake.update(snake.get_all_positions())
            
            # Update player snake, checking for collision with enemy
            game_over = snake.update(enemy_snake.get_all_positions())
            
            if game_over:
                game_active = False
                continue
                
            # Check for food collision
            if snake.get_head_position() == food.position:
                snake.grow_snake()
                food = Food(snake.get_all_positions(), enemy_snake.get_all_positions())
            
            # Draw everything
            screen.fill(WHITE)
            snake.draw(screen)
            enemy_snake.draw(screen)
            food.draw(screen)
            draw_score(screen, snake.score)
            pygame.display.update()
            
            # Control game speed
            clock.tick(FPS)
        else:
            game_over_screen(screen, snake.score)

if __name__ == "__main__":
    main()















