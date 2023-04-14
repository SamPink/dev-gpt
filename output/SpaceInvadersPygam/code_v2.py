import pygame
import sys
import random

pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Player
player_size = 50
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - player_size]
player_speed = 10

# Enemy
enemy_size = 30
num_enemies = 5
enemy_pos = [[random.randint(0, SCREEN_WIDTH - enemy_size), 0] for _ in range(num_enemies)]
enemy_speed = 3

# Score
score_value = 0
font = pygame.font.Font(None, 32)

def detect_collision(player_pos, enemy_pos, size):
    px, py = player_pos
    ex, ey = enemy_pos

    if (ex >= px and ex < (px + size)) or (px >= ex and px < (ex + size)):
        if (ey >= py and ey < (py + size)) or (py >= ey and py < (ey + size)):
            return True
    return False

def display_score(surface, score):
    score_text = font.render("Score: " + str(score), True, BLACK)
    surface.blit(score_text, (10, 10))

game_over = False

clock = pygame.time.Clock()

level = 1

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            if event.key == pygame.K_LEFT:
                x -= player_speed
            elif event.key == pygame.K_RIGHT:
                x += player_speed

            player_pos[0] = x

    screen.fill(WHITE)

    for index, enemy in enumerate(enemy_pos):
        if enemy[1] >= 0 and enemy[1] < SCREEN_HEIGHT:
            enemy[1] += enemy_speed
        else:
            enemy[0] = random.randint(0, SCREEN_WIDTH - enemy_size)
            enemy[1] = 0
            score_value += 1

        if detect_collision(player_pos, enemy, player_size):
            game_over = True
            break

        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_size, enemy_size))
  
    if score_value > 0 and score_value % num_enemies == 0:
        level += 1
        print("Level Up:", level)
        num_enemies += 2
        enemy_pos = [[random.randint(0, SCREEN_WIDTH - enemy_size), 0] for _ in range(num_enemies)]
        score_value += num_enemies
        enemy_speed += 1

    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))
    display_score(screen, score_value)

    clock.tick(30)
    pygame.display.update()