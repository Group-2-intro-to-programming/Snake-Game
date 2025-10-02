# input_handler.py
# Pascal Ng’ang’a

import pygame

# define the direction
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class InputHandler:
    definite(self):
        self.direction = RIGHT  # default start direction

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.direction != DOWN:
            self.direction = UP
        elif keys[pygame.K_DOWN] and self.direction != UP:
            self.direction = DOWN
        elif keys[pygame.K_LEFT] and self.direction != RIGHT:
            self.direction = LEFT
        elif keys[pygame.K_RIGHT] and self.direction != LEFT:
            self.direction = RIGHT

        return self.direction

from input_handler import InputHandler

pygame.init()
clock = pygame.time.Clock()

input_handler = InputHandler()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    direction = input_handler.handle_input()
    print(direction)  # replace with snake movement logic

    clock.tick(10)

pygame.quit()

