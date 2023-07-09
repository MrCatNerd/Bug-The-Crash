import pygame

pygame.init()


class HealthBar:
    def __init__(
        self, health: float, max_health: float, position: pygame.FRect, color
    ) -> None:
        self.position = position
        self.max_health = max_health
        self.health = health
        self.color = color

    def update(self, position: pygame.FRect) -> None:
        self.position = position

        self.health = min(self.health, self.max_health)  # to not create overflow

    def render(self, window) -> None:
        pygame.draw.rect(window, (50, 50, 50), self.position)
        pygame.draw.rect(
            window,
            self.color,
            (
                self.position.x,
                self.position.y,
                self.health / self.max_health * self.position.width,
                self.position.height,
            ),
        )
