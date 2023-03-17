import sys
import pygame
from pygame.locals import *


pygame.init()

# Game dimensions and constants
WIDTH, HEIGHT = 400, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)

# Player properties
player_width, player_height = 40, 40

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump")
clock = pygame.time.Clock()

player = pygame.Rect(WIDTH // 2, HEIGHT // 2, player_width, player_height)

game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        player.x -= 5
        if player.x < 0:
            player.x = 0
    if keys[K_RIGHT]:
        player.x += 5
        if player.x > WIDTH - player_width:
            player.x = WIDTH - player_width

    screen.fill(WHITE)
    pygame.draw.rect(screen, (0, 0, 255), player)
    pygame.display.update()
    clock.tick(FPS)