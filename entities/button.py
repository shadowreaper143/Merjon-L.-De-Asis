import pygame


class MobileButtons:

    def __init__(
        self,
        screen_width,
        screen_height
    ):

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.enabled = True

        self.button_size = 85
        self.margin = 25

        # LEFT
        self.left_button = pygame.Rect(
            self.margin,
            screen_height - self.button_size - self.margin,
            self.button_size,
            self.button_size
        )

        # RIGHT
        self.right_button = pygame.Rect(
            self.margin + self.button_size + 15,
            screen_height - self.button_size - self.margin,
            self.button_size,
            self.button_size
        )

        # FIRE
        self.fire_button = pygame.Rect(
            screen_width - self.button_size - self.margin,
            screen_height - self.button_size - self.margin,
            self.button_size,
            self.button_size
        )

        self.left_pressed = False
        self.right_pressed = False
        self.fire_pressed = False

    # ==================================================
    # ENABLE / DISABLE
    # ==================================================

    def set_enabled(
        self,
        enabled
    ):

        self.enabled = bool(enabled)

        if not self.enabled:

            self.left_pressed = False
            self.right_pressed = False
            self.fire_pressed = False

    def is_enabled(self):

        return self.enabled

    # ==================================================
    # HANDLE MOUSE
    # ==================================================

    def handle_mouse(
        self,
        player,
        events
    ):

        if not self.enabled:

            return False

        movement_changed = False

        mouse_buttons = pygame.mouse.get_pressed()

        mouse_pos = pygame.mouse.get_pos()

        self.left_pressed = (
            mouse_buttons[0]
            and self.left_button.collidepoint(
                mouse_pos
            )
        )

        self.right_pressed = (
            mouse_buttons[0]
            and self.right_button.collidepoint(
                mouse_pos
            )
        )

        self.fire_pressed = (
            mouse_buttons[0]
            and self.fire_button.collidepoint(
                mouse_pos
            )
        )

        if self.left_pressed:

            player.move_left()

            movement_changed = True

        if self.right_pressed:

            player.move_right()

            movement_changed = True

        return movement_changed

    # ==================================================
    # DRAW
    # ==================================================

    def draw(
        self,
        screen
    ):

        if not self.enabled:

            return

        # LEFT
        pygame.draw.rect(
            screen,
            (60, 120, 220),
            self.left_button,
            border_radius=18
        )

        pygame.draw.rect(
            screen,
            (220, 230, 255),
            self.left_button,
            2,
            border_radius=18
        )

        # RIGHT
        pygame.draw.rect(
            screen,
            (60, 120, 220),
            self.right_button,
            border_radius=18
        )

        pygame.draw.rect(
            screen,
            (220, 230, 255),
            self.right_button,
            2,
            border_radius=18
        )

        # FIRE
        pygame.draw.rect(
            screen,
            (230, 70, 90),
            self.fire_button,
            border_radius=18
        )

        pygame.draw.rect(
            screen,
            (255, 230, 230),
            self.fire_button,
            2,
            border_radius=18
        )

        font = pygame.font.SysFont(
            "arial",
            26,
            bold=True
        )

        left_text = font.render(
            "<",
            True,
            (255, 255, 255)
        )

        right_text = font.render(
            ">",
            True,
            (255, 255, 255)
        )

        fire_text = font.render(
            "FIRE",
            True,
            (255, 255, 255)
        )

        screen.blit(
            left_text,
            left_text.get_rect(
                center=self.left_button.center
            )
        )

        screen.blit(
            right_text,
            right_text.get_rect(
                center=self.right_button.center
            )
        )

        screen.blit(
            fire_text,
            fire_text.get_rect(
                center=self.fire_button.center
            )
        )