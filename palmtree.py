import pygame
from random import choice

class PalmTree(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int],  frames: list[pygame.Surface]):
        super().__init__()
        self.frames: list[pygame.Surface] = frames
        self.frame_index = 0
        self.animation_speed = 0 if len(frames) == 0 else choice([0.05, 0.08, 0.1, 0.15, 0.2])
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

    def animation(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, world_shift):
        self.rect.x += world_shift
        self.animation()
        # pygame.draw.rect(pygame.display.get_surface(), "red", self.rect)
