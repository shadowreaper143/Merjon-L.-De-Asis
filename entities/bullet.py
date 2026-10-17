import pygame
import os


class Bullet:
    """Fast reusable player projectile.

    The projectile image is loaded and scaled only once for the whole
    class instead of once for every bullet. This prevents Twin Shot
    from causing disk I/O and image scaling during rapid fire.
    """

    _shared_image = None
    _image_loaded = False

    def __init__(self, x, y):
        self.width = 20
        self.height = 40
        self.speed = 10

        self.x = x - self.width // 2
        self.y = y - self.height

        self._ensure_shared_image()
        self.image = Bullet._shared_image

        self.rect = pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height
        )

    @classmethod
    def _ensure_shared_image(cls):
        if cls._image_loaded:
            return

        cls._image_loaded = True

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        image_path = os.path.join(
            base_dir,
            "assets",
            "images",
            "projectile.png"
        )

        try:
            image = pygame.image.load(image_path)

            # convert_alpha() is faster to blit when a display is active.
            if pygame.display.get_surface() is not None:
                image = image.convert_alpha()

            cls._shared_image = pygame.transform.scale(
                image,
                (20, 40)
            )

        except Exception:
            fallback = pygame.Surface(
                (20, 40),
                pygame.SRCALPHA
            )

            pygame.draw.rect(
                fallback,
                (255, 255, 0),
                (7, 0, 6, 40)
            )

            cls._shared_image = fallback

    def update(self):
        self.y -= self.speed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def is_off_screen(self):
        return self.rect.bottom < 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)
