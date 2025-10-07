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
        self.player_name = None
        
        # Initialize font
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
    
    def ask_player_name(self, screen):
        """Prompt player to enter their name"""
        font = pygame.font.Font(None, 48)
        name = ""
        input_active = True


        while input_active:   
            screen.fill((0, 30, 0))
            prompt1 = font.render("Enter your name (max 10 chars):", True, (255, 255, 255))
            rect = prompt1.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 50))
            prompt2 = font.render("Press ENTER to confirm", True, (200, 200, 200))
            rect2 = prompt2.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 80))
            screen.blit(prompt1, rect)
            screen.blit(prompt2, rect2)

            name_surf = font.render(name, True, (255, 255, 0))
            name_rect = name_surf.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 20))
            screen.blit(name_surf, name_rect)

            pygame.display.flip()

            #input handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if name.strip() != "":
                            input_active = False
                            self.player_name = name.strip()[:10]  # Limit to 10 chars
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 10 and event.unicode.isprintable():
                            name += event.unicode
        self.player_name = name if name else "Player"                        

          
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
            print("Warning: Could not save high score")
    
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
        """Draw score, high score, speed, and obstacle count on screen"""
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, (255, 215, 0))
        
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (screen.get_width() - high_score_text.get_width() - 10, 10))
        
        # Display current speed/level
        if current_speed:
            level = current_speed - 4 # Assuming starting speed is 5
            speed_text = self.font.render(f"Level: {level}", True, (0, 255, 255))
            screen.blit(speed_text, (10, screen.get_height() - 80))
        
        # Display obstacle count
        if obstacle_count > 0:
            obstacle_text = self.font.render(f"Obstacles: {obstacle_count}", True, (255, 165, 0))
            screen.blit(obstacle_text, (10, screen.get_height() - 40))

    def start_screen(self, screen):
        """Display start screen before the game begins"""
        screen.fill((10, 30, 10))  # dark green

        title_font = pygame.font.Font(None, 96)
        title_text = title_font.render("SNAKE GAME", True, (0, 255, 0))
        title_rect = title_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 100))
        screen.blit(title_text, title_rect)

        start_font = pygame.font.Font(None, 48)
        start_text = start_font.render("Press ENTER to Start", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
        screen.blit(start_text, start_rect)


     # Wait for ENTER key to start
        pygame.display.flip()
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
        """Display game over screen with background image."""
        try:
            bg_image = pygame.image.load("assets/game_over.png").convert()
            bg_image = pygame.transform.scale(bg_image, (screen.get_width(), screen.get_height()))
        except:
            bg_image = None  # fallback if image not found

        font = pygame.font.Font(None, 72)
        score_font = pygame.font.Font(None, 36)

        if bg_image:
            self.fade_in(screen, bg_image)
        else:
            screen.fill((30, 0, 0))  # Dark red background

        # Overlay text
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100))
        screen.blit(game_over_text, game_over_rect)

        final_score = score_font.render(f"{self.player_name} Score: {self.score}", True, (255, 255, 255))
        screen.blit(final_score, (screen.get_width() // 2 - final_score.get_width() // 2, screen.get_height() // 2))

        high_score = score_font.render(f"High Score: {self.high_score}", True, (255, 215, 0))
        screen.blit(high_score, (screen.get_width() // 2 - high_score.get_width() // 2, screen.get_height() // 2 + 50))

        restart = score_font.render("Press Y to Restart / N to Quit", True, (200, 200, 200))
        screen.blit(restart, (screen.get_width() // 2 - restart.get_width() // 2, screen.get_height() // 2 + 120))

        pygame.display.flip()

