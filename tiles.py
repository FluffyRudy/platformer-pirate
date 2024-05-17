import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], image: pygame.Surface):
        super().__init__()
        self.image = image
        self.rect  = self.image.get_rect(topleft=pos)

    def update(self, world_shift):
        self.rect.x += world_shift
