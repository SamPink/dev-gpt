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

# Player
player_size = 50
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - player_size]

# Enemy
enemy_size = 30
enemy_pos = [random.randint(0, SCREEN_WIDTH - enemy_size), 0]

# Speed
SPEED = 10

game_over = False

clock = pygame.time.Clock()

def detect_collision(player_pos, enemy_pos, size):
    px, py = player_pos
    ex, ey = enemy_pos

    if (ex >= px and ex < (px + size)) or (px >= ex and px < (ex + size)):
        if (ey >= py and ey < (py + size)) or (py >= ey and py < (ey + size)):
            return True
    return False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            if event.key == pygame.K_LEFT:
                x -= SPEED
            elif event.key == pygame.K_RIGHT:
                x += SPEED

            player_pos[0] = x

    screen.fill(WHITE)

    if enemy_pos[1] >= 0 and enemy_pos[1] < SCREEN_HEIGHT:
        enemy_pos[1] += SPEED
    else:
        enemy_pos[0] = random.randint(0, SCREEN_WIDTH - enemy_size)
        enemy_pos[1] = 0

    if detect_collision(player_pos, enemy_pos, player_size):
        game_over = True

    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))
    pygame.draw.rect(screen, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

    clock.tick(30)
    pygame.display.update()