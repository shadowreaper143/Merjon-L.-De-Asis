import pygame
import random
import os

from entities.player import Player
from entities.enemy import Enemy
from entities.bullet import Bullet
from entities.background import Background

from managers.database import DatabaseManager
from config.settings_manager import load_settings, save_settings


class EnemyBullet:
    """Projectile fired by enemies."""

    def __init__(self, x, y, speed=6, horizontal_speed=0):
        self.width = 12
        self.height = 30
        self.speed = speed
        self.horizontal_speed = horizontal_speed

        self.x = x - self.width // 2
        self.y = y

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def update(self):
        self.x += self.horizontal_speed
        self.y += self.speed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def is_off_screen(self, screen_height):
        return self.y > screen_height or self.x < -self.width or self.x > 2000

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (255, 100, 100),
            self.rect,
            border_radius=5
        )


class SpaceBoss:
    """Stage 10 boss: stays at the top, moves horizontally and shoots."""

    def __init__(self, screen_width, screen_height, hp=120):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width = 190
        self.height = 100
        self.x = (screen_width - self.width) / 2
        self.y = 80
        self.speed = 3.2
        self.direction = 1
        self.max_hp = hp
        self.hp = hp
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def update(self):
        self.x += self.speed * self.direction
        if self.x <= 20:
            self.x = 20
            self.direction = 1
        if self.x + self.width >= self.screen_width - 20:
            self.x = self.screen_width - self.width - 20
            self.direction = -1
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def is_dead(self):
        return self.hp <= 0

    def draw(self, screen):
        pygame.draw.rect(screen, (120, 40, 170), self.rect.inflate(18, 18), width=3, border_radius=18)
        pygame.draw.polygon(screen, (150, 45, 170), [
            (self.rect.centerx, self.rect.top),
            (self.rect.right, self.rect.top + 35),
            (self.rect.right - 20, self.rect.bottom - 5),
            (self.rect.centerx, self.rect.bottom - 22),
            (self.rect.left + 20, self.rect.bottom - 5),
            (self.rect.left, self.rect.top + 35),
        ])
        pygame.draw.polygon(screen, (60, 25, 90), [
            (self.rect.centerx, self.rect.top + 15),
            (self.rect.centerx + 55, self.rect.top + 43),
            (self.rect.centerx + 25, self.rect.bottom - 20),
            (self.rect.centerx - 25, self.rect.bottom - 20),
            (self.rect.centerx - 55, self.rect.top + 43),
        ])
        pygame.draw.circle(screen, (255, 80, 120), self.rect.center, 17)
        pygame.draw.circle(screen, (255, 220, 90), self.rect.center, 8)
        pygame.draw.rect(screen, (220, 100, 220), (self.rect.left + 20, self.rect.bottom - 20, 22, 18), border_radius=4)
        pygame.draw.rect(screen, (220, 100, 220), (self.rect.right - 42, self.rect.bottom - 20, 22, 18), border_radius=4)

        bar_x = self.rect.x
        bar_y = self.rect.y - 25
        pygame.draw.rect(screen, (65, 65, 85), (bar_x, bar_y, self.width, 12), border_radius=6)
        hp_width = int(self.width * (self.hp / self.max_hp))
        if hp_width > 0:
            pygame.draw.rect(screen, (255, 70, 100), (bar_x, bar_y, hp_width, 12), border_radius=6)


class MiniBoss:
    """Mini boss that appears on every 5th stage except the main Stage 10 boss."""

    def __init__(self, screen_width, screen_height, hp=65):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width = 145
        self.height = 78
        self.x = (screen_width - self.width) / 2
        self.y = 95
        self.speed = 4.2
        self.direction = 1
        self.max_hp = hp
        self.hp = hp
        self.fire_delay = 55
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def update(self):
        self.x += self.speed * self.direction
        if self.x <= 20:
            self.x = 20
            self.direction = 1
        if self.x + self.width >= self.screen_width - 20:
            self.x = self.screen_width - self.width - 20
            self.direction = -1
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def is_dead(self):
        return self.hp <= 0

    def draw(self, screen):
        # Mini boss body
        pygame.draw.rect(
            screen, (35, 100, 190), self.rect.inflate(12, 12),
            width=3, border_radius=14
        )
        pygame.draw.polygon(screen, (55, 145, 235), [
            (self.rect.centerx, self.rect.top),
            (self.rect.right, self.rect.top + 25),
            (self.rect.right - 15, self.rect.bottom - 5),
            (self.rect.centerx, self.rect.bottom - 17),
            (self.rect.left + 15, self.rect.bottom - 5),
            (self.rect.left, self.rect.top + 25),
        ])
        pygame.draw.polygon(screen, (20, 45, 95), [
            (self.rect.centerx, self.rect.top + 12),
            (self.rect.centerx + 38, self.rect.top + 32),
            (self.rect.centerx + 18, self.rect.bottom - 16),
            (self.rect.centerx - 18, self.rect.bottom - 16),
            (self.rect.centerx - 38, self.rect.top + 32),
        ])
        pygame.draw.circle(screen, (90, 240, 255), self.rect.center, 11)
        pygame.draw.circle(screen, (255, 230, 100), self.rect.center, 5)

        # HP bar
        bar_x = self.rect.x
        bar_y = self.rect.y - 20
        pygame.draw.rect(screen, (65, 65, 85), (bar_x, bar_y, self.width, 10), border_radius=5)
        hp_width = int(self.width * (self.hp / self.max_hp))
        if hp_width > 0:
            pygame.draw.rect(screen, (90, 190, 255), (bar_x, bar_y, hp_width, 10), border_radius=5)


class GameManager:

    def __init__(
        self,
        screen,
        screen_width,
        screen_height
    ):

        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        # ==================================================
        # BACKGROUND
        # ==================================================

        self.background = Background(
            self.screen_width,
            self.screen_height,
            scroll_speed=0.15
        )

        # ==================================================
        # COLORS
        # ==================================================

        self.bg_color = (12, 15, 30)
        self.panel_color = (25, 30, 55)
        self.panel2_color = (35, 40, 70)

        self.white = (245, 245, 255)
        self.gray = (170, 175, 195)
        self.dark_gray = (80, 85, 105)

        self.blue = (90, 170, 255)
        self.cyan = (80, 230, 255)
        self.green = (90, 220, 140)
        self.red = (240, 90, 110)
        self.yellow = (255, 215, 80)
        self.orange = (255, 160, 80)

        # ==================================================
        # FONTS
        # ==================================================

        self.font_small = pygame.font.SysFont(
            "arial",
            20
        )

        self.font = pygame.font.SysFont(
            "arial",
            26
        )

        self.font_medium = pygame.font.SysFont(
            "arial",
            32,
            bold=True
        )

        self.font_large = pygame.font.SysFont(
            "arial",
            50,
            bold=True
        )

        self.font_title = pygame.font.SysFont(
            "arial",
            64,
            bold=True
        )

        # ==================================================
        # SETTINGS
        # ==================================================

        self.settings = load_settings()

        self.volume = float(
            self.settings.get(
                "sound",
                {}
            ).get(
                "volume",
                0.7
            )
        )

        self.volume = max(
            0.0,
            min(1.0, self.volume)
        )

        self.mobile_controls = bool(
            self.settings.get("controls", {}).get("mobile", True)
        )
        self.mobile_left_rect = pygame.Rect(40, self.screen_height - 150, 90, 90)
        self.mobile_right_rect = pygame.Rect(145, self.screen_height - 150, 90, 90)
        self.mobile_fire_rect = pygame.Rect(self.screen_width - 150, self.screen_height - 150, 110, 90)
        self.mobile_toggle_rect = pygame.Rect(442, 530, 140, 52)

        # ==================================================
        # DATABASE
        # ==================================================

        self.database = DatabaseManager()

        # ==================================================
        # GAME STATE
        # ==================================================

        self.game_state = "auth"

        # auth:
        # login / register
        #
        # start:
        # start game screen
        #
        # playing:
        # gameplay
        #
        # game_over:
        # game over screen
        #
        # leaderboard:
        # leaderboard
        #
        # settings:
        # settings screen

        self.register_mode = False

        # ==================================================
        # AUTH DATA
        # ==================================================

        self.username = ""
        self.password = ""

        self.active_field = "username"

        self.show_password = False

        self.auth_message = ""
        self.auth_message_color = self.red

        self.current_player = None
        self.current_player_id = None

        # ==================================================
        # AUTH RECTANGLES
        # ==================================================

        self.username_rect = pygame.Rect(
            300,
            255,
            424,
            55
        )

        self.password_rect = pygame.Rect(
            300,
            330,
            424,
            55
        )

        self.auth_button_rect = pygame.Rect(
            300,
            415,
            424,
            58
        )

        self.switch_button_rect = pygame.Rect(
            300,
            490,
            424,
            48
        )

        # ==================================================
        # START SCREEN
        # ==================================================

        self.start_button_rect = pygame.Rect(
            312,
            390,
            400,
            70
        )

        self.start_leaderboard_rect = pygame.Rect(
            312,
            485,
            400,
            55
        )

        self.start_logout_rect = pygame.Rect(
            312,
            560,
            400,
            55
        )

        # ==================================================
        # GAME OVER
        # ==================================================

        self.play_again_rect = pygame.Rect(
            312,
            380,
            400,
            60
        )

        self.game_leaderboard_rect = pygame.Rect(
            312,
            455,
            400,
            55
        )

        self.game_logout_rect = pygame.Rect(
            312,
            525,
            400,
            55
        )

        # ==================================================
        # SETTINGS
        # ==================================================

        self.settings_back_rect = pygame.Rect(
            312,
            650,
            400,
            55
        )

        self.volume_minus_rect = pygame.Rect(
            370,
            255,
            70,
            55
        )

        self.volume_plus_rect = pygame.Rect(
            584,
            255,
            70,
            55
        )

        # ==================================================
        # BUFF CARD BUTTONS
        # ==================================================

        self.buff_card_rects = [
            pygame.Rect(65, 260, 275, 300),
            pygame.Rect(374, 260, 275, 300),
            pygame.Rect(683, 260, 275, 300),
        ]

        # ==================================================
        # GAME VARIABLES
        # ==================================================

        self.player = None

        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []

        self.score = 0

        # ==================================================
        # STAGES / LIVES
        # ==================================================

        self.stage = 1
        self.hearts = 3
        self.max_hearts = 3
        self.enemies_defeated = 0
        self.stage_target = 10
        self.damage_cooldown = 0
        self.stage_message_timer = 0

        # ==================================================
        # BOSS SYSTEM
        # ==================================================

        self.boss = None
        self.boss_type = None
        self.boss_fire_timer = 0
        self.boss_fire_delay = 42
        self.boss_stage = 10
        self.mini_boss_stage_interval = 5
        self.boss_type = None

        # ==================================================
        # BUFF CARD SYSTEM
        # ==================================================

        self.buff_cards = []
        self.buff_levels = {
            "rapid_fire": 0,
            "twin_shot": 0,
            "speed": 0,
            "shield": 0,
            "heart": 0,
            "power": 0,
        }
        self.twin_shot = False
        self.shield_charges = 0
        self.player_power = 1

        self.enemy_spawn_timer = 0
        self.enemy_fire_timer = 0

        self.enemy_spawn_delay = 60
        self.enemy_fire_delay = 45

        self.max_enemies = 5

        # Continuous player firing
        self.fire_cooldown = 0
        self.fire_delay = 10
        self.max_player_bullets = 18
        self.max_enemy_bullets = 12
        self.shoot_sound_cooldown = 0
        self.explosion_sound_cooldown = 0

        # ==================================================
        # GAME OVER
        # ==================================================

        self.score_saved = False

        # ==================================================
        # SETTINGS / SOUNDS
        # ==================================================

        self.shoot_sound = None
        self.explosion_sound = None

        self.load_sounds()

        # Start with auth screen
        self.reset_auth()

    # ======================================================
    # SOUND
    # ======================================================

    def load_sounds(self):

        try:
            shoot_path = os.path.join(
                "assets",
                "sounds",
                "shoot.wav"
            )

            explosion_path = os.path.join(
                "assets",
                "sounds",
                "explosion.wav"
            )

            if os.path.exists(shoot_path):
                self.shoot_sound = pygame.mixer.Sound(
                    shoot_path
                )

            if os.path.exists(explosion_path):
                self.explosion_sound = pygame.mixer.Sound(
                    explosion_path
                )

            self.apply_volume()

        except Exception:
            self.shoot_sound = None
            self.explosion_sound = None

    def apply_volume(self):

        if self.shoot_sound:
            self.shoot_sound.set_volume(
                self.volume
            )

        if self.explosion_sound:
            self.explosion_sound.set_volume(
                self.volume
            )

    def play_shoot_sound(self):

        if self.shoot_sound and self.shoot_sound_cooldown <= 0:
            try:
                self.shoot_sound.play()
                self.shoot_sound_cooldown = 3
            except Exception:
                pass

    def play_explosion_sound(self):

        if self.explosion_sound and self.explosion_sound_cooldown <= 0:
            try:
                self.explosion_sound.play()
                self.explosion_sound_cooldown = 2
            except Exception:
                pass

    # ======================================================
    # AUTH RESET
    # ======================================================

    def reset_auth(self):

        self.username = ""
        self.password = ""

        self.active_field = "username"

        self.show_password = False

        self.auth_message = ""

    # ======================================================
    # START GAME
    # ======================================================

    def start_game(self):

        self.reset_game()
        self.prepare_buff_selection()
        self.game_state = "buff_select"

    # ======================================================
    # RESET GAME
    # ======================================================

    def reset_game(self):

        self.player = Player(
            self.screen_width,
            self.screen_height
        )

        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []

        self.score = 0

        # Reset stage and lives every new game
        self.stage = 1
        self.hearts = self.max_hearts
        self.enemies_defeated = 0
        self.stage_target = 10
        self.damage_cooldown = 0
        self.stage_message_timer = 120

        self.enemy_spawn_timer = 0
        self.enemy_fire_timer = 0

        self.fire_cooldown = 0
        self.shoot_sound_cooldown = 0
        self.explosion_sound_cooldown = 0

        self.score_saved = False
        self.boss = None
        self.boss_fire_timer = 0
        self.buff_cards = []
        self.buff_levels = {
            "rapid_fire": 0,
            "twin_shot": 0,
            "speed": 0,
            "shield": 0,
            "heart": 0,
            "power": 0,
        }
        self.twin_shot = False
        self.shield_charges = 0
        self.player_power = 1

    # ======================================================
    # EVENT HANDLER
    # ======================================================

    def handle_events(self, events):

        for event in events:

            # ------------------------------------------------
            # AUTH
            # ------------------------------------------------

            if self.game_state == "auth":
                self.handle_auth_events(event)

            # ------------------------------------------------
            # START
            # ------------------------------------------------

            elif self.game_state == "start":
                self.handle_start_events(event)

            # ------------------------------------------------
            # PLAYING
            # ------------------------------------------------

            elif self.game_state == "playing":
                self.handle_game_events(event)

            # ------------------------------------------------
            # BUFF SELECTION
            # ------------------------------------------------

            elif self.game_state == "buff_select":
                self.handle_buff_events(event)

            # ------------------------------------------------
            # GAME OVER
            # ------------------------------------------------

            elif self.game_state == "game_over":
                self.handle_game_over_events(event)

            # ------------------------------------------------
            # LEADERBOARD
            # ------------------------------------------------

            elif self.game_state == "leaderboard":
                self.handle_leaderboard_events(event)

            # ------------------------------------------------
            # SETTINGS
            # ------------------------------------------------

            elif self.game_state == "settings":
                self.handle_settings_events(event)

    # ======================================================
    # AUTH EVENTS
    # ======================================================

    def handle_auth_events(self, event):

        # ==================================================
        # MOUSE CLICK
        # ==================================================

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button != 1:
                return

            mouse_pos = event.pos

            # ----------------------------------------------
            # USERNAME
            # ----------------------------------------------

            if self.username_rect.collidepoint(
                mouse_pos
            ):

                self.active_field = "username"

                return

            # ----------------------------------------------
            # PASSWORD
            # ----------------------------------------------

            if self.password_rect.collidepoint(
                mouse_pos
            ):

                # THIS IS THE IMPORTANT FIX
                self.active_field = "password"

                return

            # ----------------------------------------------
            # LOGIN / REGISTER BUTTON
            # ----------------------------------------------

            if self.auth_button_rect.collidepoint(
                mouse_pos
            ):

                self.process_auth()

                return

            # ----------------------------------------------
            # SWITCH LOGIN / REGISTER
            # ----------------------------------------------

            if self.switch_button_rect.collidepoint(
                mouse_pos
            ):

                self.register_mode = (
                    not self.register_mode
                )

                self.active_field = "username"

                self.auth_message = ""

                return

        # ==================================================
        # KEYBOARD
        # ==================================================

        if event.type != pygame.KEYDOWN:
            return

        # --------------------------------------------------
        # F2 = SHOW / HIDE PASSWORD
        # --------------------------------------------------

        if event.key == pygame.K_F2:

            self.show_password = (
                not self.show_password
            )

            return

        # --------------------------------------------------
        # TAB
        # --------------------------------------------------

        if event.key == pygame.K_TAB:

            if self.register_mode:

                fields = [
                    "username",
                    "password"
                ]

            else:

                fields = [
                    "username",
                    "password"
                ]

            if self.active_field not in fields:

                self.active_field = fields[0]

            else:

                index = fields.index(
                    self.active_field
                )

                index += 1

                if index >= len(fields):
                    index = 0

                self.active_field = fields[index]

            return

        # --------------------------------------------------
        # ENTER
        # --------------------------------------------------

        if event.key == pygame.K_RETURN:

            self.process_auth()

            return

        # --------------------------------------------------
        # BACKSPACE
        # --------------------------------------------------

        if event.key == pygame.K_BACKSPACE:

            if self.active_field == "username":

                self.username = (
                    self.username[:-1]
                )

            elif self.active_field == "password":

                self.password = (
                    self.password[:-1]
                )

            return

        # --------------------------------------------------
        # ESC
        # --------------------------------------------------

        if event.key == pygame.K_ESCAPE:

            self.active_field = None

            return

        # --------------------------------------------------
        # TYPING
        # --------------------------------------------------

        if event.unicode:

            character = event.unicode

            if not character.isprintable():
                return

            # USERNAME
            if self.active_field == "username":

                if len(self.username) < 30:

                    self.username += character

            # PASSWORD
            elif self.active_field == "password":

                if len(self.password) < 50:

                    self.password += character

    # ======================================================
    # PROCESS LOGIN / REGISTER
    # ======================================================

    def process_auth(self):

        username = self.username.strip()
        password = self.password

        # ==================================================
        # REGISTER
        # ==================================================

        if self.register_mode:

            if len(username) < 3:

                self.auth_message = (
                    "Username must be at least 3 characters."
                )

                self.auth_message_color = self.red

                return

            if len(password) < 6:

                self.auth_message = (
                    "Password must be at least 4 characters."
                )

                self.auth_message_color = self.red

                return

            try:

                success, result = (
                    self.database.register_player(
                        username,
                        password
                    )
                )

                if success:

                    # --------------------------------------------------
                    # DEMO / SCHOOL DATABASE PASSWORD COLUMN
                    # --------------------------------------------------
                    # The normal password_hash is still used for login.
                    # This additionally writes the typed password to a
                    # separate `password` column so it can be viewed in
                    # phpMyAdmin. Plaintext password storage is insecure
                    # and should only be used for a local school demo.
                    self.save_demo_password(username, password)

                    self.current_player_id = result

                    self.current_player = {
                        "id": result,
                        "username": username
                    }

                    self.auth_message = (
                        "Registration successful!"
                    )

                    self.auth_message_color = (
                        self.green
                    )

                    self.game_state = "start"

                else:

                    self.auth_message = str(
                        result
                    )

                    self.auth_message_color = (
                        self.red
                    )

            except Exception as e:

                self.auth_message = (
                    "Registration error: "
                    + str(e)
                )

                self.auth_message_color = (
                    self.red
                )

            return

        # ==================================================
        # LOGIN
        # ==================================================

        if len(username) == 0:

            self.auth_message = (
                "Please enter your username."
            )

            self.auth_message_color = (
                self.red
            )

            return

        if len(password) == 0:

            self.auth_message = (
                "Please enter your password."
            )

            self.auth_message_color = (
                self.red
            )

            return

        try:

            player = (
                self.database.authenticate_player(
                    username,
                    password
                )
            )

            if player:

                self.current_player = player

                self.current_player_id = (
                    player.get("id")
                )

                self.username = player.get(
                    "username",
                    username
                )

                self.auth_message = (
                    "Login successful!"
                )

                self.auth_message_color = (
                    self.green
                )

                self.game_state = "start"

            else:

                self.auth_message = (
                    "Invalid username or password."
                )

                self.auth_message_color = (
                    self.red
                )

        except Exception as e:

            self.auth_message = (
                "Login error: "
                + str(e)
            )

            self.auth_message_color = (
                self.red
            )

    # ======================================================
    # SAVE DEMO PASSWORD
    # ======================================================

    def save_demo_password(self, username, password):
        """
        Creates/updates a plaintext password column for a local
        school/demo database.

        IMPORTANT: password_hash remains the real authentication
        value. Plaintext passwords are not recommended for production.
        """

        connection = None
        cursor = None

        try:
            connection = self.database.connect()
            cursor = connection.cursor()

            # Add a visible password column if it does not exist.
            try:
                cursor.execute(
                    """
                    ALTER TABLE players
                    ADD COLUMN password VARCHAR(255) NULL
                    """
                )
            except Exception:
                # Column already exists.
                pass

            cursor.execute(
                """
                UPDATE players
                SET password = %s
                WHERE username = %s
                """,
                (password, username)
            )

            connection.commit()

        except Exception as e:
            print(
                "Could not save demo password:",
                e
            )

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

            if connection:
                try:
                    connection.close()
                except Exception:
                    pass

    # ======================================================
    # START EVENTS
    # ======================================================

    def handle_start_events(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button != 1:
                return

            pos = event.pos

            if self.start_button_rect.collidepoint(
                pos
            ):

                self.start_game()

            elif self.start_leaderboard_rect.collidepoint(
                pos
            ):

                self.game_state = "leaderboard"

            elif self.start_logout_rect.collidepoint(
                pos
            ):

                self.logout()

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:
                self.start_game()

            elif event.key == pygame.K_ESCAPE:
                self.game_state = "settings"

    # ======================================================
    # BUFF EVENTS
    # ======================================================

    def handle_buff_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for index, rect in enumerate(self.buff_card_rects):
                if rect.collidepoint(event.pos) and index < len(self.buff_cards):
                    self.apply_buff(self.buff_cards[index]["id"])
                    self.begin_stage()
                    return

        if event.type == pygame.KEYDOWN:
            key_map = {pygame.K_1: 0, pygame.K_KP1: 0, pygame.K_2: 1, pygame.K_KP2: 1, pygame.K_3: 2, pygame.K_KP3: 2}
            if event.key in key_map:
                index = key_map[event.key]
                if index < len(self.buff_cards):
                    self.apply_buff(self.buff_cards[index]["id"])
                    self.begin_stage()

    # ======================================================
    # GAME EVENTS
    # ======================================================

    def handle_game_events(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                self.game_state = "settings"

    # ======================================================
    # GAME OVER EVENTS
    # ======================================================

    def handle_game_over_events(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button != 1:
                return

            pos = event.pos

            if self.play_again_rect.collidepoint(
                pos
            ):

                self.start_game()

            elif self.game_leaderboard_rect.collidepoint(
                pos
            ):

                self.game_state = "leaderboard"

            elif self.game_logout_rect.collidepoint(
                pos
            ):

                self.logout()

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:

                self.start_game()

            elif event.key == pygame.K_ESCAPE:

                self.game_state = "start"

    # ======================================================
    # LEADERBOARD EVENTS
    # ======================================================

    def handle_leaderboard_events(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                self.game_state = "start"

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                self.game_state = "start"

    # ======================================================
    # SETTINGS EVENTS
    # ======================================================

    def handle_settings_events(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button != 1:
                return

            pos = event.pos

            # ----------------------------------------------
            # VOLUME DOWN
            # ----------------------------------------------

            if self.volume_minus_rect.collidepoint(
                pos
            ):

                self.volume -= 0.1

                self.volume = max(
                    0.0,
                    self.volume
                )

                self.save_current_settings()

                self.apply_volume()

            # ----------------------------------------------
            # VOLUME UP
            # ----------------------------------------------

            elif self.volume_plus_rect.collidepoint(
                pos
            ):

                self.volume += 0.1

                self.volume = min(
                    1.0,
                    self.volume
                )

                self.save_current_settings()

                self.apply_volume()

            # ----------------------------------------------
            # MOBILE CONTROLS TOGGLE
            # ----------------------------------------------

            elif self.mobile_toggle_rect.collidepoint(pos):
                self.mobile_controls = not self.mobile_controls
                self.save_current_settings()

            # ----------------------------------------------
            # BACK
            # ----------------------------------------------

            elif self.settings_back_rect.collidepoint(
                pos
            ):

                if self.player is not None:

                    self.game_state = "playing"

                else:

                    self.game_state = "start"

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                if self.player is not None:

                    self.game_state = "playing"

                else:

                    self.game_state = "start"

            elif event.key == pygame.K_MINUS:

                self.volume -= 0.1

                self.volume = max(
                    0.0,
                    self.volume
                )

                self.save_current_settings()

                self.apply_volume()

            elif event.key == pygame.K_EQUALS:

                self.volume += 0.1

                self.volume = min(
                    1.0,
                    self.volume
                )

                self.save_current_settings()

                self.apply_volume()

    # ======================================================
    # SAVE SETTINGS
    # ======================================================

    def save_current_settings(self):

        self.settings.setdefault(
            "sound",
            {}
        )

        self.settings["sound"]["volume"] = round(self.volume, 2)
        self.settings.setdefault("controls", {})
        self.settings["controls"]["mobile"] = bool(self.mobile_controls)

        try:

            save_settings(
                self.settings
            )

        except Exception:
            pass

    # ======================================================
    # BUFF / BOSS SYSTEM
    # ======================================================

    def prepare_buff_selection(self):
        pool = [
            {"id": "rapid_fire", "title": "RAPID FIRE", "description": "Shoot faster. Fire delay is reduced.", "color": self.cyan},
            {"id": "twin_shot", "title": "TWIN SHOT", "description": "Fire two extra bullets beside the main shot.", "color": self.yellow},
            {"id": "speed", "title": "SPEED BOOST", "description": "Increase your movement speed.", "color": self.green},
            {"id": "shield", "title": "ENERGY SHIELD", "description": "Block one hit without losing a heart.", "color": self.blue},
            {"id": "heart", "title": "EXTRA HEART", "description": "Gain one maximum heart and restore one heart.", "color": self.red},
            {"id": "power", "title": "POWER CORE", "description": "Increase bullet damage against the boss.", "color": self.orange},
        ]
        self.buff_cards = random.sample(pool, 3)

    def apply_buff(self, buff_id):
        self.buff_levels[buff_id] = self.buff_levels.get(buff_id, 0) + 1
        if buff_id == "rapid_fire":
            self.fire_delay = max(3, self.fire_delay - 2)
        elif buff_id == "twin_shot":
            self.twin_shot = True
        elif buff_id == "speed":
            if hasattr(self.player, "speed"):
                self.player.speed = min(12, self.player.speed + 1)
        elif buff_id == "shield":
            self.shield_charges += 1
        elif buff_id == "heart":
            self.max_hearts += 1
            self.hearts = min(self.max_hearts, self.hearts + 1)
        elif buff_id == "power":
            self.player_power += 1

    def begin_stage(self):
        self.game_state = "playing"
        self.enemies.clear()
        self.enemy_bullets.clear()
        self.enemy_spawn_timer = 0
        self.enemy_fire_timer = 0
        self.boss_fire_timer = 0
        self.damage_cooldown = max(self.damage_cooldown, 75)
        self.stage_message_timer = 100

        # Boss schedule:
        # Stage 5, 15, 25... = Mini Boss
        # Stage 10, 20, 30... = Main Boss
        # All other stages = normal enemies only (they DO NOT shoot).
        if self.stage % 10 == 0:
            self.boss = SpaceBoss(self.screen_width, self.screen_height, hp=120 + (self.stage - 10) * 15)
            self.boss_type = "boss"
            self.boss_fire_delay = max(28, 42 - (self.stage - 10) // 2)
        elif self.stage % self.mini_boss_stage_interval == 0:
            self.boss = MiniBoss(
                self.screen_width,
                self.screen_height,
                hp=65 + (self.stage - 5) * 8
            )
            self.boss_type = "mini_boss"
            self.boss_fire_delay = max(38, 55 - (self.stage - 5) // 2)
        else:
            self.boss = None
            self.boss_type = None

    def boss_fire(self):
        """Only bosses fire. Normal enemy ships never fire bullets."""
        if not self.boss or self.boss.is_dead():
            return

        remaining = self.max_enemy_bullets - len(self.enemy_bullets)
        if remaining <= 0:
            return

        x = self.boss.x + self.boss.width // 2
        y = self.boss.y + self.boss.height

        if self.boss_type == "mini_boss":
            patterns = [
                (0, 4.5, 0),
                (-28, 4.2, -0.8),
                (28, 4.2, 0.8),
            ]
        else:
            patterns = [
                (0, 4.2, 0),
                (-45, 4.0, -1.0),
                (45, 4.0, 1.0),
            ]

        for offset, speed, horizontal_speed in patterns[:remaining]:
            self.enemy_bullets.append(
                EnemyBullet(
                    x + offset,
                    y,
                    speed=speed,
                    horizontal_speed=horizontal_speed
                )
            )

    def defeat_boss(self):
        if self.boss_type == "mini_boss":
            self.score += 500
        else:
            self.score += 1000

        self.play_explosion_sound()
        self.boss = None
        self.boss_type = None
        self.enemy_bullets.clear()
        self.bullets.clear()
        self.stage += 1
        self.enemies_defeated = 0
        self.stage_target = 10 + (self.stage - 1) * 2
        self.prepare_buff_selection()
        self.game_state = "buff_select"

    # ======================================================
    # UPDATE
    # ======================================================

    def update(self):

        # Keep the background animation independent from gameplay state.
        self.background.update()

        if self.shoot_sound_cooldown > 0:
            self.shoot_sound_cooldown -= 1

        if self.explosion_sound_cooldown > 0:
            self.explosion_sound_cooldown -= 1

        if self.game_state != "playing":
            return

        if self.player is None:
            return

        # Damage invincibility timer
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        if self.stage_message_timer > 0:
            self.stage_message_timer -= 1

        keys = pygame.key.get_pressed()

        # ==================================================
        # PLAYER MOVEMENT
        # ==================================================

        if keys[pygame.K_LEFT]:

            self.player.move_left()

        if keys[pygame.K_RIGHT]:

            self.player.move_right()

        mouse_buttons = pygame.mouse.get_pressed()
        if self.mobile_controls:
            if mouse_buttons[0] and self.mobile_left_rect.collidepoint(pygame.mouse.get_pos()):
                self.player.move_left()
            if mouse_buttons[0] and self.mobile_right_rect.collidepoint(pygame.mouse.get_pos()):
                self.player.move_right()

        # ==================================================
        # CONTINUOUS FIRING
        # ==================================================

        if self.fire_cooldown > 0:

            self.fire_cooldown -= 1

        firing = keys[pygame.K_SPACE]
        if self.mobile_controls and pygame.mouse.get_pressed()[0]:
            firing = firing or self.mobile_fire_rect.collidepoint(pygame.mouse.get_pos())

        if firing:

            if self.fire_cooldown <= 0:

                self.fire_player_bullet()

                self.fire_cooldown = (
                    self.fire_delay
                )

        # ==================================================
        # PLAYER UPDATE
        # ==================================================

        self.player.update()

        # ==================================================
        # BOSS UPDATE
        # ==================================================

        if self.boss is not None:
            self.boss.update()
            self.boss_fire_timer += 1
            if self.boss_fire_timer >= self.boss_fire_delay:
                self.boss_fire()
                self.boss_fire_timer = 0

        # ==================================================
        # PLAYER BULLETS
        # ==================================================

        for bullet in self.bullets[:]:

            bullet.update()

            if bullet.is_off_screen():

                self.bullets.remove(
                    bullet
                )

        # ==================================================
        # STAGE DIFFICULTY
        # ==================================================

        current_spawn_delay = max(25, self.enemy_spawn_delay - (self.stage - 1) * 4)
        current_fire_delay = max(20, self.enemy_fire_delay - (self.stage - 1) * 3)
        current_max_enemies = min(10, 5 + (self.stage - 1) // 2)

        # ==================================================
        # ENEMY SPAWNING
        # ==================================================

        if self.boss is None:
            self.enemy_spawn_timer += 1

        if (
            self.boss is None
            and self.enemy_spawn_timer
            >= current_spawn_delay
        ):

            if len(self.enemies) < current_max_enemies:

                self.spawn_enemy()

            self.enemy_spawn_timer = 0

        # ==================================================
        # ENEMY UPDATE
        # ==================================================

        for enemy in ([] if self.boss is not None else self.enemies[:]):

            enemy.update()

            if enemy.is_off_screen(
                self.screen_height
            ):

                self.enemies.remove(
                    enemy
                )

                # An enemy reaching the bottom costs one heart.
                self.lose_life()

                if self.game_state == "game_over":
                    return

        # ==================================================
        # NORMAL ENEMY FIRING REMOVED
        # ==================================================
        # Regular enemy ships no longer shoot.
        # Only MiniBoss and SpaceBoss can create enemy bullets.

        # ==================================================
        # ENEMY BULLETS
        # ==================================================

        for bullet in self.enemy_bullets[:]:

            bullet.update()

            if bullet.is_off_screen(
                self.screen_height
            ):

                # lose_life() can clear enemy_bullets, so always verify
                # the object is still in the list before removing it.
                if bullet in self.enemy_bullets:
                    self.enemy_bullets.remove(bullet)

                continue

            if bullet.rect.colliderect(
                self.player.rect
            ):

                # lose_life() may clear/reset the entire enemy bullet list.
                # Checking membership prevents: ValueError: list.remove(x)
                if bullet in self.enemy_bullets:
                    self.enemy_bullets.remove(bullet)

                self.play_explosion_sound()
                self.lose_life()

                if self.game_state == "game_over":
                    return

                continue

        # ==================================================
        # PLAYER BULLET VS ENEMY
        # ==================================================

        for bullet in self.bullets[:]:

            hit_enemy = None

            for enemy in self.enemies[:]:

                if bullet.rect.colliderect(
                    enemy.rect
                ):

                    hit_enemy = enemy

                    break

            if hit_enemy:

                if bullet in self.bullets:

                    self.bullets.remove(
                        bullet
                    )

                if hit_enemy in self.enemies:

                    self.enemies.remove(
                        hit_enemy
                    )

                self.score += 10
                self.enemies_defeated += 1

                self.play_explosion_sound()

                # Advance to the next stage after enough enemies
                # have been destroyed.
                if self.enemies_defeated >= self.stage_target:
                    self.advance_stage()
                    return

        # ==================================================
        # PLAYER BULLETS VS BOSS
        # ==================================================

        if self.boss is not None:
            for bullet in self.bullets[:]:
                if bullet.rect.colliderect(self.boss.rect):
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    self.boss.take_damage(self.player_power)
                    self.score += 20
                    if self.boss.is_dead():
                        self.defeat_boss()
                        return

        # ==================================================
        # PLAYER VS ENEMY
        # ==================================================

        if self.boss is not None and self.boss.rect.colliderect(self.player.rect):
            self.lose_life()
            if self.game_state == "game_over":
                return

        for enemy in ([] if self.boss is not None else self.enemies[:]):

            if enemy.rect.colliderect(
                self.player.rect
            ):

                self.play_explosion_sound()

                if enemy in self.enemies:
                    self.enemies.remove(enemy)

                self.lose_life()

                if self.game_state == "game_over":
                    return

                break

    # ======================================================
    # PLAYER FIRE
    # ======================================================

    def fire_player_bullet(self):

        # Prevent an unlimited number of bullets from accumulating.
        if len(self.bullets) >= self.max_player_bullets:
            return

        bullet_x = (
            self.player.x
            + self.player.width // 2
        )

        bullet_y = self.player.y

        bullet = Bullet(
            bullet_x,
            bullet_y
        )

        self.bullets.append(bullet)

        # Twin Shot = center + left + right.
        # Respect the global bullet cap to avoid frame spikes.
        if self.twin_shot:
            if len(self.bullets) < self.max_player_bullets:
                self.bullets.append(
                    Bullet(bullet_x - 22, bullet_y)
                )

            if len(self.bullets) < self.max_player_bullets:
                self.bullets.append(
                    Bullet(bullet_x + 22, bullet_y)
                )

        self.play_shoot_sound()

    # ======================================================
    # SPAWN ENEMY
    # ======================================================

    def spawn_enemy(self):

        enemy = Enemy(
            self.screen_width,
            self.screen_height
        )

        # Increase enemy speed as stages become harder.
        enemy.speed = min(5.0, 1.0 + (self.stage - 1) * 0.35)

        self.enemies.append(
            enemy
        )

    # ======================================================
    # ENEMY FIRE
    # ======================================================

    def enemy_fire(self):
        # Kept for compatibility; regular enemies are no longer allowed to fire.
        return

        if not self.enemies:
            return

        if len(self.enemy_bullets) >= self.max_enemy_bullets:
            return

        # Choose a random enemy
        enemy = random.choice(
            self.enemies
        )

        bullet = EnemyBullet(
            enemy.x + enemy.width // 2,
            enemy.y + enemy.height,
            speed=2
        )

        self.enemy_bullets.append(
            bullet
        )

    # ======================================================
    # LOSE LIFE
    # ======================================================

    def lose_life(self):

        # Prevent one collision from removing multiple hearts.
        if self.damage_cooldown > 0:
            return

        if self.shield_charges > 0:
            self.shield_charges -= 1
            self.damage_cooldown = 90
            self.enemy_bullets.clear()
            return

        self.hearts -= 1
        self.damage_cooldown = 90

        # Remove enemy bullets so the player gets a fair recovery window.
        self.enemy_bullets.clear()

        if self.hearts <= 0:
            self.hearts = 0
            self.finish_game()

    # ======================================================
    # ADVANCE STAGE
    # ======================================================

    def advance_stage(self):

        self.stage += 1
        self.enemies_defeated = 0

        # More enemies are required for each new stage.
        self.stage_target = 10 + (self.stage - 1) * 2

        # Clear the old wave and start a fresh one.
        self.enemies.clear()
        self.enemy_bullets.clear()
        self.boss = None
        self.boss_type = None

        self.enemy_spawn_timer = 0
        self.enemy_fire_timer = 0

        self.stage_message_timer = 120

        # Give the player a little protection while choosing the next buff.
        self.damage_cooldown = 60
        self.prepare_buff_selection()
        self.game_state = "buff_select"

    # ======================================================
    # FINISH GAME
    # ======================================================

    def finish_game(self):

        if self.game_state == "game_over":
            return

        if not self.score_saved:

            self.save_score()

            self.score_saved = True

        self.game_state = "game_over"

    # ======================================================
    # SAVE SCORE
    # ======================================================

    def save_score(self):

        if not self.current_player_id:
            return

        try:

            self.database.save_score(
                self.current_player_id,
                self.score
            )

        except Exception:
            pass

    # ======================================================
    # LOGOUT
    # ======================================================

    def logout(self):

        self.current_player = None
        self.current_player_id = None

        self.score = 0
        self.stage = 1
        self.hearts = self.max_hearts
        self.enemies_defeated = 0
        self.stage_target = 10
        self.damage_cooldown = 0
        self.boss = None
        self.boss_type = None
        self.buff_cards = []
        self.twin_shot = False
        self.shield_charges = 0
        self.player_power = 1
        self.fire_delay = 9
        self.max_hearts = 3

        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []

        self.player = None

        self.reset_auth()

        self.register_mode = False

        self.game_state = "auth"

    # ======================================================
    # DRAW
    # ======================================================

    def draw(self):

        self.screen.fill(
            self.bg_color
        )

        if self.game_state == "auth":

            self.draw_auth()

        elif self.game_state == "start":

            self.draw_start()

        elif self.game_state == "playing":

            self.draw_game()

        elif self.game_state == "buff_select":

            self.draw_buff_selection()

        elif self.game_state == "game_over":

            self.draw_game_over()

        elif self.game_state == "leaderboard":

            self.draw_leaderboard()

        elif self.game_state == "settings":

            self.draw_settings()

    # ======================================================
    # AUTH DRAW
    # ======================================================

    def draw_auth(self):

        # ==================================================
        # TITLE
        # ==================================================

        title_text = (
            "CREATE ACCOUNT"
            if self.register_mode
            else "SPACE INVADERS"
        )

        title = self.font_title.render(
            title_text,
            True,
            self.cyan
        )

        title_rect = title.get_rect(
            center=(
                self.screen_width // 2,
                100
            )
        )

        self.screen.blit(
            title,
            title_rect
        )

        subtitle_text = (
            "Register to play"
            if self.register_mode
            else "Login to continue"
        )

        subtitle = self.font.render(
            subtitle_text,
            True,
            self.gray
        )

        subtitle_rect = subtitle.get_rect(
            center=(
                self.screen_width // 2,
                160
            )
        )

        self.screen.blit(
            subtitle,
            subtitle_rect
        )

        # ==================================================
        # USERNAME
        # ==================================================

        self.draw_input(
            self.username_rect,
            "Username",
            self.username,
            "username"
        )

        # ==================================================
        # PASSWORD
        # ==================================================

        password_value = self.password

        if self.show_password:

            password_display = password_value

        else:

            password_display = (
                "*" * len(password_value)
            )

        self.draw_input(
            self.password_rect,
            "Password",
            password_display,
            "password"
        )

        # ==================================================
        # AUTH BUTTON
        # ==================================================

        self.draw_button(
            self.auth_button_rect,
            "REGISTER"
            if self.register_mode
            else "LOGIN",
            self.blue
        )

        # ==================================================
        # SWITCH BUTTON
        # ==================================================

        switch_text = (
            "Already have an account? LOGIN"
            if self.register_mode
            else "Create a new account"
        )

        self.draw_button(
            self.switch_button_rect,
            switch_text,
            self.panel2_color,
            small=True
        )

        # ==================================================
        # PASSWORD INFO
        # ==================================================

        info = self.font_small.render(
            "Click a field to type  |  TAB = next field  |  F2 = show/hide password",
            True,
            self.gray
        )

        info_rect = info.get_rect(
            center=(
                self.screen_width // 2,
                590
            )
        )

        self.screen.blit(
            info,
            info_rect
        )

        # ==================================================
        # MESSAGE
        # ==================================================

        if self.auth_message:

            message = self.font_small.render(
                self.auth_message,
                True,
                self.auth_message_color
            )

            message_rect = message.get_rect(
                center=(
                    self.screen_width // 2,
                    690
                )
            )

            self.screen.blit(
                message,
                message_rect
            )

    # ======================================================
    # INPUT DRAW
    # ======================================================

    def draw_input(
        self,
        rect,
        label,
        value,
        field_name
    ):

        # --------------------------------------------------
        # LABEL
        # --------------------------------------------------

        label_surface = self.font_small.render(
            label,
            True,
            self.gray
        )

        self.screen.blit(
            label_surface,
            (
                rect.x,
                rect.y - 28
            )
        )

        # --------------------------------------------------
        # BACKGROUND
        # --------------------------------------------------

        pygame.draw.rect(
            self.screen,
            self.panel_color,
            rect,
            border_radius=10
        )

        # --------------------------------------------------
        # BORDER
        # --------------------------------------------------

        if self.active_field == field_name:

            border_color = self.cyan

            border_width = 3

        else:

            border_color = self.dark_gray

            border_width = 2

        pygame.draw.rect(
            self.screen,
            border_color,
            rect,
            border_width,
            border_radius=10
        )

        # --------------------------------------------------
        # TEXT
        # --------------------------------------------------

        if value:

            text_surface = self.font.render(
                value,
                True,
                self.white
            )

        else:

            placeholder = (
                "Enter " + label.lower()
            )

            text_surface = self.font.render(
                placeholder,
                True,
                self.dark_gray
            )

        text_rect = text_surface.get_rect(
            midleft=(
                rect.x + 15,
                rect.centery
            )
        )

        self.screen.blit(
            text_surface,
            text_rect
        )

        # --------------------------------------------------
        # CURSOR
        # --------------------------------------------------

        if self.active_field == field_name:

            if pygame.time.get_ticks() % 1000 < 500:

                cursor_x = (
                    rect.x
                    + 15
                    + text_surface.get_width()
                    + 2
                )

                cursor_top = (
                    rect.y + 12
                )

                cursor_bottom = (
                    rect.bottom - 12
                )

                pygame.draw.line(
                    self.screen,
                    self.cyan,
                    (
                        cursor_x,
                        cursor_top
                    ),
                    (
                        cursor_x,
                        cursor_bottom
                    ),
                    2
                )

    # ======================================================
    # START DRAW
    # ======================================================

    def draw_start(self):

        # ==================================================
        # TITLE
        # ==================================================

        title = self.font_title.render(
            "SPACE INVADERS",
            True,
            self.cyan
        )

        title_rect = title.get_rect(
            center=(
                self.screen_width // 2,
                120
            )
        )

        self.screen.blit(
            title,
            title_rect
        )

        # ==================================================
        # WELCOME
        # ==================================================

        player_name = "Player"

        if self.current_player:

            player_name = self.current_player.get(
                "username",
                "Player"
            )

        welcome = self.font_medium.render(
            "Welcome, " + player_name + "!",
            True,
            self.white
        )

        welcome_rect = welcome.get_rect(
            center=(
                self.screen_width // 2,
                220
            )
        )

        self.screen.blit(
            welcome,
            welcome_rect
        )

        # ==================================================
        # DESCRIPTION
        # ==================================================

        desc = self.font.render(
            "Destroy enemies and survive as long as possible!",
            True,
            self.gray
        )

        desc_rect = desc.get_rect(
            center=(
                self.screen_width // 2,
                285
            )
        )

        self.screen.blit(
            desc,
            desc_rect
        )

        # ==================================================
        # START BUTTON
        # ==================================================

        self.draw_button(
            self.start_button_rect,
            "START GAME",
            self.green
        )

        # ==================================================
        # LEADERBOARD
        # ==================================================

        self.draw_button(
            self.start_leaderboard_rect,
            "LEADERBOARD",
            self.panel2_color,
            small=True
        )

        # ==================================================
        # LOGOUT
        # ==================================================

        self.draw_button(
            self.start_logout_rect,
            "LOGOUT",
            self.red,
            small=True
        )

        # ==================================================
        # CONTROLS
        # ==================================================

        controls = self.font_small.render(
            "LEFT / RIGHT = Move     HOLD SPACE = Fire     ESC = Settings",
            True,
            self.gray
        )

        controls_rect = controls.get_rect(
            center=(
                self.screen_width // 2,
                660
            )
        )

        self.screen.blit(
            controls,
            controls_rect
        )

    # ======================================================
    # DRAW HEARTS
    # ======================================================

    def draw_hearts(self, start_x, start_y):

        label = self.font_small.render(
            "LIVES",
            True,
            self.white
        )

        self.screen.blit(
            label,
            (start_x, start_y + 4)
        )

        for i in range(self.max_hearts):

            x = start_x + 65 + i * 32
            y = start_y + 13

            filled = i < self.hearts
            color = self.red if filled else self.dark_gray

            # Simple heart shape made from circles and a triangle.
            pygame.draw.circle(
                self.screen,
                color,
                (x - 5, y - 3),
                7
            )

            pygame.draw.circle(
                self.screen,
                color,
                (x + 5, y - 3),
                7
            )

            pygame.draw.polygon(
                self.screen,
                color,
                [
                    (x - 11, y),
                    (x + 11, y),
                    (x, y + 15)
                ]
            )

    # ======================================================
    # GAME DRAW
    # ======================================================

    def draw_game(self):

        # ==================================================
        # BACKGROUND
        # ==================================================

        self.background.draw(self.screen)

        # ==================================================
        # SCORE
        # ==================================================

        score_text = self.font_medium.render(
            "SCORE: " + str(self.score),
            True,
            self.white
        )

        self.screen.blit(
            score_text,
            (
                25,
                20
            )
        )

        # ==================================================
        # STAGE
        # ==================================================

        stage_text = self.font_medium.render(
            f"STAGE {self.stage}",
            True,
            self.cyan
        )

        stage_rect = stage_text.get_rect(
            center=(
                self.screen_width // 2,
                30
            )
        )

        self.screen.blit(
            stage_text,
            stage_rect
        )

        # ==================================================
        # HEARTS / LIVES
        # ==================================================

        self.draw_hearts(
            self.screen_width - 180,
            15
        )

        if self.shield_charges > 0:
            shield_text = self.font_small.render(
                f"SHIELD x{self.shield_charges}",
                True,
                self.blue
            )
            self.screen.blit(
                shield_text,
                shield_text.get_rect(center=(self.screen_width - 105, 62))
            )

        # ==================================================
        # PLAYER
        # ==================================================

        if self.player:

            # Blink while temporarily protected after taking damage.
            if self.damage_cooldown <= 0 or (self.damage_cooldown // 6) % 2 == 0:
                self.player.draw(
                    self.screen
                )

        # ==================================================
        # PLAYER BULLETS
        # ==================================================

        for bullet in self.bullets:

            bullet.draw(
                self.screen
            )

        # ==================================================
        # BOSS
        # ==================================================

        if self.boss is not None:
            self.boss.draw(self.screen)
            if self.boss_type == "mini_boss":
                label_text = "MINI BOSS"
                label_color = (90, 190, 255)
            else:
                label_text = "BOSS"
                label_color = (255, 100, 180)
            boss_label = self.font_medium.render(label_text, True, label_color)
            self.screen.blit(
                boss_label,
                boss_label.get_rect(center=(self.screen_width // 2, 205))
            )

        # ==================================================
        # ENEMIES
        # ==================================================

        for enemy in self.enemies:

            enemy.draw(
                self.screen
            )

        # ==================================================
        # ENEMY BULLETS
        # ==================================================

        for bullet in self.enemy_bullets:

            bullet.draw(
                self.screen
            )

        # ==================================================
        # STAGE MESSAGE
        # ==================================================

        if self.stage_message_timer > 0:

            stage_message = self.font_large.render(
                f"STAGE {self.stage}",
                True,
                self.yellow
            )

            stage_message_rect = stage_message.get_rect(
                center=(
                    self.screen_width // 2,
                    130
                )
            )

            self.screen.blit(
                stage_message,
                stage_message_rect
            )

        # ==================================================
        # MOBILE CONTROLS
        # ==================================================

        if self.mobile_controls:
            self.draw_button(self.mobile_left_rect, "LEFT", self.panel2_color, small=True)
            self.draw_button(self.mobile_right_rect, "RIGHT", self.panel2_color, small=True)
            self.draw_button(self.mobile_fire_rect, "FIRE", self.red, small=True)

        # ==================================================
        # CONTROL INFO
        # ==================================================

        control_text = self.font_small.render(
            "LEFT / RIGHT = MOVE     HOLD SPACE = FIRE     ESC = SETTINGS",
            True,
            self.gray
        )

        control_rect = control_text.get_rect(
            center=(
                self.screen_width // 2,
                self.screen_height - 20
            )
        )

        self.screen.blit(
            control_text,
            control_rect
        )

    # ======================================================
    # BUFF SELECTION DRAW
    # ======================================================

    def draw_buff_selection(self):
        self.screen.fill(self.bg_color)

        title = self.font_title.render("CHOOSE YOUR BUFF", True, self.cyan)
        self.screen.blit(title, title.get_rect(center=(self.screen_width // 2, 80)))

        stage_text = self.font_medium.render(f"STAGE {self.stage}", True, self.yellow)
        self.screen.blit(stage_text, stage_text.get_rect(center=(self.screen_width // 2, 140)))

        message = self.font_small.render(
            "Choose one card. Your buff stays active for the rest of this run.",
            True, self.gray
        )
        self.screen.blit(message, message.get_rect(center=(self.screen_width // 2, 180)))

        mouse_pos = pygame.mouse.get_pos()

        for index, card in enumerate(self.buff_cards):
            rect = self.buff_card_rects[index]
            color = card["color"]
            hovered = rect.collidepoint(mouse_pos)
            panel = tuple(min(255, c + 18) for c in self.panel_color) if hovered else self.panel_color

            pygame.draw.rect(self.screen, panel, rect, border_radius=18)
            pygame.draw.rect(self.screen, color, rect, width=3, border_radius=18)

            number = self.font_medium.render(str(index + 1), True, color)
            self.screen.blit(number, number.get_rect(center=(rect.centerx, rect.top + 38)))

            title_surface = self.font_medium.render(card["title"], True, self.white)
            self.screen.blit(title_surface, title_surface.get_rect(center=(rect.centerx, rect.top + 95)))

            words = card["description"].split()
            lines = []
            current = ""
            for word in words:
                test = (current + " " + word).strip()
                if self.font_small.size(test)[0] <= rect.width - 30:
                    current = test
                else:
                    if current:
                        lines.append(current)
                    current = word
            if current:
                lines.append(current)

            y = rect.top + 145
            for line in lines:
                surface = self.font_small.render(line, True, self.gray)
                self.screen.blit(surface, surface.get_rect(center=(rect.centerx, y)))
                y += 25

            choose = self.font_small.render(f"CLICK OR PRESS {index + 1}", True, color)
            self.screen.blit(choose, choose.get_rect(center=(rect.centerx, rect.bottom - 35)))

        active = []
        if self.twin_shot:
            active.append("Twin Shot")
        if self.shield_charges:
            active.append(f"Shield x{self.shield_charges}")
        if self.max_hearts > 3:
            active.append(f"Hearts {self.max_hearts}")
        if self.fire_delay < 9:
            active.append("Rapid Fire")
        if self.player_power > 1:
            active.append(f"Power x{self.player_power}")

        if active:
            active_text = self.font_small.render(
                "Active Buffs: " + "  |  ".join(active),
                True, self.green
            )
            self.screen.blit(active_text, active_text.get_rect(center=(self.screen_width // 2, 610)))

    # ======================================================
    # GAME OVER DRAW
    # ======================================================

    def draw_game_over(self):

        title = self.font_title.render(
            "GAME OVER",
            True,
            self.red
        )

        title_rect = title.get_rect(
            center=(
                self.screen_width // 2,
                130
            )
        )

        self.screen.blit(
            title,
            title_rect
        )

        score_text = self.font_large.render(
            "SCORE: " + str(self.score),
            True,
            self.yellow
        )

        score_rect = score_text.get_rect(
            center=(
                self.screen_width // 2,
                250
            )
        )

        self.screen.blit(
            score_text,
            score_rect
        )

        stage_text = self.font_medium.render(
            f"REACHED STAGE {self.stage}",
            True,
            self.cyan
        )

        stage_rect = stage_text.get_rect(
            center=(
                self.screen_width // 2,
                315
            )
        )

        self.screen.blit(
            stage_text,
            stage_rect
        )

        self.draw_button(
            self.play_again_rect,
            "PLAY AGAIN",
            self.green
        )

        self.draw_button(
            self.game_leaderboard_rect,
            "LEADERBOARD",
            self.panel2_color,
            small=True
        )

        self.draw_button(
            self.game_logout_rect,
            "LOGOUT",
            self.red,
            small=True
        )

    # ======================================================
    # LEADERBOARD DRAW
    # ======================================================

    def draw_leaderboard(self):

        title = self.font_title.render(
            "LEADERBOARD",
            True,
            self.cyan
        )

        title_rect = title.get_rect(
            center=(
                self.screen_width // 2,
                80
            )
        )

        self.screen.blit(
            title,
            title_rect
        )

        try:

            leaderboard = (
                self.database.get_leaderboard(
                    10
                )
            )

        except Exception:

            leaderboard = []

        start_y = 160

        # Header
        header = self.font_medium.render(
            "RANK       PLAYER                 SCORE",
            True,
            self.yellow
        )

        header_rect = header.get_rect(
            center=(
                self.screen_width // 2,
                start_y
            )
        )

        self.screen.blit(
            header,
            header_rect
        )

        y = start_y + 55

        if not leaderboard:

            empty = self.font.render(
                "No scores yet.",
                True,
                self.gray
            )

            empty_rect = empty.get_rect(
                center=(
                    self.screen_width // 2,
                    y + 40
                )
            )

            self.screen.blit(
                empty,
                empty_rect
            )

        else:

            for index, row in enumerate(
                leaderboard,
                start=1
            ):

                if isinstance(row, dict):

                    username = row.get(
                        "username",
                        "Unknown"
                    )

                    score = row.get(
                        "score",
                        row.get(
                            "max_score",
                            0
                        )
                    )

                else:

                    try:

                        username = row[0]
                        score = row[1]

                    except Exception:

                        username = "Unknown"
                        score = 0

                line = self.font.render(
                    f"{index:<8} {str(username):<22} {score}",
                    True,
                    self.white
                )

                line_rect = line.get_rect(
                    center=(
                        self.screen_width // 2,
                        y
                    )
                )

                self.screen.blit(
                    line,
                    line_rect
                )

                y += 42

        info = self.font_small.render(
            "Click anywhere or press ESC to return",
            True,
            self.gray
        )

        info_rect = info.get_rect(
            center=(
                self.screen_width // 2,
                self.screen_height - 45
            )
        )

        self.screen.blit(
            info,
            info_rect
        )

    # ======================================================
    # SETTINGS DRAW
    # ======================================================

    def draw_settings(self):

        # ==================================================
        # BACKGROUND
        # ==================================================

        self.screen.fill(self.bg_color)

        # ==================================================
        # SETTINGS PANEL
        # ==================================================

        panel_rect = pygame.Rect(230, 35, 564, 700)

        pygame.draw.rect(
            self.screen,
            self.panel_color,
            panel_rect,
            border_radius=22
        )

        pygame.draw.rect(
            self.screen,
            self.cyan,
            panel_rect,
            2,
            border_radius=22
        )

        center_x = self.screen_width // 2

        # ==================================================
        # TITLE
        # ==================================================

        title = self.font_large.render(
            "SETTINGS",
            True,
            self.cyan
        )

        self.screen.blit(
            title,
            title.get_rect(
                center=(center_x, 95)
            )
        )

        subtitle = self.font_small.render(
            "Configure your game",
            True,
            self.gray
        )

        self.screen.blit(
            subtitle,
            subtitle.get_rect(
                center=(center_x, 135)
            )
        )

        pygame.draw.line(
            self.screen,
            self.dark_gray,
            (285, 170),
            (739, 170),
            2
        )

        # ==================================================
        # SOUND VOLUME
        # ==================================================

        volume_title = self.font_medium.render(
            "Sound Volume",
            True,
            self.white
        )

        self.screen.blit(
            volume_title,
            volume_title.get_rect(
                center=(center_x, 215)
            )
        )

        self.draw_button(
            self.volume_minus_rect,
            "-",
            self.panel2_color
        )

        self.draw_button(
            self.volume_plus_rect,
            "+",
            self.panel2_color
        )

        volume_percent = int(round(self.volume * 100))

        volume_text = self.font_medium.render(
            f"{volume_percent}%",
            True,
            self.yellow
        )

        self.screen.blit(
            volume_text,
            volume_text.get_rect(
                center=(center_x, 282)
            )
        )

        # Volume bar
        bar_x = 370
        bar_y = 325
        bar_width = 284
        bar_height = 12

        pygame.draw.rect(
            self.screen,
            self.dark_gray,
            (bar_x, bar_y, bar_width, bar_height),
            border_radius=6
        )

        filled_width = int(bar_width * self.volume)

        if filled_width > 0:
            pygame.draw.rect(
                self.screen,
                self.cyan,
                (bar_x, bar_y, filled_width, bar_height),
                border_radius=6
            )

        # ==================================================
        # KEYBOARD CONTROLS
        # ==================================================

        controls_title = self.font_medium.render(
            "Keyboard Controls",
            True,
            self.white
        )

        self.screen.blit(
            controls_title,
            controls_title.get_rect(
                center=(center_x, 380)
            )
        )

        controls = [
            "LEFT / RIGHT  -  Move",
            "HOLD SPACE    -  Fire continuously",
            "ESC           -  Open Settings"
        ]

        y = 415

        for control_text in controls:

            surface = self.font_small.render(
                control_text,
                True,
                self.gray
            )

            self.screen.blit(
                surface,
                surface.get_rect(
                    center=(center_x, y)
                )
            )

            y += 25

        # ==================================================
        # MOBILE CONTROLS
        # ==================================================

        mobile_title = self.font_medium.render(
            "Mobile Controls",
            True,
            self.white
        )

        self.screen.blit(
            mobile_title,
            mobile_title.get_rect(
                center=(center_x, 505)
            )
        )

        mobile_label = "ON" if self.mobile_controls else "OFF"

        mobile_color = (
            self.green
            if self.mobile_controls
            else self.red
        )

        self.draw_button(
            self.mobile_toggle_rect,
            mobile_label,
            mobile_color
        )

        mobile_status = (
            "Touch controls enabled"
            if self.mobile_controls
            else "Touch controls disabled"
        )

        status = self.font_small.render(
            mobile_status,
            True,
            self.gray
        )

        self.screen.blit(
            status,
            status.get_rect(
                center=(center_x, 600)
            )
        )

        # ==================================================
        # KEYBOARD SHORTCUTS
        # ==================================================

        help_text = self.font_small.render(
            "- / + Volume     M Mobile     ESC Back",
            True,
            self.gray
        )

        self.screen.blit(
            help_text,
            help_text.get_rect(
                center=(center_x, 625)
            )
        )

        # ==================================================
        # BACK BUTTON
        # ==================================================

        self.draw_button(
            self.settings_back_rect,
            "BACK",
            self.blue
        )

    # ======================================================
    # GENERIC BUTTON
    # ======================================================

    def draw_button(
        self,
        rect,
        text,
        color,
        small=False
    ):

        mouse_pos = pygame.mouse.get_pos()

        if rect.collidepoint(mouse_pos):

            hover_color = tuple(
                min(255, value + 25)
                for value in color
            )

        else:

            hover_color = color

        pygame.draw.rect(
            self.screen,
            hover_color,
            rect,
            border_radius=12
        )

        pygame.draw.rect(
            self.screen,
            (220, 225, 240),
            rect,
            2,
            border_radius=12
        )

        font = (
            self.font_small
            if small
            else self.font_medium
        )

        text_surface = font.render(
            text,
            True,
            self.white
        )

        text_rect = text_surface.get_rect(
            center=rect.center
        )

        self.screen.blit(
            text_surface,
            text_rect
        )
