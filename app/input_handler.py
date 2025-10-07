# input_handler.py - Pascal Ng'ang'a
# Input Handler: Detect arrow keys, prevent opposite direction

import pygame

class InputHandler:
    def __init__(self):
        self.current_direction = "RIGHT"  # Default starting direction
    
    def get_direction(self, current_direction):
        """
        Get new direction from keyboard input.
        Prevents snake from going in opposite direction instantly.
        """
        self.current_direction = current_direction
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None  # Signal to quit game
            
            if event.type == pygame.KEYDOWN:
                # Check arrow keys and prevent opposite direction
                if event.key == pygame.K_UP and current_direction != "DOWN":
                    return "UP"
                elif event.key == pygame.K_DOWN and current_direction != "UP":
                    return "DOWN"
                elif event.key == pygame.K_LEFT and current_direction != "RIGHT":
                    return "LEFT"
                elif event.key == pygame.K_RIGHT and current_direction != "LEFT":
                    return "RIGHT"
        
        # Return current direction if no valid key pressed
        return current_direction
    
    def check_quit(self):
        """Check if user wants to quit"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
        return False
    
    def wait_for_restart(self):
        """Wait for user to press Y (restart) or N (quit)"""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        return True  # Restart
                    elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                        return False  # Quit
        return False