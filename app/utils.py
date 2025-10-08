# utils.py - Edith Agai
# Constants and helper functions

import pygame

# Screen dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# UI margins (reserved for header and footer)
HEADER_HEIGHT = 60
FOOTER_HEIGHT = 60
PLAY_AREA_TOP = HEADER_HEIGHT
PLAY_AREA_BOTTOM = WINDOW_HEIGHT - FOOTER_HEIGHT

# Block/Grid size
BLOCK_SIZE = 20

# Game speed settings (FPS)
STARTING_SPEED = 5  # Slower start
MAX_SPEED = 20  # Maximum speed
SPEED_INCREASE_INTERVAL = 30  # Increase speed every 30 points

# Obstacle settings
OBSTACLE_SPAWN_SCORE = 50  # Start spawning obstacles at 50 points
OBSTACLE_INCREASE_INTERVAL = 40  # Add new obstacle every 40 points
MAX_OBSTACLES = 10  # Maximum number of obstacles

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_GRAY = (20, 20, 20)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Score per food
POINTS_PER_FOOD = 10

# Starting position for snake
START_POSITION = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

def init_pygame():
    """Initialize pygame and mixer (with error handling)"""
    pygame.init()
    try:
        pygame.mixer.init()
    except pygame.error:
        print("Warning: No audio device found. Game will run without sound.")

def create_window(width, height, title):
    """Create and return game window"""
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    return screen

def center_text(text, font, screen):
    """Helper to center text on screen"""
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    return text_rect

def calculate_game_speed(score):
    """Calculate current game speed based on score"""
    speed_increments = score // SPEED_INCREASE_INTERVAL
    new_speed = STARTING_SPEED + speed_increments
    return min(new_speed, MAX_SPEED)  # Cap at max speed

def should_spawn_obstacle(score, current_obstacles):
    """Determine if a new obstacle should spawn"""
    if score < OBSTACLE_SPAWN_SCORE:
        return False
    if current_obstacles >= MAX_OBSTACLES:
        return False
    
    # Calculate how many obstacles should exist at this score
    expected_obstacles = 1 + (score - OBSTACLE_SPAWN_SCORE) // OBSTACLE_INCREASE_INTERVAL
    expected_obstacles = min(expected_obstacles, MAX_OBSTACLES)
    
    return current_obstacles < expected_obstacles