import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BASE_WIDTH, BASE_HEIGHT = 100, 20
BALL_RADIUS = 15
BOMB_RADIUS = 20
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collect Ball Game")

# base class
class Base:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - BASE_WIDTH // 2, HEIGHT - BASE_HEIGHT - 10, BASE_WIDTH, BASE_HEIGHT)

    def move(self, dx):
        self.rect.x += dx
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WIDTH - BASE_WIDTH:
            self.rect.x = WIDTH - BASE_WIDTH

    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, self.rect)

# Ball class
class Ball:
    def __init__(self):
        self.reset_position()
        self.speed = 5

    def reset_position(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - BALL_RADIUS), 0, BALL_RADIUS, BALL_RADIUS)

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, GREEN, (self.rect.x + BALL_RADIUS // 2, self.rect.y + BALL_RADIUS // 2), BALL_RADIUS)

# Bomb class
class Bomb:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - BOMB_RADIUS), 0, BOMB_RADIUS, BOMB_RADIUS)
        self.speed = 5

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, RED, (self.rect.x + BOMB_RADIUS // 2, self.rect.y + BOMB_RADIUS // 2), BOMB_RADIUS)

# Main game loop
def main():
    clock = pygame.time.Clock()
    base = Base()
    balls = [Ball() for _ in range(5)]  # Start with 5 collectible balls
    bombs = []
    score = 0
    lives = 3
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                base.move(-10)
            if keys[pygame.K_RIGHT]:
                base.move(10)

            for ball in balls:
                ball.move()
                # Check for collision with base
                if base.rect.colliderect(ball.rect):
                    score += 1
                    ball.reset_position()  # Reset ball position to the top

                # Reset ball if it goes off screen
                if ball.rect.y > HEIGHT:
                    ball.reset_position()  # Reset ball position to the top

            # Bomb spawning logic
            if random.randint(1, 100) < 2:  # 2% chance to spawn a bomb
                bombs.append(Bomb())

            for bomb in bombs:
                bomb.move()
                # Check for collision with base
                if base.rect.colliderect(bomb.rect):
                    lives -= 1
                    bombs.remove(bomb)  # Remove bomb after collision

                # Reset bomb if it goes off screen
                if bomb.rect.y > HEIGHT:
                    bombs.remove(bomb)

            # Check for game over
            if lives <= 0:
                game_over = True

            # Drawing
            screen.fill(WHITE)
            base.draw(screen)
            for ball in balls:
                ball.draw(screen)
            for bomb in bombs:
                bomb.draw(screen)

            # Display score and lives
            font = pygame.font.Font(None, 36)
            text = font.render(f'Score: {score} Lives: {lives}', True, BLACK)
            screen.blit(text, (10, 10))

            pygame.display.flip()
            clock.tick(FPS)
        else:
            # Game over screen
            screen.fill(WHITE)
            font = pygame.font.Font(None, 48)
            game_over_text = font.render(f'Game Over! Score: {score}', True, BLACK)
            restart_text = font.render('Press R to Restart', True, BLACK)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 20))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))
            pygame.display.flip()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:  # Restart the game
                main()

    pygame.quit()

if __name__ == "__main__":
    main()
