import pygame

from settings import HEIGHT, WIDTH
from animation import Animation
from healthbar import HealthBar
from weapon import Poison
from particle import Particle
from utils import join

pygame.init()


class Player:
    def __init__(
        self,
        animations: dict[str:Animation],
        position: pygame.FRect,
        shoot_delay_ms: float,
    ) -> None:
        # money and upgrades and stats
        self.coins: int = 0
        self.upgrades: list[str] = [
            "none",
            "faster shooting",
            "health",
            "life steal",
            "end",
        ]
        self.current_upgrade = 0
        self.life_steal_percent: float = 0
        self.kills: int = 0

        # health
        self.health: HealthBar = HealthBar(
            500,
            500,
            pygame.FRect(
                position.x,
                position.y - 20,
                204.8,
                10,
            ),
            (20, 245, 35),
        )

        self.dead = False

        self.stage: int = 1

        # position
        self.position = position

        # animation
        self.animations: dict[str:Animation] = animations  # {name: Animation}
        self.direction_animation = False  # False: left, True: right
        self.idle: bool = (
            True  # True: idle animation, False: direction_animation conditions
        )

        # gravity
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0.35)

        # jumping
        self.jumping = False  # says if player is pressing the same key
        self.grounded = True  # says if player is on the ground

        # slowfall
        self.pressed_slowfall: bool = False
        self.slowfall_point: pygame.Vector2 = pygame.Vector2(
            self.position.x, self.position.y
        )
        self.slowfalling: bool = False

        # pew pew
        self.projectiles: list[Poison] = []
        self.direction = -2.5  # - left + right
        self.shoot_delay_ms = shoot_delay_ms
        self.current_shoot_delay_ms = self.shoot_delay_ms

        # sfx
        self.sfx_jump: pygame.mixer.Sound = pygame.mixer.Sound(
            join("assets", "sfx", "jump.wav")
        )
        self.sfx_jump.set_volume(0.2)

    def update(
        self,
        deltaTime: float,
        keys,
        mouse_pressed: bool,
        enemies: list,
        particle_list: list[Particle],
    ) -> None:
        # pew pew

        if (
            keys[pygame.K_SPACE]
            and self.current_shoot_delay_ms >= self.shoot_delay_ms
            and not self.dead
        ):
            self.projectiles.append(
                Poison(
                    (self.position.x, self.position.y),
                    self.direction,
                    -15,
                )
            )
            self.current_shoot_delay_ms = 0

        if self.current_shoot_delay_ms < self.shoot_delay_ms:
            self.current_shoot_delay_ms += deltaTime * 1000

        for projectile in self.projectiles:
            projectile.update(deltaTime, enemies, particle_list)

            if projectile.dead:
                self.health.health += projectile.health_dead_buffer * (
                    self.life_steal_percent / 100
                )
                self.projectiles.remove(projectile)

        # slowfall
        if mouse_pressed and not self.dead:
            if not self.pressed_slowfall:
                self.slowfall_point.x = self.position.x + self.position.width / 2
                self.slowfall_point.y = self.position.y
            self.pressed_slowfall = True
            self.slowfalling = True
        elif not mouse_pressed and self.slowfalling and not self.dead:
            self.slowfalling = False
            self.pressed_slowfall = False

        # gravity
        if self.slowfalling and self.position.y >= self.slowfall_point.y:
            self.velocity += self.acceleration * deltaTime * 60 * 0.2
            self.velocity.y = min(self.velocity.y, 2.5)
        else:
            self.velocity += self.acceleration * deltaTime * 60

        # movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a] and not self.dead:
            self.position.x -= deltaTime * 600 * (self.stage / 9)
            self.direction_animation = False
            self.idle = False
            self.direction = -2.5
        elif self.direction_animation == False:
            self.idle = True

        if keys[pygame.K_RIGHT] or keys[pygame.K_d] and not self.dead:
            self.position.x += deltaTime * 600 * (self.stage / 9)
            self.direction_animation = True
            self.idle = False
            self.direction = 2.5
        elif self.direction_animation == True:
            self.idle = True

        if (
            (keys[pygame.K_UP] or keys[pygame.K_w])
            and ((not self.jumping) and self.grounded)
            and not self.dead
        ):
            self.velocity.y = -15 * (1, 0.35)[int(self.slowfalling)]
            self.jumping = True

            # sfx
            self.sfx_jump.play()
        elif not (keys[pygame.K_UP] or keys[pygame.K_w]) and self.jumping:
            self.jumping = False

        # floor

        if self.position.y > HEIGHT - self.position.height:
            self.position.y = HEIGHT - self.position.height
            self.velocity.y = 0
            self.grounded = True
        else:
            self.grounded = False

        # say in screen
        if self.position.x > WIDTH:
            self.position.x = 0

        if self.position.x < -self.position.width:
            self.position.x = WIDTH - self.position.width

        # update position
        self.position.x += self.velocity.x * deltaTime * 60
        self.position.y += self.velocity.y * deltaTime * 60

        # animation
        self.animation.update(deltaTime)

        # health
        self.health.update(
            pygame.FRect(
                self.position.x,
                self.position.y - 20,
                204.8,
                10,
            )
        )

        if self.health.health <= 0:
            self.dead = True

        self.stage = self.health.max_health - self.health.health // 20
        self.stage = max(0, min(15, self.stage))

    def render(self, window) -> None:
        # pygame.draw.rect(window, (255, 255, 255), self.position, 5) # TODO remove me
        if self.slowfalling:
            pygame.draw.line(
                window,
                (221, 220, 211),
                self.slowfall_point,
                (self.position.x + self.position.width / 2, self.position.y),
                5,
            )

        for projectile in self.projectiles:
            projectile.render(window)

        self.animation.render(window, self.position)

        self.health.render(window)

    @property
    def animation(self) -> Animation:
        if self.idle:
            return self.animations["idle"]
        elif self.direction_animation:
            return self.animations["right"]
        elif not self.direction_animation:
            return self.animations["left"]
        else:
            raise ("The code is bad :(")
