# graphics.py - Kimani Roy
# Graphics: Load and render background, snake sprites, food, sounds

import pygame
import os

class Graphics:
    def __init__(self, screen, block_size=20):
        self.screen = screen
        self.block_size = block_size
        
        # Try to load images, fall back to colored rectangles if not available
        self.use_images = True
        try:
            self.background = pygame.image.load("Assets/background.png")
            self.snake_head_img = pygame.image.load("Assets/snakehead.png")
            self.snake_body_img = pygame.image.load("Assets/snakebody.png")
            self.food_img = pygame.image.load("Assets/apple.png")
            
            # Scale images to block size
            self.snake_head_img = pygame.transform.scale(self.snake_head_img, (block_size, block_size))
            self.snake_body_img = pygame.transform.scale(self.snake_body_img, (block_size, block_size))
            self.food_img = pygame.transform.scale(self.food_img, (block_size, block_size))
        except:
            self.use_images = False
            print("Warning: Could not load image assets, using colored rectangles instead")
        
        # Try to load sounds with better error handling
        self.use_sounds = True
        self.eat_sound = None
        self.gameover_sound = None
        try:
            if pygame.mixer.get_init():
                self.eat_sound = pygame.mixer.Sound("Assets/eat.wav")
                self.gameover_sound = pygame.mixer.Sound("Assets/gameover.wav")
            else:
                self.use_sounds = False
        except (pygame.error, FileNotFoundError):
            self.use_sounds = False
            print("Warning: Could not load sound assets or no audio device available")
    
    def draw_background(self):
        """Draw checkered dark green background"""
        rows = self.screen.get_height() // self.block_size
        cols = self.screen.get_width() // self.block_size
        dark_green = (30, 60, 30)
        darker_green = (20, 40, 20)

        for row in range(rows):
            for col in range(cols):
                color = dark_green if (row + col) % 2 == 0 else darker_green
                pygame.draw.rect(
                    self.screen, color,
                    (col * self.block_size, row * self.block_size, self.block_size, self.block_size)
                )

    
    def draw_snake_head(self, x, y, direction):
        """Draw snake head, rotated based on direction"""
        if self.use_images:
            # Rotate head based on direction
            if direction == "UP":
                rotated = pygame.transform.rotate(self.snake_head_img, 90)
            elif direction == "DOWN":
                rotated = pygame.transform.rotate(self.snake_head_img, -90)
            elif direction == "LEFT":
                rotated = pygame.transform.rotate(self.snake_head_img, 180)
            else:  # RIGHT
                rotated = self.snake_head_img
            self.screen.blit(rotated, (x, y))
        else:
            # Fallback: green rectangle
            pygame.draw.rect(self.screen, (0, 255, 0), 
                           (x, y, self.block_size, self.block_size))
    
    def draw_snake_body(self, body_positions):
        """Draw all snake body segments"""
        for pos in body_positions:
            if self.use_images:
                self.screen.blit(self.snake_body_img, (pos[0], pos[1]))
            else:
                # Fallback: green rectangle
                pygame.draw.rect(self.screen, (0, 200, 0), 
                               (pos[0], pos[1], self.block_size, self.block_size))
    
    def draw_food(self, x, y):
        """Draw food/apple"""
        if self.use_images:
            self.screen.blit(self.food_img, (x, y))
        else:
            # Fallback: red rectangle
            pygame.draw.rect(self.screen, (255, 0, 0), 
                           (x, y, self.block_size, self.block_size))
    
    def play_eat_sound(self):
        """Play sound when snake eats food"""
        if self.use_sounds and self.eat_sound:
            try:
                self.eat_sound.play()
            except:
                pass
    
    def play_crash_sound(self):
        """Play sound when game is over"""
        if self.use_sounds and self.gameover_sound:
            try:
                self.gameover_sound.play()
            except:
                pass
    
    def draw_obstacles(self, obstacle_positions):
        """Draw all obstacles"""
        for pos in obstacle_positions:
            # Draw obstacle as gray/stone block
            pygame.draw.rect(self.screen, (128, 128, 128), 
                           (pos[0], pos[1], self.block_size, self.block_size))
            # Add border for 3D effect
            pygame.draw.rect(self.screen, (80, 80, 80), 
                           (pos[0], pos[1], self.block_size, self.block_size), 2)