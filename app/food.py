# food.py - June Maritim
# Food Logic: Randomly spawn food, manage multiple apples

import random
import pygame

class Food:
    def __init__(self, window_width=800, window_height=600, block_size=20, 
                 play_area_top=60, play_area_bottom=None ):
        self.window_width = window_width
        self.window_height = window_height
        self.block_size = block_size

        self.play_area_top = play_area_top
        self.play_area_bottom = play_area_bottom or window_height - 60  # Footer height
        self.position = [0, 0]
        self.spawn()
    
    def spawn(self, snake_body=None):
        """Generate random position for food, avoiding snake body"""
        while True:
            x = random.randrange(0, self.window_width - self.block_size, self.block_size)
            y = random.randrange(self.play_area_top, self.play_area_bottom - self.block_size, self.block_size)
            self.position = [x, y]
            
            # Check if food spawned on snake body
            if snake_body is None:
                break
            
            collision = False
            for segment in snake_body:
                if segment[0] == x and segment[1] == y:
                    collision = True
                    break
            
            if not collision:
                break
    
    def get_position(self):
        """Return current food position"""
        return self.position