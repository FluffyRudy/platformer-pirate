import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill("gray")
        self.rect  = self.image.get_rect(topleft=pos)

    def update(self, x_shift: int):
        self.rect.x += x_shift
