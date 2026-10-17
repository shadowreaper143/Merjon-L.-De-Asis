import pygame

from managers.game_manager import GameManager


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768


def main():

    pygame.init()

    try:
        pygame.mixer.init()
    except pygame.error:
        pass

    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    pygame.display.set_caption(
        "Space Invaders"
    )

    clock = pygame.time.Clock()

    game_manager = GameManager(
        screen,
        SCREEN_WIDTH,
        SCREEN_HEIGHT
    )

    running = True

    while running:

        events = pygame.event.get()

        for event in events:

            if event.type == pygame.QUIT:
                running = False

        game_manager.handle_events(events)

        game_manager.update()

        game_manager.draw()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()