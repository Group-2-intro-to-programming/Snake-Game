import pygame

class Graphics:
    def __init__(self, screen):
        self.screen = screen

        # Load images
        self.background = pygame.image.load("Assets/background.png")
        self.snake_head = pygame.image.load("Assets/snake_head.png")
        self.snake_body = pygame.image.load("Assets/snake_body.png")
        self.snake_tail = pygame.image.load("Assets/snake_tail.png")
        self.food = pygame.image.load("Assets/food.png")

        # Load sounds
        self.eat_sound = pygame.mixer.Sound("Assets/eat.wav")
        self.crash_sound = pygame.mixer.Sound("Assets/crash.wav")

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def draw_food(self, x, y):
        self.screen.blit(self.food, (x, y))

    def draw_snake_head(self, x, y, direction):
        """Rotate snake head based on direction"""
        if direction == "UP":
            rotated = pygame.transform.rotate(self.snake_head, 90)
        elif direction == "DOWN":
            rotated = pygame.transform.rotate(self.snake_head, -90)
        elif direction == "LEFT":
            rotated = pygame.transform.rotate(self.snake_head, 180)
        else:  # RIGHT
            rotated = self.snake_head

        self.screen.blit(rotated, (x, y))

    def draw_snake_body(self, body_positions):
        """body_positions = list of (x, y)"""
        for pos in body_positions:
            self.screen.blit(self.snake_body, pos)

    def draw_snake_tail(self, x, y):
        self.screen.blit(self.snake_tail, (x, y))

    def play_eat_sound(self):
        self.eat_sound.play()

    def play_crash_sound(self):
        self.crash_sound.play()
