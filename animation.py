import pygame

pygame.init()


class Animation:
    def __init__(self, frames: list[pygame.Surface], delay_ms: float) -> None:
        # frame
        self.frames: list[pygame.Surface] = frames
        self.current_frame = 0

        # outlines and bitmasks
        self.bitmasks: list[pygame.Mask] = []
        for frame in self.frames:
            self.bitmasks.append(pygame.mask.from_surface(frame))

        # delay
        self.current_time_ms: float = 0
        self.delay_ms: float = delay_ms

    def update(self, deltaTime: float) -> None:
        self.current_time_ms += deltaTime * 1000

        if self.current_time_ms >= self.delay_ms:
            self.current_time_ms = 0
            self.current_frame += 1

        self.current_frame %= len(self.frames)

    def render(self, window, position: pygame.FRect) -> None:
        # draw
        window.blit(self.frames[self.current_frame], position)

        # outline
        mask = self.bitmasks[self.current_frame]
        pts = mask.outline()
        new_pts: list[list[int]] = []

        for pt in pts:
            new_pts.append([pt[0] + position.x, pt[1] + position.y])

        pygame.draw.lines(window, "dark grey", False, new_pts, 2)

    @property
    def get_mask(self) -> pygame.Mask:
        return self.bitmasks[self.current_frame]
