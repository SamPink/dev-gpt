import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
GRAVITY = 0.2
JUMP_STRENGTH = -5

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird Game')

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(100, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

    def jump(self):
        self.velocity = JUMP_STRENGTH

# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((80, HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(midleft=position)

    def update(self):
        self.rect.x -= 3
        if self.rect.right < 0:
            self.kill()

# Game loop
def game_loop():
    bird = Bird()
    bird_group = pygame.sprite.Group()
    bird_group.add(bird)

    pipe_group = pygame.sprite.Group()

    clock = pygame.time.Clock()

    pygame.time.set_timer(pygame.USEREVENT, 1200)

    score = 0
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()
            if event.type == pygame.USEREVENT:
                pipe_group.add(Pipe((WIDTH, random.randint(150, HEIGHT - 150))))

        bird_group.update()
        pipe_group.update()

        if pygame.sprite.spritecollideany(bird, pipe_group) or bird.rect.top < 0 or bird.rect.bottom > HEIGHT:
            running = False
            pygame.time.delay(500)

        score += 0.01

        screen.fill(WHITE)
        bird_group.draw(screen)
        pipe_group.draw(screen)

        text = font.render(str(int(score)), True, BLACK)
        screen.blit(text, (WIDTH // 2, 50))

        pygame.display.flip()
        clock.tick(60)

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_loop()

        screen.fill(WHITE)
        font = pygame.font.Font(None, 36)
        text = font.render("Press Enter to start", True, BLACK)
        screen.blit(text, (WIDTH // 4, HEIGHT // 2 - 50))
        pygame.display.flip()

main()