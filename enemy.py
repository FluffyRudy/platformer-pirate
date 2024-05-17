import pygame
from random import choice

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], frames: list[pygame.Surface]):
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = frames[0]
        self.rect  = self.image.get_rect(topleft=pos)
        self.speed = choice([1, 2, 3]) * choice([-1, 1])
        self.change_direction()

    def move(self):
        self.rect.x += self.speed
    
    def update(self, world_shift):
        self.rect.x += world_shift
        self.animate()
        self.move()

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

    def get_status(self):
        pass

    def change_direction(self):
        self.speed *= -1

        if self.speed > 0:
            self.image = pygame.transform.flip(self.frames[int(self.frame_index)], 180, 0)
        elif self.speed < 0:
            self.image = pygame.transform.flip(self.frames[int(self.frame_index)], 0, 0)




