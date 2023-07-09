import pygame

from utils import join

pygame.init()


class Button:
    def __init__(self, position: pygame.FRect, img, state: bool = None) -> None:
        if state is None:
            state = False

        self.state = state
        self.position = position

        self.img = img

        # technical
        self.pressed: bool = False
        self.hovered: bool = False

        # sfx
        self.sfx_click: pygame.mixer.Sound = pygame.mixer.Sound(
            join("assets", "sfx", "button-click.wav")
        )

    def update(self, mx: float, my: float, mouse_pressed) -> None:
        self.hovered = self.position.collidepoint(mx, my)

        if self.hovered and mouse_pressed[0] and not self.pressed:
            self.state = not self.state
            self.pressed = True

            # sfx
            self.sfx_click.play()
        elif not mouse_pressed[0] and self.pressed:
            self.pressed = False

    def reset(self) -> None:
        self.state = False

    def render(
        self,
        window,
        text: str = None,
        font: pygame.Font = None,
        aa: bool = None,
        text_color=None,
    ) -> None:
        window.blit(self.img, self.position)

        if not (text is None or font is None) and self.hovered:
            if aa is None:
                aa = False

            if text_color is None:
                text_color = "dark orange"

            window.blit(
                font.render(text, aa, text_color),
                (self.position.x, self.position.y + 50),
            )
