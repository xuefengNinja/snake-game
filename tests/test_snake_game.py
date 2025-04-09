#!/usr/bin/env python3
"""
Unit tests for the Snake Game
"""

import unittest
import sys
import os
import pygame
from collections import namedtuple

# Add parent directory to path so we can import snake_game
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import snake_game

# Initialize pygame for testing
pygame.init()

class TestSnake(unittest.TestCase):
    def setUp(self):
        # Initialize a snake for testing
        self.snake = snake_game.Snake()
        
    def test_initial_state(self):
        # Test initial snake state
        self.assertEqual(len(self.snake.positions), 1)
        self.assertEqual(self.snake.direction, snake_game.RIGHT)
        self.assertEqual(self.snake.next_direction, snake_game.RIGHT)
        self.assertFalse(self.snake.grow)
        self.assertEqual(self.snake.score, 0)
        self.assertFalse(self.snake.is_dead)
        
    def test_get_head_position(self):
        # Test head position getter
        head_pos = self.snake.get_head_position()
        self.assertEqual(head_pos, self.snake.positions[0])
        
    def test_get_all_positions(self):
        # Test all positions getter
        all_pos = self.snake.get_all_positions()
        self.assertEqual(all_pos, self.snake.positions)
        
    def test_change_direction(self):
        # Test changing direction
        self.snake.change_direction(snake_game.UP)
        self.assertEqual(self.snake.next_direction, snake_game.UP)
        
        # Test that 180-degree turns are prevented
        self.snake.direction = snake_game.UP
        self.snake.change_direction(snake_game.DOWN)
        self.assertEqual(self.snake.next_direction, snake_game.UP)  # Direction shouldn't change
        
    def test_grow_snake(self):
        # Test growing the snake
        self.snake.grow_snake()
        self.assertTrue(self.snake.grow)
        
    def test_update_movement(self):
        # Test basic movement
        initial_head = self.snake.get_head_position()
        self.snake.update()
        new_head = self.snake.get_head_position()
        
        # Moving right should increase x by 1
        self.assertEqual(new_head[0], (initial_head[0] + 1) % snake_game.GRID_WIDTH)
        self.assertEqual(new_head[1], initial_head[1])
        
    def test_self_collision(self):
        # Create a snake that will collide with itself
        self.snake.positions = [(5, 5), (6, 5), (7, 5)]
        self.snake.direction = snake_game.LEFT
        self.snake.next_direction = snake_game.LEFT
        
        # Update should detect collision and return True (game over)
        result = self.snake.update()
        self.assertTrue(result)
        self.assertTrue(self.snake.is_dead)
        
    def test_enemy_collision(self):
        # Test collision with enemy snake
        self.snake.positions = [(5, 5)]
        enemy_positions = [(6, 5), (7, 5)]
        
        # No collision yet
        result = self.snake.update(enemy_positions)
        self.assertFalse(result)
        
        # Now there will be a collision
        enemy_positions = [(6, 5)]  # Where the snake head will be after moving right
        result = self.snake.update(enemy_positions)
        self.assertTrue(result)
        self.assertTrue(self.snake.is_dead)
        
    def test_growing_increases_length(self):
        # Test that growing increases snake length
        initial_length = len(self.snake.positions)
        self.snake.grow_snake()
        self.snake.update()
        self.assertEqual(len(self.snake.positions), initial_length + 1)
        
class TestEnemySnake(unittest.TestCase):
    def setUp(self):
        # Initialize an enemy snake for testing
        player_positions = [(10, 10)]
        self.enemy = snake_game.EnemySnake(player_positions)
        
    def test_initial_state(self):
        # Test initial enemy snake state
        self.assertEqual(len(self.enemy.positions), self.enemy.length)
        self.assertIn(self.enemy.direction, snake_game.ALL_DIRECTIONS)
        
    def test_get_head_position(self):
        # Test head position getter
        head_pos = self.enemy.get_head_position()
        self.assertEqual(head_pos, self.enemy.positions[0])
        
    def test_get_all_positions(self):
        # Test all positions getter
        all_pos = self.enemy.get_all_positions()
        self.assertEqual(all_pos, self.enemy.positions)
        
    def test_update_movement(self):
        # Test that the enemy snake moves
        initial_head = self.enemy.get_head_position()
        
        # Force a specific direction for testing
        self.enemy.direction = snake_game.RIGHT
        self.enemy.move_counter = self.enemy.move_delay  # Ensure it will move
        
        self.enemy.update([])
        new_head = self.enemy.get_head_position()
        
        # Should have moved in the direction specified
        expected_x = (initial_head[0] + snake_game.RIGHT[0]) % snake_game.GRID_WIDTH
        expected_y = (initial_head[1] + snake_game.RIGHT[1]) % snake_game.GRID_HEIGHT
        self.assertEqual(new_head, (expected_x, expected_y))
        
    def test_constant_length(self):
        # Test that the enemy snake maintains a constant length
        initial_length = len(self.enemy.positions)
        
        # Update multiple times
        for _ in range(5):
            self.enemy.move_counter = self.enemy.move_delay  # Ensure it will move
            self.enemy.update([])
            
        # Length should remain the same
        self.assertEqual(len(self.enemy.positions), initial_length)
        
class TestFood(unittest.TestCase):
    def setUp(self):
        # Initialize food for testing
        self.snake_positions = [(10, 10), (11, 10)]
        self.enemy_positions = [(5, 5), (6, 5)]
        self.food = snake_game.Food(self.snake_positions, self.enemy_positions)
        
    def test_food_position(self):
        # Test that food is not on a snake or enemy position
        self.assertNotIn(self.food.position, self.snake_positions)
        self.assertNotIn(self.food.position, self.enemy_positions)
        
    def test_randomize_position(self):
        # Test that randomize_position returns a valid position
        new_position = self.food.randomize_position(self.snake_positions + self.enemy_positions)
        self.assertNotIn(new_position, self.snake_positions)
        self.assertNotIn(new_position, self.enemy_positions)
        
        # Test that position is within grid bounds
        self.assertTrue(0 <= new_position[0] < snake_game.GRID_WIDTH)
        self.assertTrue(0 <= new_position[1] < snake_game.GRID_HEIGHT)

if __name__ == '__main__':
    unittest.main()
