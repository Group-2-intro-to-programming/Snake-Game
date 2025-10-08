# score.py - Warren Maina
# Score & End Screen: Track score, high score, display game over screen

import pygame
import os
import sys


class ScoreManager:
    def __init__(self, highscore_file="highscore.txt"):
        self.score = 0
        self.highscore_file = highscore_file
        self.high_score = self.load_high_score()
        self.player_name = "Player"
        
        # Initialize font
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        
        # Asset path
        self.asset_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
    
    def ask_player_name(self, screen):
        """Prompt player to enter their name"""
        font = pygame.font.Font(None, 48)
        small_font = pygame.font.Font(None, 32)
        name = ""
        input_active = True
        
        while input_active:   
            screen.fill((0, 30, 0))
            
            # Title
            title = self.large_font.render("SNAKE GAME", True, (0, 255, 0))
            title_rect = title.get_rect(center=(screen.get_width()//2, 100))
            screen.blit(title, title_rect)
            
            # Prompt
            prompt1 = font.render("Enter your name:", True, (255, 255, 255))
            rect = prompt1.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 50))
            screen.blit(prompt1, rect)
            
            # Name input box
            input_box = pygame.Rect(screen.get_width()//2 - 150, 
                                   screen.get_height()//2, 300, 50)
            pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
            
            name_surf = font.render(name, True, (255, 255, 0))
            name_rect = name_surf.get_rect(center=(screen.get_width()//2, 
                                                   screen.get_height()//2 + 25))
            screen.blit(name_surf, name_rect)
            
            # Instructions
            prompt2 = small_font.render("(Max 10 characters - Press ENTER to confirm)", 
                                       True, (200, 200, 200))
            rect2 = prompt2.get_rect(center=(screen.get_width()//2, 
                                            screen.get_height()//2 + 100))
            screen.blit(prompt2, rect2)
            
            pygame.display.flip()
            
            # Input handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if name.strip():
                            input_active = False
                            self.player_name = name.strip()[:10]
                        else:
                            self.player_name = "Player"
                            input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif len(name) < 10 and event.unicode.isprintable():
                        name += event.unicode
    
    def load_high_score(self):
        """Load high score from file"""
        try:
            if os.path.exists(self.highscore_file):
                with open(self.highscore_file, 'r') as f:
                    return int(f.read().strip())
        except:
            pass
        return 0
    
    def save_high_score(self):
        """Save high score to file"""
        try:
            with open(self.highscore_file, 'w') as f:
                f.write(str(self.high_score))
        except:
            print("⚠ Warning: Could not save high score")
    
    def add_point(self, points=10):
        """Add points to current score"""
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
    
    def reset_score(self):
        """Reset current score to 0"""
        self.score = 0
    
    def draw(self, screen, current_speed=None, obstacle_count=0):
        """Draw method - now handled by graphics.py header/footer"""
        pass

    def start_screen(self, screen):
        """Display start screen before the game begins"""
        screen.fill((10, 30, 10))
        
        # Title
        title_text = self.large_font.render("SNAKE GAME", True, (0, 255, 0))
        title_rect = title_text.get_rect(center=(screen.get_width()//2, 
                                                 screen.get_height()//2 - 100))
        screen.blit(title_text, title_rect)
        
        # Player greeting
        greeting_font = pygame.font.Font(None, 42)
        greeting = greeting_font.render(f"Welcome, {self.player_name}!", 
                                       True, (255, 255, 0))
        greeting_rect = greeting.get_rect(center=(screen.get_width()//2, 
                                                  screen.get_height()//2 - 30))
        screen.blit(greeting, greeting_rect)
        
        # Instructions
        start_text = self.font.render("Press ENTER to Start", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(screen.get_width()//2, 
                                                 screen.get_height()//2 + 40))
        screen.blit(start_text, start_rect)
        
        # Controls
        controls_font = pygame.font.Font(None, 28)
        controls = [
            "Use ARROW KEYS to control the snake",
            "Eat apples to grow and gain points",
            "Avoid walls, obstacles, and yourself!"
        ]
        y_offset = 120
        for i, line in enumerate(controls):
            control_text = controls_font.render(line, True, (150, 150, 150))
            control_rect = control_text.get_rect(center=(screen.get_width()//2, 
                                                         screen.get_height()//2 + y_offset + i*30))
            screen.blit(control_text, control_rect)
        
        pygame.display.flip()
        
        # Wait for ENTER key
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        waiting = False

    def game_over_screen(self, screen):
        """Display game over screen with background image"""
        # Try to load game over image
        try:
            bg_path = os.path.join(self.asset_path, 'game_over.jpg')
            bg_image = pygame.image.load(bg_path).convert()
            bg_image = pygame.transform.scale(bg_image, 
                                             (screen.get_width(), screen.get_height()))
        except Exception as e:
            print(f"⚠ Warning: Could not load game over image - {e}")
            bg_image = None
        
        # Display background
        if bg_image:
            screen.blit(bg_image, (0, 0))
            # Add semi-transparent overlay for better text readability
            overlay = pygame.Surface((screen.get_width(), screen.get_height()))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
        else:
            screen.fill((30, 0, 0))  # Dark red background
        
        # Game Over text
        game_over_text = self.large_font.render("GAME OVER", True, (255, 50, 50))
        game_over_rect = game_over_text.get_rect(center=(screen.get_width() // 2, 
                                                         screen.get_height() // 2 - 100))
        screen.blit(game_over_text, game_over_rect)
        
        # Final score
        final_score = self.font.render(f"{self.player_name}'s Score: {self.score}", 
                                      True, (255, 255, 255))
        screen.blit(final_score, 
                   (screen.get_width() // 2 - final_score.get_width() // 2, 
                    screen.get_height() // 2 - 20))
        
        # High score
        high_score = self.font.render(f"High Score: {self.high_score}", 
                                     True, (255, 215, 0))
        screen.blit(high_score, 
                   (screen.get_width() // 2 - high_score.get_width() // 2, 
                    screen.get_height() // 2 + 30))
        
        # New high score message
        if self.score == self.high_score and self.score > 0:
            new_high = self.font.render("NEW HIGH SCORE!", True, (255, 215, 0))
            screen.blit(new_high, 
                       (screen.get_width() // 2 - new_high.get_width() // 2, 
                        screen.get_height() // 2 + 80))
        
        # Restart prompt
        restart = self.font.render("Press Y to Restart / N to Quit", 
                                  True, (200, 200, 200))
        screen.blit(restart, 
                   (screen.get_width() // 2 - restart.get_width() // 2, 
                    screen.get_height() // 2 + 140))
        
        pygame.display.flip()