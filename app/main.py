import pygame
from graphics import Graphics
from snake import Snake
from food import Food
from input_handler import InputHandler
from score import ScoreManager
from utils import *

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock to control FPS
clock = pygame.time.Clock()

# Game objects
snake = Snake()
food = Food()
graphics = Graphics(screen)   # ✅ pass screen here
input_handler = InputHandler()
score = ScoreManager()

# Game loop
running = True
direction = "RIGHT"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    direction = input_handler.get_direction(direction)
    snake.move(direction)

    if snake.head == food.position:
        snake.grow()
        score.add_point()
        food.spawn()
        graphics.play_eat_sound()

    if snake.collided():
        graphics.play_crash_sound()
        running = False

    # Draw everything
    graphics.draw_background()
    graphics.draw_snake_head(snake.head[0], snake.head[1], direction)
    graphics.draw_snake_body(snake.body)
    graphics.draw_food(food.position[0], food.position[1])
    score.draw(screen)

    pygame.display.flip()
    clock.tick(10)  # control game speed

pygame.quit()
