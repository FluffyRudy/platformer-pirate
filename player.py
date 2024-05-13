from settings import TILE_SIZE
import pygame
from pygame.math import Vector2


class Player(pygame.sprite.Sprite):
    DEFAULT_SPEED = 8
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE*2))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = pos)
        
        self.direction = Vector2(0, 0)
        self.speed = self.DEFAULT_SPEED
        self.gravity = 0.8
        self.jump_speed = -16

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        
        if keys[pygame.K_UP]:
            self.jump()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()

    def reset_speed(self):
        self.speed = Player.DEFAULT_SPEED
    
