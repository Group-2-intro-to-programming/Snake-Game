import pygame

# Class Variables 
SNAKE_SIZE = 20 # Size of each snake segment
SNAKE_COLOR = (0, 255, 0)  # green 

#Constructors 
class Snake:
    def _init_(self, start_pos=(100, 100)):
        
        # Snake body is a list of (x, y) tuples
        self.body = [start_pos, (start_pos[0] - SNAKE_SIZE, start_pos[1]),
                     (start_pos[0] - 2*SNAKE_SIZE, start_pos[1])]
        self.direction = "RIGHT"  # Initial movement direction
        self.grow_flag = False    # Flag to grow after eating food

#Movement 
    def move(self):
        head_x, head_y = self.body[0]

        if self.direction == "UP":
            head_y -= SNAKE_SIZE
        elif self.direction == "DOWN":
            head_y += SNAKE_SIZE
        elif self.direction == "LEFT":
            head_x -= SNAKE_SIZE
        elif self.direction == "RIGHT":
            head_x += SNAKE_SIZE

        new_head = (head_x, head_y)
        self.body.insert(0, new_head)

        # Remove last segment unless growing
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False
#Growing as it eats 
    def grow(self):
        self.grow_flag = True
#changing direction
    def change_direction(self, new_direction):
        opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        if new_direction != opposites.get(self.direction):
            self.direction = new_direction
#self collision 
    def check_self_collision(self):
        return self.body[0] in self.body[1:]

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, SNAKE_COLOR,
                             (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))
if _name_ == "_main_":
    #Game loop for testing
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()
    snake = Snake()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction("RIGHT")
#Snake Updates
        snake.move()

        # Check for self-collision
        if snake.check_self_collision():
            print("Game Over: Snake hit itself!")
            running = False

        screen.fill((0, 0, 0))  # Clear screen
        snake.draw(screen)
        pygame.display.flip()
        clock.tick(10)  # Control speed

    pygame.quit()