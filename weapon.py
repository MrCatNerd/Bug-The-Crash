import pygame
import math
import random

from pygame import mask
from settings import WIDTH, HEIGHT
from particle import Particle
from utils import join, load_image, direction

pygame.init()


# subclasss (idk why I just wanted an extendable class)
class WeaponAim:
    def __init__(
        self,
        position: pygame.FRect,
        image: pygame.Surface,
        damage: float,
        speed: float,
        direction: pygame.Vector2,
    ) -> None:
        self.image = image
        self.mask = mask.from_surface(self.image)
        self.position = position
        self.damage = damage
        self.speed = speed
        self.direction = direction

        self.dead: bool = False

        # sfx
        self.sfx_rock_break: pygame.mixer.Sound = pygame.mixer.Sound(
            join("assets", "sfx", "rock-break.ogg")
        )
        self.sfx_rock_break.set_volume(0.8)

    def update(
        self,
        deltaTime: float,
        target,
        particle_list: list[Particle],
    ) -> None:
        overlapping = self.mask.overlap(
            target.animation.get_mask,
            (self.position.x - target.position.x, self.position.y - target.position.y),
        )

        if overlapping:
            target.health.health -= self.damage
            self.dead = True

            self.sfx_rock_break.play()

            for _ in range(0, 10):
                particle_list.append(
                    Particle(
                        "dark grey",
                        pygame.FRect(self.position.x, self.position.y, 15, 15),
                        pygame.Vector2(random.randint(-5, 5), -10),
                    )
                )

        self.position.x += self.direction.x * self.speed * deltaTime * 60
        self.position.y += self.direction.y * self.speed * deltaTime * 60

        # off-screen termination
        if (
            self.position.x - self.position.width > WIDTH
            or self.position.x + self.position.width < 0
            or self.position.y - self.position.height > HEIGHT
            or self.position.y + self.position.height < 0
        ):
            self.dead = True

            particle_list.append(
                Particle(
                    "dark grey",
                    pygame.FRect(self.position.x, self.position.y, 15, 15),
                    pygame.Vector2(random.randint(-5, 5), -10),
                )
            )

    def render(self, window) -> None:
        window.blit(self.image, self.position)
        # pygame.draw.rect(window, (255, 255, 255), self.position, 5) # TODO DELETEME

    def aimto(self, target: tuple[float, float], offset: float) -> None:
        # aim at the target
        target_x, target_y = target

        angle = direction(
            target_x, self.position.x, target_y, self.position.y - 50
        ) + math.radians(offset)

        self.direction.x = math.sin(angle)
        self.direction.y = math.cos(angle)

        # image rotation

        self.image = pygame.transform.rotate(self.image, math.degrees(angle) - 180)


class Rock(WeaponAim):
    def __init__(
        self,
        position: pygame.FRect,
        damage: float,
        speed: float,
        direction: pygame.Vector2,
    ) -> None:
        super().__init__(
            position,
            pygame.transform.scale(
                load_image(
                    join("assets", "ungabunga", "therock.png"), convert_alpha=True
                ),
                (100, 100),
            ),
            damage,
            speed,
            direction,
        )


class Poison:
    def __init__(
        self, position: tuple[float, float], direction_x: float, direction_y: float
    ) -> None:
        self.image = pygame.transform.scale(
            load_image(join("assets", "player", "poison.png"), convert_alpha=True),
            (100, 100),
        )
        self.mask = mask.from_surface(self.image)

        self.position = pygame.Vector2(*position)

        self.damage = 10

        self.acceleration = pygame.Vector2(0, 0.3)
        self.velocity = pygame.Vector2(direction_x, direction_y)

        self.dead: bool = False
        self.health_dead_buffer: float = 0

        # sfx
        self.sfx_splash_glass: pygame.mixer.Sound = pygame.mixer.Sound(
            join("assets", "sfx", "splash-glass.wav")
        )
        self.sfx_splash_glass.set_volume(0.25)

    def update(
        self,
        deltaTime: float,
        targets: list,
        particle_list: list[Particle],
    ) -> None:
        for target in targets:
            overlapping = self.mask.overlap(
                target.animation.get_mask,
                (
                    self.position.x - target.position.x,
                    self.position.y - target.position.y,
                ),
            )

            if overlapping:
                self.health_dead_buffer = target.health.health
                target.health.health -= self.damage
                self.dead = True

                self.sfx_splash_glass.play()

                for _ in range(0, 10):
                    particle_list.append(
                        Particle(
                            "dark green",
                            pygame.FRect(self.position.x, self.position.y, 15, 15),
                            pygame.Vector2(random.randint(-5, 5), -5),
                        )
                    )

        self.velocity += self.acceleration * deltaTime * 60
        self.position += self.velocity * deltaTime * 60

        # off-screen termination
        if (
            self.position.x - self.image.get_width() > WIDTH
            or self.position.x + self.image.get_width() < 0
            or self.position.y - self.image.get_height() > HEIGHT
            or self.position.y + self.image.get_height() < 0
        ):
            self.dead = True

    def render(self, window) -> None:
        window.blit(
            pygame.transform.rotate(
                self.image, self.velocity.y * (int(self.velocity.x < 0) * 2 - 1) * 2.5
            ),
            self.position,
        )
