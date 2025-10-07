# obstacles.py - Obstacle Management
# Handles spawning and managing obstacles/barriers

import random
import pygame

class Obstacle:
    def __init__(self, position, block_size=20):
        self.position = position  # [x, y]
        self.block_size = block_size
    
    def get_position(self):
        return self.position

class ObstacleManager:
    def __init__(self, window_width=800, window_height=600, block_size=20):
        self.window_width = window_width
        self.window_height = window_height
        self.block_size = block_size
        self.obstacles = []
    
    def spawn_obstacle(self, snake_body, food_position):
        """Spawn a new obstacle at a random valid position"""
        max_attempts = 100
        attempts = 0
        
        while attempts < max_attempts:
            x = random.randrange(0, self.window_width - self.block_size, self.block_size)
            y = random.randrange(0, self.window_height - self.block_size, self.block_size)
            
            # Check if position is valid (not on snake, food, or other obstacles)
            valid = True
            
            # Check snake body
            for segment in snake_body:
                if segment[0] == x and segment[1] == y:
                    valid = False
                    break
            
            # Check food
            if food_position[0] == x and food_position[1] == y:
                valid = False
            
            # Check other obstacles
            for obs in self.obstacles:
                if obs.position[0] == x and obs.position[1] == y:
                    valid = False
                    break
            
            # Check if too close to edges (leave some margin)
            margin = self.block_size * 3
            if (x < margin or x > self.window_width - margin - self.block_size or
                y < margin or y > self.window_height - margin - self.block_size):
                valid = False
            
            if valid:
                self.obstacles.append(Obstacle([x, y], self.block_size))
                return True
            
            attempts += 1
        
        return False  # Failed to find valid position
    
    def check_collision(self, position):
        """Check if position collides with any obstacle"""
        for obs in self.obstacles:
            if obs.position[0] == position[0] and obs.position[1] == position[1]:
                return True
        return False
    
    def get_all_positions(self):
        """Return list of all obstacle positions"""
        return [obs.position for obs in self.obstacles]
    
    def clear_obstacles(self):
        """Remove all obstacles"""
        self.obstacles = []
    
    def obstacle_count(self):
        """Return number of obstacles"""
        return len(self.obstacles)