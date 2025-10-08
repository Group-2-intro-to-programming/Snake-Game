# snake.py - Ashley Chege
# Snake Logic: Movement, growing, collision detection

import pygame

class Snake:
    def __init__(self, start_pos=(100, 100), block_size=20):
        self.block_size = block_size
        # Snake body is a list of [x, y] positions
        self.body = [
            list(start_pos),
            [start_pos[0] - block_size, start_pos[1]],
            [start_pos[0] - 2 * block_size, start_pos[1]]
        ]
        self.direction = "RIGHT"  # Initial direction
        self.grow_flag = False
    
    @property
    def head(self):
        """Return the position of snake's head"""
        return self.body[0]
    
    def move(self, direction):
        """Move snake in the given direction"""
        self.direction = direction
        head_x, head_y = self.head
        
        # Calculate new head position based on direction
        if direction == "UP":
            head_y -= self.block_size
        elif direction == "DOWN":
            head_y += self.block_size
        elif direction == "LEFT":
            head_x -= self.block_size
        elif direction == "RIGHT":
            head_x += self.block_size
        
        # Insert new head at the beginning
        new_head = [head_x, head_y]
        self.body.insert(0, new_head)
        
        # Remove tail unless snake is growing
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False
    
    def grow(self):
        """Set flag to grow snake on next move"""
        self.grow_flag = True
    
    def check_self_collision(self):
        """Check if snake head collides with its body"""
        head = self.head
        for segment in self.body[1:]:
            if head[0] == segment[0] and head[1] == segment[1]:
                return True
        return False
    
    def check_wall_collision(self, window_width, window_height, play_area_top=60, play_area_bottom=540):
        """Check if snake hits the wall or UI boundaries"""
        head_x, head_y = self.head
        if (head_x < 0 or head_x >= window_width or 
            head_y < play_area_top or head_y >= play_area_bottom):
            return True
        return False
    
    def collided(self, window_width=800, window_height=600, play_area_top=60, play_area_bottom=540):
        """Check all collision types"""
        return self.check_self_collision() or self.check_wall_collision(window_width, window_height, play_area_top, play_area_bottom)