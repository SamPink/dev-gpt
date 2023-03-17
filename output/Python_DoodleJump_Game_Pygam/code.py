import sys
import pygame
from pygame.locals import *


pygame.init()

# Game dimensions and constants
screen_width, screen_height = 400, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)

# Player properties
player_width, player_height = 40, 40
player_initial_pos = (screen_width // 2, screen_height - player_height * 2)

# Platform properties
platform_width, platform_height = 80, 10

# Doodle Jump logic
class DoodleJump:
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Doodle Jump")
        self.clock = pygame.time.Clock()

        self.player = pygame.Rect(player_initial_pos, (player_width, player_height))
        self.player_speed = 5
        self.player_jump_speed = 8
        self.gravity = 1

        self.platforms = self.generate_platforms()
        self.dy = -self.player_jump_speed

        self.game_running = True

    def generate_platforms(self):
        y_spacing = screen_height // 6
        platforms = []
        for i in range(6):
            x = (pygame.time.get_ticks() // 1000) % 400
            y = i * y_spacing
            platform = pygame.Rect(x, y, platform_width, platform_height)
            platforms.append(platform)
        return platforms

    def check_platform_collision(self):
        for platform in self.platforms:
            if self.player.colliderect(platform) and self.dy > 0:
                self.dy = -self.player_jump_speed

    def game_loop(self):
        while self.game_running:
            self.handle_input()
            self.update()
            self.render()

    def handle_input(self):
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
            self.player.x -= self.player_speed
        if keys[K_RIGHT]:
            self.player.x += self.player_speed

    def update(self):
        self.player.y += int(self.dy)
        self.dy += self.gravity

        if self.player.y < screen_height // 2:
            self.player.y = screen_height // 2
            for platform in self.platforms:
                platform.y += int(self.dy)
                if platform.y > screen_height:
                    platform.y = -(platform_height * 2)
        self.check_platform_collision()

    def render(self):
        self.screen.fill(WHITE)
        pygame.draw.rect(self.screen, (0, 0, 255), self.player)
        for platform in self.platforms:
            pygame.draw.rect(self.screen, (0, 255, 0), platform)
        pygame.display.update()
        self.clock.tick(FPS)

    def run(self):
        self.game_loop()


if __name__ == "__main__":
    game = DoodleJump()
    game.run()