import pygame
import random

from utils import join
from animation import Animation
from weapon import Rock
from settings import WIDTH, HEIGHT
from healthbar import HealthBar
from particle import Particle


pygame.init()


# subclass
class Enemy:
    def __init__(
        self,
        animations: dict[Animation],
        position: pygame.FRect,
        shooting_speed_ms: float,
        ms_offset: int = None,
    ) -> None:
        if ms_offset is None:
            ms_offset = 0

        # health
        self.health: HealthBar = HealthBar(
            200,
            200,
            pygame.FRect(
                position.x,
                position.y - 20,
                position.width,
                10,
            ),
            "turquoise",
        )

        self.dead = False

        # position
        self.position = position
        self.speed = random.randint(3, 5) * 2

        # animations
        self.animations = animations

        # projectiles
        self.rocks: list[Rock] = []

        # technical stuff
        self.shooting_speed_ms = shooting_speed_ms
        self.current_shooting_ms = self.shooting_speed_ms - ms_offset
        self.ai_offset = random.randint(1, 400) - 200

        # gravity
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0.35)

    def update(self, deltaTime: float, target, particle_list: list[Particle]) -> None:
        self.animation.update(deltaTime)

        self.AI(deltaTime, target)

        self.velocity += self.acceleration * deltaTime * 60

        if self.current_shooting_ms > self.shooting_speed_ms:
            self.current_shooting_ms = 0
            self.rocks.append(
                Rock(
                    pygame.FRect(
                        self.position.x,
                        self.position.y,
                        100,
                        100,
                    ),
                    10,
                    6.5,
                    pygame.Vector2(0, 0),
                )
            )
            # self.rocks[-1].aimto((mx - 20, my - 100)) # TODO remove me
            self.rocks[-1].aimto(
                (target.position.x, target.position.y), random.randint(-7, 7)
            )

        self.current_shooting_ms += deltaTime * 1000

        for rock in self.rocks:
            rock.update(deltaTime, target, particle_list)

            if rock.dead:
                self.rocks.remove(rock)

        # floor
        if self.position.y > HEIGHT - self.position.height:
            self.position.y = HEIGHT - self.position.height
            self.velocity.y = 0
            self.grounded = True
        else:
            self.grounded = False

        # say in screen
        if self.position.x > WIDTH + self.position.width:
            self.position.x = -self.position.width

        if self.position.x < -self.position.width:
            self.position.x = WIDTH + self.position.width

        # update position
        self.position.x += self.velocity.x * deltaTime * 60
        self.position.y += self.velocity.y * deltaTime * 60

        # handle boss stuff and health
        self.health.update(
            pygame.FRect(
                self.position.x,
                self.position.y - 20,
                self.position.width,
                10,
            ),
        )

        if self.health.health <= 0:
            self.dead = True

    def render(self, window) -> None:
        self.animation.render(window, self.position)

        for spear in self.rocks:
            spear.render(window)

        self.health.render(window)

    def AI(self, deltaTime: float, target) -> None:
        move_x: float = 0

        if self.current_shooting_ms >= self.shooting_speed_ms:
            self.ai_offset = random.randint(1, 400) - 200

        target_x = target.position.x + self.ai_offset

        if abs(self.position.x - target_x) > self.speed:
            if self.position.x > target_x:
                move_x = -self.speed
                self.going_right = False
            elif self.position.x < target_x:
                move_x = self.speed
                self.going_right = True

        self.position.x += move_x * deltaTime * 60

    @property
    def animation(self) -> Animation:
        if self.going_right:
            return self.animations["right"]
        else:
            return self.animations["left"]


class UngaBunga(Enemy):
    def __init__(
        self,
        position: pygame.FRect,
        shooting_speed_ms: float,
        ms_offset: int = None,
    ) -> None:
        self.going_right = False  # False: left, True: Right

        # convert breaks the texture
        super().__init__(
            {
                "left": Animation(
                    [
                        pygame.transform.scale(
                            pygame.image.load(
                                join("assets", "ungabunga", f"ungabunga ({n}).png")
                            ),
                            (180, 200),
                        )
                        for n in range(1, 17)
                    ],
                    50,
                ),
                "right": Animation(
                    [
                        pygame.transform.flip(
                            pygame.transform.scale(
                                pygame.image.load(
                                    join("assets", "ungabunga", f"ungabunga ({n}).png")
                                ),
                                (180, 200),
                            ),
                            True,
                            False,
                        )
                        for n in range(1, 17)
                    ],
                    50,
                ),
            },
            position,
            shooting_speed_ms,
            ms_offset,
        )
