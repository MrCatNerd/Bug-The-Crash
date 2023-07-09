import pygame

from settings import WIDTH, HEIGHT

pygame.init()


class Particle:
    def __init__(
        self,
        color: tuple[int, int, int],
        position: pygame.FRect,
        velocity: pygame.Vector2,
    ) -> None:
        self.position = position

        self.velocity = velocity
        self.acceleartion = pygame.Vector2(0, 0.3)

        self.color = color

        self.dead: bool = False

    def update(self, deltaTime: float) -> None:
        self.velocity += self.acceleartion * deltaTime * 60

        self.position.x += self.velocity.x * deltaTime * 60
        self.position.y += self.velocity.y * deltaTime * 60

        if (
            self.position.right > WIDTH
            or self.position.x < 0
            or self.position.bottom > HEIGHT
            or self.position.y < 0
        ):
            self.dead = True

    def render(self, window) -> None:
        pygame.draw.rect(window, self.color, self.position)
