def game_loop(ai_enabled=False):
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
            if not ai_enabled and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()
            if event.type == pygame.USEREVENT:
                pipe_group.add(Pipe((WIDTH, random.randint(100, HEIGHT - 300))))

        if ai_enabled:
            # AI logic - jump if the bird is about to collide with a pipe
            for pipe in pipe_group:
                if pipe.rect.left < bird.rect.right and pipe.rect.right > bird.rect.left:
                    if pipe.height + PIPE_GAP - bird.rect.y > bird.rect.height // 2:
                        bird.jump()
        
        bird_group.update()
        pipe_group.update()

        if pygame.sprite.spritecollideany(bird, pipe_group, collided=pygame.sprite.collide_mask) or bird.rect.top < 0 or bird.rect.bottom > HEIGHT:
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

    return int(score)
def play_ai_game():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                ai_score = game_loop(ai_enabled=True)
                print(f"AI Score: {ai_score}")
                break

        screen.fill(WHITE)
        font = pygame.font.Font(None, 36)
        text = font.render("Press Enter for AI to play", True, BLACK)
        screen.blit(text, (WIDTH // 4, HEIGHT // 2 - 50))
        pygame.display.flip()
def main():
    human_player = True
    while True:
        if human_player:
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
        else:
            play_ai_game()

        human_player = not human_player

main()