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


def initialize_game():
    """Initialize pygame and create game window"""
    init_pygame()
    screen = create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Snake Game - Group 2")
    return screen


def get_player_info(screen):
    """Get player name and show start screen"""
    score_manager = ScoreManager()
    score_manager.ask_player_name(screen)
    score_manager.start_screen(screen)
    return score_manager.player_name


def create_game_objects(screen, player_name):
    """Create all game objects for a new game"""
    snake = Snake(start_pos=START_POSITION, block_size=BLOCK_SIZE)
    food = Food(window_width=WINDOW_WIDTH, window_height=WINDOW_HEIGHT, 
                block_size=BLOCK_SIZE, play_area_top=PLAY_AREA_TOP, 
                play_area_bottom=PLAY_AREA_BOTTOM)
    obstacles = ObstacleManager(window_width=WINDOW_WIDTH, 
                               window_height=WINDOW_HEIGHT, 
                               block_size=BLOCK_SIZE)
    graphics = Graphics(screen, block_size=BLOCK_SIZE)
    input_handler = InputHandler()
    score_manager = ScoreManager()
    score_manager.player_name = player_name
    
    return snake, food, obstacles, graphics, input_handler, score_manager


def handle_food_collection(snake, food, score_manager, graphics, obstacles):
    """Handle when snake eats food"""
    snake.grow()
    score_manager.add_point(POINTS_PER_FOOD)
    graphics.play_eat_sound()
    
    # Play score-up sound every 50 points
    if score_manager.score % 50 == 0 and score_manager.score > 0:
        graphics.play_scoreup_sound()
    
    food.spawn(snake.body)
    
    # Check if we should spawn a new obstacle
    if should_spawn_obstacle(score_manager.score, obstacles.obstacle_count()):
        obstacles.spawn_obstacle(snake.body, food.position)


def check_collisions(snake, obstacles):
    """Check all collision types"""
    hit_wall_or_self = snake.collided(WINDOW_WIDTH, WINDOW_HEIGHT)
    hit_obstacle = obstacles.check_collision(snake.head)
    return hit_wall_or_self or hit_obstacle


def render_game(screen, graphics, snake, food, obstacles, score_manager, 
                direction, current_speed):
    """Render all game elements"""
    graphics.draw_background()
    graphics.draw_obstacles(obstacles.get_all_positions())
    
    # Draw snake body (excluding head)
    if len(snake.body) > 1:
        graphics.draw_snake_body(snake.body[1:])
    
    # Draw snake head
    graphics.draw_snake_head(snake.head[0], snake.head[1], direction)
    
    # Draw food
    graphics.draw_food(food.position[0], food.position[1])
    
    # Draw UI
    score_manager.draw(screen, current_speed, obstacles.obstacle_count())

    #Header and Footer
    graphics.draw_header(
        score_manager.player_name, score_manager.score, score_manager.high_score
    )
    level = calculate_level(score_manager.score)
    graphics.draw_footer(
        level, obstacles.obstacle_count()
        )

    
    pygame.display.flip()


def game_loop(screen, player_name):
    """Main game loop for a single game session"""
    # Create game objects
    snake, food, obstacles, graphics, input_handler, score_manager = \
        create_game_objects(screen, player_name)
    
    # Game state
    clock = pygame.time.Clock()
    running = True
    direction = "RIGHT"
    current_speed = STARTING_SPEED
    
    while running:
        # Handle input
        new_direction = input_handler.get_direction(direction)
        
        # Check if user wants to quit
        if new_direction is None:
            return False  # Signal to quit entire game
        
        direction = new_direction
        
        # Move snake
        snake.move(direction)
        
        # Check if snake ate food
        if snake.head[0] == food.position[0] and snake.head[1] == food.position[1]:
            handle_food_collection(snake, food, score_manager, graphics, obstacles)
            current_speed = calculate_game_speed(score_manager.score)
        
        # Check collisions
        if check_collisions(snake, obstacles):
            graphics.play_crash_sound()
            running = False
        
        # Render everything
        render_game(screen, graphics, snake, food, obstacles, 
                   score_manager, direction, current_speed)
        
        # Control game speed
        clock.tick(current_speed)
    
    # Game over sequence
    graphics.play_gameover_music()
    score_manager.game_over_screen(screen)
    
    # Wait for restart decision
    return input_handler.wait_for_restart()


def main():
    """Main game function"""
    # Initialize game
    screen = initialize_game()
    
    # Get player info once at the start
    player_name = get_player_info(screen)
    
    # Game loop - keep playing until user quits
    play_again = True
    while play_again:
      play_again = game_loop(screen, player_name)
    
    # Cleanup
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()