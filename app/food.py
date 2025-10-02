import random
import pygame
# Screen dimensions
window_x=600
window_y=400
snake_block = 10  # size of one block
# Generate random position
food_x = random.randrange(0, window_x - snake_block, snake_block)
food_y = random.randrange(0, window_y - snake_block, snake_block)

food_position = [food_x, food_y]
pygame.draw.rect(game_window, pygame.Color(255, 0, 0), pygame.Rect(food_position[0], food_position[1], snake_block, snake_block))
# If snake eats the food
if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
    score += 10
    snake_body.append([0, 0])  # grow snake
    # Respawn new food
    food_x = random.randrange(0, window_x - snake_block, snake_block)
    food_y = random.randrange(0, window_y - snake_block, snake_block)
    food_position = [food_x, food_y]
