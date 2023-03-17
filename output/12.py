def main():
    doodler_x = WINDOW_WIDTH // 2
    doodler_y = WINDOW_HEIGHT // 2
    doodler = Doodler(doodler_x, doodler_y)

    platforms = [Platform(random.randint(25, WINDOW_WIDTH - 125), random.randint(25, WINDOW_HEIGHT)) for _ in range(10)]

    # ...rest of the code remains the same