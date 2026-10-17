import pygame
import random
import os


class Enemy:

    def __init__(
        self,
        screen_width,
        screen_height=None
    ):

        # ============================================
        # SCREEN
        # ============================================

        self.screen_width = screen_width

        if screen_height is None:
            screen_height = 768

        self.screen_height = screen_height

        # ============================================
        # ENEMY SIZE
        # ============================================

        self.width = 70
        self.height = 70

        # ============================================
        # ENEMY SPEED
        # ============================================

        self.speed = 1

        # ============================================
        # RANDOM X POSITION
        # ============================================

        max_x = max(
            0,
            self.screen_width - self.width
        )

        self.x = random.randint(
            0,
            max_x
        )

        # ============================================
        # START ABOVE SCREEN
        # ============================================

        self.y = -self.height

        # ============================================
        # RECTANGLE
        # ============================================

        self.rect = pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height
        )

        # ============================================
        # SHOOTING SETTINGS
        # ============================================

        self.can_shoot = True

        # Individual enemy shooting cooldown
        self.shoot_cooldown = random.randint(
            30,
            120
        )

        self.shoot_delay = random.randint(
            90,
            180
        )

        # ============================================
        # IMAGE
        # ============================================

        self.image = None

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        # Primary image
        image_path = os.path.join(
            base_dir,
            "assets",
            "images",
            "enemyship.png"
        )

        # Alternative image
        alternative_path = os.path.join(
            base_dir,
            "assets",
            "images",
            "enemy1.png"
        )

        try:

            if os.path.exists(image_path):

                self.image = pygame.image.load(
                    image_path
                ).convert_alpha()

            elif os.path.exists(alternative_path):

                self.image = pygame.image.load(
                    alternative_path
                ).convert_alpha()

            if self.image:

                self.image = pygame.transform.scale(
                    self.image,
                    (
                        self.width,
                        self.height
                    )
                )

        except Exception as error:

            print(
                "Enemy image loading error:",
                error
            )

            self.image = None

    # ================================================
    # UPDATE
    # ================================================

    def update(self):

        # --------------------------------------------
        # Move downward
        # --------------------------------------------

        self.y += self.speed

        # --------------------------------------------
        # Update rectangle
        # --------------------------------------------

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # --------------------------------------------
        # Update shooting cooldown
        # --------------------------------------------

        if self.shoot_cooldown > 0:

            self.shoot_cooldown -= 1

    # ================================================
    # CAN SHOOT NOW
    # ================================================

    def ready_to_shoot(self):

        if not self.can_shoot:
            return False

        return self.shoot_cooldown <= 0

    # ================================================
    # RESET SHOOT COOLDOWN
    # ================================================

    def reset_shoot_cooldown(self):

        self.shoot_cooldown = random.randint(
            max(30, self.shoot_delay - 30),
            self.shoot_delay + 30
        )

    # ================================================
    # GET BULLET POSITION
    # ================================================

    def get_bullet_position(self):

        return (
            self.rect.centerx,
            self.rect.bottom - 5
        )

    # ================================================
    # CHECK IF OFF SCREEN
    # ================================================

    def is_off_screen(
        self,
        screen_height=None
    ):

        if screen_height is None:
            screen_height = self.screen_height

        return (
            self.rect.top > screen_height
        )

    # ================================================
    # DRAW
    # ================================================

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

            # ========================================
            # FALLBACK ENEMY SHAPE
            # ========================================

            points = [

                (
                    self.rect.centerx,
                    self.rect.top
                ),

                (
                    self.rect.right,
                    self.rect.bottom
                ),

                (
                    self.rect.centerx,
                    self.rect.bottom - 15
                ),

                (
                    self.rect.left,
                    self.rect.bottom
                )

            ]

            pygame.draw.polygon(
                screen,
                (230, 70, 100),
                points
            )

            # ========================================
            # ENEMY WINDOW
            # ========================================

            pygame.draw.circle(
                screen,
                (255, 220, 100),
                (
                    self.rect.centerx,
                    self.rect.centery
                ),
                7
            )

            # ========================================
            # ENEMY CORE
            # ========================================

            pygame.draw.circle(
                screen,
                (255, 100, 100),
                (
                    self.rect.centerx,
                    self.rect.centery
                ),
                3
            )

    # ================================================
    # COLLISION RECT
    # ================================================

    def get_rect(self):

        return self.rect

    # ================================================
    # CENTER POSITION
    # ================================================

    def get_center(self):

        return (
            self.rect.centerx,
            self.rect.centery
        )

    # ================================================
    # RESET POSITION
    # ================================================

    def reset_position(self):

        max_x = max(
            0,
            self.screen_width - self.width
        )

        self.x = random.randint(
            0,
            max_x
        )

        self.y = -self.height

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        self.shoot_cooldown = random.randint(
            30,
            120
        )

    # ================================================
    # ENABLE SHOOTING
    # ================================================

    def enable_shooting(self):

        self.can_shoot = True

    # ================================================
    # DISABLE SHOOTING
    # ================================================

    def disable_shooting(self):

        self.can_shoot = False

    # ================================================
    # DESTROY / DISABLE
    # ================================================

    def destroy(self):

        self.can_shoot = False

        self.x = -1000
        self.y = -1000

        self.rect.x = -1000
        self.rect.y = -1000