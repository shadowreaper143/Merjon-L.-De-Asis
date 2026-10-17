import pygame
import os


class Player:

    def __init__(
        self,
        screen_width,
        screen_height
    ):

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.width = 80
        self.height = 80

        self.speed = 5

        self.x = (
            screen_width // 2
            - self.width // 2
        )

        self.y = (
            screen_height
            - self.height
            - 40
        )

        self.image = None

        self.load_image()

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def load_image(self):

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        image_path = os.path.join(
            base_dir,
            "assets",
            "images",
            "ship1.png"
        )

        try:

            self.image = pygame.image.load(
                image_path
            ).convert_alpha()

            self.image = pygame.transform.scale(
                self.image,
                (
                    self.width,
                    self.height
                )
            )

        except Exception:

            self.image = pygame.Surface(
                (
                    self.width,
                    self.height
                ),
                pygame.SRCALPHA
            )

            pygame.draw.polygon(
                self.image,
                (0, 220, 255),
                [
                    (40, 0),
                    (5, 70),
                    (25, 60),
                    (40, 80),
                    (55, 60),
                    (75, 70)
                ]
            )

    def move_left(self):

        self.x -= self.speed

        if self.x < 0:

            self.x = 0

        self.rect.x = int(self.x)

    def move_right(self):

        self.x += self.speed

        max_x = (
            self.screen_width
            - self.width
        )

        if self.x > max_x:

            self.x = max_x

        self.rect.x = int(self.x)

    def reset(self):

        self.x = (
            self.screen_width // 2
            - self.width // 2
        )

        self.y = (
            self.screen_height
            - self.height
            - 40
        )

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def update(self):

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(
        self,
        screen
    ):

        if self.image:

            screen.blit(
                self.image,
                self.rect
            )

        else:

            pygame.draw.rect(
                screen,
                (0, 220, 255),
                self.rect
            )