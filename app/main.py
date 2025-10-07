# main.py - Edith Agai (Integrator)
# Main game loop - integrates all modules

import pygame
import sys
from graphics import Graphics
from snake import Snake
from food import Food
from obstacles import ObstacleManager
from input_handler import InputHandler
from score import ScoreManager
from utils import *

def main():
    """Main game function"""
    # Initialize pygame
    init_pygame()
    
    # Create game window
    screen = create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Snake Game - Group 2")
    score_manager = ScoreManager()
    score_manager.ask_player_name(screen)
    score_manager.start_screen(screen)

    # Create clock for FPS control
    clock = pygame.time.Clock()
    
    # Game loop flag
    play_again = True
    
    while play_again:
        # Initialize game objects
        snake = Snake(start_pos=START_POSITION, block_size=BLOCK_SIZE)
        food = Food(window_width=WINDOW_WIDTH, window_height=WINDOW_HEIGHT, block_size=BLOCK_SIZE)
        obstacles = ObstacleManager(window_width=WINDOW_WIDTH, window_height=WINDOW_HEIGHT, block_size=BLOCK_SIZE)
        graphics = Graphics(screen, block_size=BLOCK_SIZE)
        input_handler = InputHandler()
        score_manager = ScoreManager()
        
        # Game state
        running = True
        direction = "RIGHT"
        current_speed = STARTING_SPEED
        
        # Main game loop
        while running:
            # Handle input
            new_direction = input_handler.get_direction(direction)
            
            # Check if user wants to quit
            if new_direction is None:
                running = False
                play_again = False
                break
            
            direction = new_direction
            
            # Move snake
            snake.move(direction)
            
            # Check if snake ate food
            if snake.head[0] == food.position[0] and snake.head[1] == food.position[1]:
                snake.grow()
                score_manager.add_point(POINTS_PER_FOOD)
                food.spawn(snake.body)
                graphics.play_eat_sound()
                
                # Update speed based on score
                current_speed = calculate_game_speed(score_manager.score)
                
                # Check if we should spawn a new obstacle
                if should_spawn_obstacle(score_manager.score, obstacles.obstacle_count()):
                    obstacles.spawn_obstacle(snake.body, food.position)
            
            # Check collisions (wall, self, or obstacles)
            hit_wall_or_self = snake.collided(WINDOW_WIDTH, WINDOW_HEIGHT)
            hit_obstacle = obstacles.check_collision(snake.head)
            
            if hit_wall_or_self or hit_obstacle:
                graphics.play_crash_sound()
                running = False
            
            # Draw everything
            graphics.draw_background()
            
            # Draw obstacles
            graphics.draw_obstacles(obstacles.get_all_positions())
            
            # Draw snake body (excluding head)
            if len(snake.body) > 1:
                graphics.draw_snake_body(snake.body[1:])
            
            # Draw snake head
            graphics.draw_snake_head(snake.head[0], snake.head[1], direction)
            
            # Draw food
            graphics.draw_food(food.position[0], food.position[1])
            
            # Draw score with speed and obstacle info
            score_manager.draw(screen, current_speed, obstacles.obstacle_count())
            
            # Update display
            pygame.display.flip()
            
            # Control game speed (increases as score increases)
            clock.tick(current_speed)
        
        # Game over - show end screen
        if play_again:  # Only show if didn't quit during game
            score_manager.game_over_screen(screen)
            pygame.display.flip()
            play_again = input_handler.wait_for_restart()
    
    # Quit pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()