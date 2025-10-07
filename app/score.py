import pygame
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Score & End Screen")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)

# Fonts
font = pygame.font.SysFont("comicsans", 30)
game_over_font = pygame.font.SysFont("comicsans", 50, bold=True)

# Score variables
score = 0
high_score = 0

def show_score():
    """Display current score and high score."""
    score_text = font.render(f"Score: {score}   High Score: {high_score}", True, BLACK)
    screen.blit(score_text, (10, 10))

def game_over_screen():
    """Display Game Over screen with restart option."""
    global score, high_score

    if score > high_score:
        high_score = score  # update high score

    screen.fill(WHITE)
    over_text = game_over_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, BLACK)
    restart_text = font.render("Press R to Restart or Q to Quit", True, GREEN)

    # Center text
    screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//3))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//1.5))

    pygame.display.update()

    # Wait for restart or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # restart
                    score = 0
                    return  # exit screen, back to game
                if event.key == pygame.K_q:  # quit
                    pygame.quit()
                    sys.exit()

# --- DEMO LOOP (replace with actual snake game logic) ---
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Simulate scoring for demo
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                score += 10
            if event.key == pygame.K_e:  # simulate end game
                game_over_screen()

    show_score()
    pygame.display.update()
    clock.tick(10)

pygame.quit()
