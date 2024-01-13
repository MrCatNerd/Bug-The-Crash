import pygame
import time
import sys
import random
import math

from settings import *
from utils import *
from animation import Animation
from player import Player
from enemy import UngaBunga
from particle import Particle
from button import Button
from weapon import Poison

pygame.init()
pygame.mixer.init()


class Main:
    def __init__(self):
        # basic
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(load_image(join("assets", "icon.png")))

        self.app_state: str = "main menu"

        self.clock = pygame.time.Clock()
        self.running = True
        self.background = pygame.transform.scale(
            load_image(join("assets", "ungabungahouse.png")), (WIDTH, HEIGHT)
        )

        # music and sfx
        self.game_over_sfx: pygame.mixer.Sound = pygame.mixer.Sound(
            join("assets", "sfx", "game-over.ogg")
        )
        self.game_over_sfx.set_volume(0.7)

        pygame.mixer.music.load(join("assets", "sound", "menumusic.ogg"))
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play()

        self.current_music = "menu"
        self.music_switch: bool = False
        pygame.mixer.music.set_volume(0.7)

        self.reset()

        # text
        self.font = pygame.font.Font(join("assets", "font", "basis33.ttf"), 30)
        self.button_font = pygame.font.Font(join("assets", "font", "basis33.ttf"), 40)
        self.medium_plus_font = pygame.font.Font(
            join("assets", "font", "basis33.ttf"), 150
        )
        self.medium_minus_font = pygame.font.Font(
            join("assets", "font", "basis33.ttf"), 80
        )
        self.giant_font = pygame.font.Font(join("assets", "font", "basis33.ttf"), 200)

        # ui and hud and more
        self.ui_play_button = Button(
            pygame.FRect(
                self.screen.get_width() / 2 - 50, self.screen.get_height() / 2, 100, 100
            ),
            pygame.transform.scale(
                load_image(
                    join("assets", "interface", "play-button.png"),
                ),
                (100, 100),
            ),
        )

        self.ui_info_button = Button(
            pygame.FRect(
                self.screen.get_width() - 300,
                50,
                100,
                100,
            ),
            pygame.transform.scale(
                load_image(
                    join("assets", "interface", "info.png"),
                ),
                (100, 100),
            ),
        )

        self.ui_exit_button = Button(
            pygame.FRect(self.screen.get_width() - 150, 50, 100, 100),
            pygame.transform.scale(
                load_image(join("assets", "interface", "exit.png"), convert_alpha=True),
                (100, 100),
            ),
        )

        self.hud_home_button = Button(
            pygame.FRect(10, 10, 50, 50),
            pygame.transform.scale(
                load_image(join("assets", "interface", "home.png")), (50, 50)
            ),
        )

        self.hud_retry_button = Button(
            pygame.FRect(10, 70, 50, 50),
            pygame.transform.scale(
                load_image(join("assets", "interface", "retry-arrow.png")), (50, 50)
            ),
        )

        self.hud_pause_button = Button(
            pygame.FRect(10, 130, 50, 50),
            pygame.transform.scale(
                load_image(join("assets", "interface", "pause-button.png")), (50, 50)
            ),
        )

        self.hud_upgrade_button = Button(
            pygame.FRect(10, 190, 50, 50),
            pygame.transform.scale(
                load_image(join("assets", "interface", "upgrade.png")), (50, 50)
            ),
        )

        self.hud_heal_button = Button(
            pygame.FRect(10, 250, 50, 50),
            pygame.transform.scale(
                load_image(join("assets", "interface", "heal.png")), (50, 50)
            ),
        )

        self.hud_speciel_attack_button = Button(
            pygame.FRect(10, 310, 50, 50),
            pygame.transform.scale(
                load_image(join("assets", "interface", "sword-array.png")), (50, 50)
            ),
        )

        self.game_over_home_button = Button(
            pygame.FRect(
                self.screen.get_width() / 2 + 100,
                self.screen.get_height() / 2,
                100,
                100,
            ),
            pygame.transform.scale(
                load_image(join("assets", "interface", "home.png")), (100, 100)
            ),
        )

        self.game_over_retry_button = Button(
            pygame.FRect(
                self.screen.get_width() / 2 - 100,
                self.screen.get_height() / 2,
                100,
                100,
            ),
            pygame.transform.scale(
                load_image(join("assets", "interface", "retry-arrow.png")), (100, 100)
            ),
        )

        self.how_to_play_home_button = Button(
            pygame.FRect(
                self.screen.get_width() - 100,
                self.screen.get_height() - 100,
                100,
                100,
            ),
            pygame.transform.scale(
                load_image(join("assets", "interface", "home.png")), (100, 100)
            ),
        )

        # start
        self.run()

    def reset(self) -> None:
        # particles
        self.particles: list[Particle] = []

        # enemy
        self.ungabungas = [
            UngaBunga(
                pygame.FRect(random.randint(100, 900), -100, 180, 200), 1000, i * 500
            )
            for i in range(1, 4)
        ]

        # player
        self.player = Player(
            {
                "idle": Animation(
                    [
                        pygame.transform.scale(
                            load_image(
                                "assets",
                                "player",
                                f"spiderframe{n}.png",
                                convert_alpha=True,
                            ),
                            (204.8, 180),
                        )
                        for n in range(1, 7)
                    ],
                    100,
                ),
                "left": Animation(
                    [
                        pygame.transform.scale(
                            load_image(
                                "assets",
                                "player",
                                f"spider-sideframe{n}.png",
                                convert_alpha=True,
                            ),
                            (204.8, 200),
                        )
                        for n in range(1, 7)
                    ],
                    50,
                ),
                "right": Animation(
                    [
                        pygame.transform.flip(
                            pygame.transform.scale(
                                load_image(
                                    "assets",
                                    "player",
                                    f"spider-sideframe{n}.png",
                                    convert_alpha=True,
                                ),
                                (204.8, 200),
                            ),
                            True,
                            False,
                        )
                        for n in range(1, 7)
                    ],
                    50,
                ),
            },
            pygame.FRect(500, 100, 204.8, 180),
            250,
        )

    def run(self):
        last_time: float = time.time()

        animation_sin = 0

        while self.running:
            deltaTime: float = time.time() - last_time
            last_time = time.time()

            keys = pygame.key.get_pressed()
            mx, my = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            animation_sin += deltaTime * 60
            animation_sin %= 360

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            self.screen.blit(self.background, (0, 0))

            # main game here

            # music

            if self.current_music == "game" and self.music_switch == True:
                pygame.mixer.music.load(join("assets", "sound", "menumusic.ogg"))
                pygame.mixer.music.play(-1)
                self.music_switch = False
            elif self.current_music == "menu" and self.music_switch == True:
                pygame.mixer.music.load(join("assets", "sound", "spiderswebfinal.ogg"))
                pygame.mixer.music.play(-1)
                self.music_switch = False

            if self.app_state == "main menu":
                self.current_music = "menu"
                self.ui_play_button.update(mx, my, mouse_pressed)
                self.ui_play_button.render(self.screen)

                self.ui_info_button.update(mx, my, mouse_pressed)
                self.ui_info_button.render(self.screen)

                self.ui_exit_button.update(mx, my, mouse_pressed)
                self.ui_exit_button.render(self.screen)

                title = self.medium_plus_font.render("Bug The Crash", False, "white")
                title_shadow = self.medium_plus_font.render(
                    "Bug The Crash", False, "black"
                )

                ungabunga_title = self.medium_minus_font.render(
                    "by MrCatNerd", False, "white"
                )
                ungabunga_title = pygame.transform.rotate(
                    ungabunga_title,
                    math.sin(math.radians(animation_sin)) * 15,
                )

                ungabunga_title_shadow = self.medium_minus_font.render(
                    "by MrCatNerd", False, "black"
                )
                ungabunga_title_shadow = pygame.transform.rotate(
                    ungabunga_title_shadow,
                    math.sin(math.radians(animation_sin)) * 15,
                )

                self.screen.blit(ungabunga_title_shadow, (295, 695))
                self.screen.blit(ungabunga_title, (300, 700))

                self.screen.blit(
                    title_shadow,
                    (95, 195 + math.sin(math.radians(animation_sin)) * 50),
                )
                self.screen.blit(
                    title, (100, 200 + math.sin(math.radians(animation_sin)) * 50)
                )

                if self.ui_info_button.state:
                    self.app_state = "how to play"
                    self.ui_info_button.state = False

                if self.ui_play_button.state:
                    self.music_switch = True
                    self.app_state = "game"
                    self.ui_play_button.state = False

                if self.ui_exit_button.state:
                    self.quit()
            elif self.app_state == "how to play":
                self.how_to_play_home_button.update(mx, my, mouse_pressed)
                self.how_to_play_home_button.render(self.screen)

                if self.how_to_play_home_button.state:
                    self.app_state = "main menu"
                    self.how_to_play_home_button.state = False

                info = self.button_font.render(
                    """
Movement:
    WAD or arrow keys to move
    SPACE to shoot
    LEFT CLICK to hang on a web

You need to murder:
    cavemen

HUD:
- go to main menu option
- restart game option
- pause option
- upgrade option:
    - first 25 coins,
    - second 50 coins,
    - third 75 coins
- heal option - 100 coins
- speciel ability option - 30 coins
""",
                    False,
                    "white",
                )

                self.screen.blit(info, (0, 0))
            elif self.app_state == "game over":
                self.game_over_retry_button.update(mx, my, mouse_pressed)
                self.game_over_retry_button.render(self.screen)

                self.game_over_home_button.update(mx, my, mouse_pressed)
                self.game_over_home_button.render(self.screen)

                self.screen.blit(
                    self.giant_font.render("GAME OVER", True, "black"),
                    (95, self.screen.get_height() - 245),
                )

                self.screen.blit(
                    self.giant_font.render("GAME OVER", True, "white"),
                    (100, self.screen.get_height() - 250),
                )

                if self.game_over_retry_button.state:
                    self.reset()
                    self.app_state = "game"
                    self.game_over_retry_button.state = False
                elif self.game_over_home_button.state:
                    self.music_switch = True
                    self.app_state = "main menu"
                    self.game_over_home_button.state = False
            elif self.app_state == "game":
                self.current_music = "game"
                if not self.hud_pause_button.state:
                    # particles
                    for particle in self.particles:
                        particle.update(deltaTime)
                        particle.render(self.screen)

                        if particle.dead:
                            self.particles.remove(particle)

                    # enemy

                    for ungabunga in self.ungabungas:
                        ungabunga.update(
                            deltaTime,
                            self.player,
                            self.particles,
                        )
                        ungabunga.render(self.screen)

                        if ungabunga.dead:
                            self.ungabungas.remove(ungabunga)
                            self.player.health.health += 100
                            self.player.coins += 5

                    if len(self.ungabungas) < 3:
                        self.ungabungas.append(
                            UngaBunga(
                                pygame.FRect(random.randint(100, 900), -100, 180, 200),
                                1000,
                            )
                        )

                    # player
                    self.player.update(
                        deltaTime,
                        keys,
                        pygame.mouse.get_pressed()[0],
                        self.ungabungas,
                        self.particles,
                    )

                    # shadow
                    self.screen.blit(
                        self.button_font.render(
                            f"{self.player.coins} coins", False, "black"
                        ),
                        (295, 45),
                    )

                    # real text
                    self.screen.blit(
                        self.medium_minus_font.render(
                            f"{self.player.coins} coins\n {self.player.kills} kills",
                            False,
                            "white",
                        ),
                        (300, 50),
                    )

                    if self.player.dead:
                        self.app_state = "game over"
                        self.reset()
                        self.game_over_sfx.play()

                    self.player.render(self.screen)

                    self.hud_speciel_attack_button.update(mx, my, mouse_pressed)
                    self.hud_speciel_attack_button.render(
                        self.screen, "speciel\nattack", self.button_font
                    )

                    self.hud_heal_button.update(mx, my, mouse_pressed)
                    self.hud_heal_button.render(
                        self.screen, "heal\n+100", self.button_font
                    )

                    self.hud_upgrade_button.update(mx, my, mouse_pressed)
                    self.hud_upgrade_button.render(
                        self.screen,
                        self.player.upgrades[self.player.current_upgrade + 1].replace(
                            " ", "\n"
                        ),
                        self.button_font,
                    )

                    self.hud_pause_button.update(mx, my, mouse_pressed)
                    self.hud_pause_button.render(self.screen, "pause", self.button_font)

                    self.hud_retry_button.update(mx, my, mouse_pressed)
                    self.hud_retry_button.render(
                        self.screen, "retry/reset", self.button_font
                    )

                    self.hud_home_button.update(mx, my, mouse_pressed)
                    self.hud_home_button.render(
                        self.screen, "back\nhome", self.button_font
                    )

                    if self.hud_heal_button.state:
                        if self.player.coins >= 100:
                            self.player.coins -= 100
                            self.player.health.health += 100

                        self.hud_heal_button.state = False

                    if self.hud_speciel_attack_button.state:
                        if self.player.coins >= 30:
                            self.player.coins -= 30

                            for x in range(0, self.screen.get_width() + 1, 50):
                                self.player.projectiles.append(
                                    Poison(
                                        (x, random.randint(50, 100)),
                                        random.randint(-3, 3),
                                        -1,
                                    )
                                )

                        self.hud_speciel_attack_button.state = False

                    if self.hud_upgrade_button.state:
                        if (
                            self.player.coins >= (self.player.current_upgrade + 1) * 25
                            and self.player.current_upgrade < 3
                        ):
                            self.player.coins -= (self.player.current_upgrade + 1) * 25
                            self.player.current_upgrade += 1

                            if self.player.current_upgrade == 1:
                                self.player.shoot_delay_ms -= 30
                            elif self.player.current_upgrade == 2:
                                self.player.health.max_health += 150
                                self.player.health.health += 150
                            elif self.player.current_upgrade == 3:
                                self.player.life_steal_percent += 3

                        self.hud_upgrade_button.state = False

                    if self.hud_home_button.state:
                        self.music_switch = True
                        self.app_state = "main menu"
                        self.hud_home_button.state = False
                    if self.hud_retry_button.state:
                        self.reset()
                        self.hud_retry_button.state = False

                else:
                    for particle in self.particles:
                        particle.render(self.screen)

                    for ungabunga in self.ungabungas:
                        ungabunga.render(self.screen)

                    # shadow
                    self.screen.blit(
                        self.button_font.render(
                            f"{self.player.coins} coins\n {self.player.kills} kills",
                            False,
                            "black",
                        ),
                        (295, 45),
                    )

                    # real text
                    self.screen.blit(
                        self.medium_minus_font.render(
                            f"{self.player.coins} coins\n {self.player.kills} kills",
                            False,
                            "white",
                        ),
                        (300, 50),
                    )

                    self.player.render(self.screen)

                    self.hud_speciel_attack_button.render(
                        self.screen, "speciel\nattack", self.button_font
                    )

                    self.hud_heal_button.render(
                        self.screen, "heal\n+100", self.button_font
                    )

                    self.hud_upgrade_button.render(
                        self.screen,
                        self.player.upgrades[self.player.current_upgrade + 1].replace(
                            " ", "\n"
                        ),
                        self.button_font,
                    )

                    self.hud_pause_button.update(mx, my, mouse_pressed)
                    self.hud_pause_button.render(self.screen, "pause", self.button_font)

                    self.hud_retry_button.update(mx, my, mouse_pressed)
                    self.hud_retry_button.render(
                        self.screen, "retry/reset", self.button_font
                    )

                    self.hud_home_button.update(mx, my, mouse_pressed)
                    self.hud_home_button.render(
                        self.screen, "back\nhome", self.button_font
                    )

                    if self.hud_home_button.state:
                        self.app_state = "main menu"
                        self.hud_home_button.state = False

                    if self.hud_pause_button.state:
                        giant_pause = self.giant_font.render("PAUSED", False, "white")
                        self.screen.blit(
                            giant_pause,
                            (
                                self.screen.get_width() / 2 - 250,
                                self.screen.get_height() / 2 - 50,
                            ),
                        )
                        pygame.mixer.music.set_volume(0.2)
                    elif pygame.mixer.music.get_volume() <= 0.2:
                        pygame.mixer.music.set_volume(0.7)
                    if self.hud_retry_button.state:
                        self.reset()
                        self.hud_retry_button.state = False

            # fps
            self.screen.blit(
                self.font.render(
                    f"{round(self.clock.get_fps(), 1)} fps", True, "white"
                ),
                (0, self.screen.get_height() - 30),
            )

            pygame.display.update()
            self.clock.tick()

    def quit(self):
        self.running = False
        pygame.mixer.quit()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main = Main()
