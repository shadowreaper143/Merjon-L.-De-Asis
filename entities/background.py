import pygame
import os


class Background:
    """
    Handles the game background.

    Features:
    - Loads background1.png
    - Automatically scales to the screen
    - Optional scrolling effect
    - Fallback gradient if image is missing
    """

    def __init__(
        self,
        screen_width,
        screen_height,
        image_path=None,
        scroll_speed=0.0
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.scroll_speed = scroll_speed

        self.offset_y = 0.0

        # ============================================
        # DEFAULT IMAGE PATH
        # ============================================

        if image_path is None:
            base_dir = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )

            image_path = os.path.join(
                base_dir,
                "assets",
                "images",
                "background.png"
            )

        self.image_path = image_path

        # ============================================
        # LOAD BACKGROUND
        # ============================================

        self.image = None

        self.load_image()

    # ============================================================
    # LOAD IMAGE
    # ============================================================

    def load_image(self):

        try:

            if os.path.exists(self.image_path):

                image = pygame.image.load(
                    self.image_path
                ).convert()

                self.image = pygame.transform.scale(
                    image,
                    (
                        self.screen_width,
                        self.screen_height
                    )
                )

            else:

                self.image = None

        except pygame.error:

            self.image = None

    # ============================================================
    # UPDATE
    # ============================================================

    def update(self):

        if self.scroll_speed == 0:
            return

        self.offset_y += self.scroll_speed

        if self.offset_y >= self.screen_height:
            self.offset_y = 0

    # ============================================================
    # DRAW
    # ============================================================

    def draw(self, screen):

        # ============================================
        # IMAGE BACKGROUND
        # ============================================

        if self.image is not None:

            if self.scroll_speed == 0:

                screen.blit(
                    self.image,
                    (0, 0)
                )

            else:

                y = int(self.offset_y)

                screen.blit(
                    self.image,
                    (0, y)
                )

                screen.blit(
                    self.image,
                    (
                        0,
                        y - self.screen_height
                    )
                )

        # ============================================
        # FALLBACK
        # ============================================

        else:

            self.draw_fallback(screen)

    # ============================================================
    # FALLBACK BACKGROUND
    # ============================================================

    def draw_fallback(self, screen):

        # Simple dark space background

        screen.fill(
            (8, 10, 25)
        )

        # Stars

        # Use deterministic positions so stars
        # do not randomly change every frame.

        stars = [
            (40, 80, 2),
            (130, 170, 1),
            (220, 90, 2),
            (310, 250, 1),
            (420, 120, 2),
            (520, 300, 1),
            (630, 70, 2),
            (720, 210, 1),
            (820, 130, 2),
            (930, 270, 1),
            (80, 400, 1),
            (180, 520, 2),
            (290, 450, 1),
            (390, 600, 2),
            (500, 500, 1),
            (610, 650, 2),
            (730, 420, 1),
            (840, 550, 2),
            (950, 470, 1),
        ]

        for x, y, size in stars:

            pygame.draw.circle(
                screen,
                (180, 200, 255),
                (x, y),
                size
            )