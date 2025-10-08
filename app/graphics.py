# graphics.py - Kimani Roy
# Graphics: Load and render background, snake sprites, food, sounds

import pygame
import os

class Graphics:
    def __init__(self, screen, block_size=20):
        self.screen = screen
        self.block_size = block_size
        
        # Base path for assets
        self.asset_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
        
        # Load images
        self.use_images = self._load_images()
        
        # Check if audio is available first
        self.audio_available = pygame.mixer.get_init() is not None
        
        # Load sounds only if audio is available
        if self.audio_available:
            self.use_sounds = self._load_sounds()
            self._load_background_music()
        else:
            self.use_sounds = False
            print("ℹ Info: Running in silent mode (no audio device)")
    
    def _load_images(self):
        """Load all image assets with error handling"""
        try:
            # Note: Asset names are case-sensitive on Linux
            head_path = os.path.join(self.asset_path, 'SnakeHead.png')
            body_path = os.path.join(self.asset_path, 'snakebody.png')
            
            self.snake_head_img = pygame.image.load(head_path)
            self.snake_body_img = pygame.image.load(body_path)
            
            # Scale images to block size
            self.snake_head_img = pygame.transform.scale(
                self.snake_head_img, (self.block_size, self.block_size)
            )
            self.snake_body_img = pygame.transform.scale(
                self.snake_body_img, (self.block_size, self.block_size)
            )
            
            print("✓ Images loaded successfully")
            return True
        except Exception as e:
            print(f"⚠ Warning: Could not load images - {e}")
            print("  Using colored rectangles instead")
            return False
    
    def _load_sounds(self):
        """Load all sound effects with error handling"""
        try:
            eat_path = os.path.join(self.asset_path, 'eating.mp3')
            scoreup_path = os.path.join(self.asset_path, 'scoreup.mp3')
            crash_path = os.path.join(self.asset_path, 'hitwall.mp3')
            
            self.eat_sound = pygame.mixer.Sound(eat_path)
            self.scoreup_sound = pygame.mixer.Sound(scoreup_path)
            self.crash_sound = pygame.mixer.Sound(crash_path)
            
            # Set volume levels (0.0 to 1.0)
            self.eat_sound.set_volume(0.5)
            self.scoreup_sound.set_volume(0.6)
            self.crash_sound.set_volume(0.7)
            
            print("✓ Sound effects loaded successfully")
            return True
        except Exception as e:
            print(f"⚠ Warning: Could not load sound effects - {e}")
            self.eat_sound = None
            self.scoreup_sound = None
            self.crash_sound = None
            return False
    
    def _load_background_music(self):
        """Load and play background music"""
        try:
            music_path = os.path.join(self.asset_path, 'in-game.mp3')
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)  # Loop indefinitely
            print("✓ Background music loaded and playing")
        except Exception as e:
            print(f"⚠ Warning: Could not load background music - {e}")
    
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
    
    def draw_header(self, player_name, score, high_score):
        """Draw header with player name, score, and high score"""
        header_bg = (10, 20, 10)
        pygame.draw.rect(self.screen, header_bg, (0, 0, self.screen.get_width(), 60))
        
        font = pygame.font.Font(None, 32)
        
        # Player name (left)
        name_text = font.render(f"Player: {player_name}", True, (255, 255, 255))
        self.screen.blit(name_text, (10, 15))
        
        # Score (center)
        score_text = font.render(f"Score: {score}", True, (0, 255, 0))
        score_rect = score_text.get_rect(center=(self.screen.get_width()//2, 30))
        self.screen.blit(score_text, score_rect)
        
        # High score (right)
        high_text = font.render(f"High: {high_score}", True, (255, 215, 0))
        self.screen.blit(high_text, (self.screen.get_width() - high_text.get_width() - 10, 15))
    
    def draw_footer(self, level, obstacles):
        """Draw footer with level and obstacles"""
        footer_bg = (10, 20, 10)
        footer_y = self.screen.get_height() - 60
        pygame.draw.rect(self.screen, footer_bg, (0, footer_y, self.screen.get_width(), 60))
        
        font = pygame.font.Font(None, 32)
        
        # Level (left)
        level_text = font.render(f"Level: {level}", True, (0, 255, 255))
        self.screen.blit(level_text, (10, footer_y + 15))
        
        # Obstacles (right)
        if obstacles > 0:
            obs_text = font.render(f"Obstacles: {obstacles}", True, (255, 165, 0))
            self.screen.blit(obs_text, (self.screen.get_width() - obs_text.get_width() - 10, footer_y + 15))
    
    def draw_snake_head(self, x, y, direction):
        """Draw snake head, rotated based on direction"""
        if self.use_images:
            # Rotate head based on direction
            rotation_map = {
                "UP": 90,
                "DOWN": -90,
                "LEFT": 180,
                "RIGHT": 0
            }
            angle = rotation_map.get(direction, 0)
            rotated = pygame.transform.rotate(self.snake_head_img, angle)
            self.screen.blit(rotated, (x, y))
        else:
            # Fallback: green rectangle with border
            pygame.draw.rect(self.screen, (0, 255, 0), 
                           (x, y, self.block_size, self.block_size))
            pygame.draw.rect(self.screen, (0, 200, 0), 
                           (x, y, self.block_size, self.block_size), 2)
    
    def draw_snake_body(self, body_positions):
        """Draw all snake body segments"""
        for pos in body_positions:
            if self.use_images:
                self.screen.blit(self.snake_body_img, (pos[0], pos[1]))
            else:
                # Fallback: green rectangle with border
                pygame.draw.rect(self.screen, (0, 200, 0), 
                               (pos[0], pos[1], self.block_size, self.block_size))
                pygame.draw.rect(self.screen, (0, 150, 0), 
                               (pos[0], pos[1], self.block_size, self.block_size), 2)
    
    def draw_food(self, x, y):
        """Draw food/apple"""
        # Draw red apple (no asset file provided, so using graphics)
        pygame.draw.circle(self.screen, (220, 20, 20), 
                          (x + self.block_size // 2, y + self.block_size // 2), 
                          self.block_size // 2)
        # Add highlight for 3D effect
        pygame.draw.circle(self.screen, (255, 100, 100), 
                          (x + self.block_size // 2 - 3, y + self.block_size // 2 - 3), 
                          self.block_size // 6)
    
    def play_eat_sound(self):
        """Play sound when snake eats food"""
        if self.audio_available and self.use_sounds and self.eat_sound:
            try:
                self.eat_sound.play()
            except:
                pass
    
    def play_scoreup_sound(self):
        """Play sound when score increases significantly"""
        if self.audio_available and self.use_sounds and self.scoreup_sound:
            try:
                self.scoreup_sound.play()
            except:
                pass
    
    def play_crash_sound(self):
        """Play sound when game is over"""
        if self.audio_available and self.use_sounds and self.crash_sound:
            try:
                # Stop background music when game ends
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                self.crash_sound.play()
            except:
                pass
    
    def play_gameover_music(self):
        """Play game over music"""
        if not self.audio_available:
            return
        try:
            gameover_path = os.path.join(self.asset_path, 'GameOver.mp3')
            pygame.mixer.music.load(gameover_path)
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play()
        except Exception as e:
            pass  # Silently fail if game over music can't load
    
    def restart_background_music(self):
        """Restart background music for new game"""
        if not self.audio_available:
            return
        try:
            music_path = os.path.join(self.asset_path, 'in-game.mp3')
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except:
            pass
    
    def draw_obstacles(self, obstacle_positions):
        """Draw all obstacles with 3D stone effect"""
        for pos in obstacle_positions:
            # Main stone block
            pygame.draw.rect(self.screen, (128, 128, 128), 
                           (pos[0], pos[1], self.block_size, self.block_size))
            # Highlight (top-left)
            pygame.draw.rect(self.screen, (160, 160, 160), 
                           (pos[0], pos[1], self.block_size, self.block_size // 4))
            # Shadow (bottom-right border)
            pygame.draw.rect(self.screen, (80, 80, 80), 
                           (pos[0], pos[1], self.block_size, self.block_size), 2)