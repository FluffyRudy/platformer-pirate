from settings import TILE_SIZE
import pygame
from pygame.math import Vector2
import os
from support import import_folder

class Player(pygame.sprite.Sprite):
    DEFAULT_SPEED = 4
    def __init__(self, pos: tuple[int, int]):
        super().__init__()

        self.display_surface = pygame.display.get_surface()

        self.frame_index = 0
        self.animation_speed = 0.2
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}
        self.import_character_assets()

        self.dust_frame_index = 0
        self.dust_run_particles = []
        self.import_dust_run_particles()

        self.status = 'idle'
        self.facing_right = True

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        
        self.direction = Vector2(0, 0)
        self.speed = self.DEFAULT_SPEED
        self.gravity = 0.4
        self.jump_speed = -12

    def import_character_assets(self):
        character_path = 'graphics/player/'
        for animation in self.animations:
            full_path = os.path.join(character_path, animation)
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        dust_run_particles_path = 'graphics/dust_particles/run/'
        self.dust_run_particles = import_folder(dust_run_particles_path)

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        frame = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = frame
        else:
            self.image = pygame.transform.flip(frame, True, False)
        midbottom = self.rect.midbottom
        self.rect = self.image.get_rect(midbottom=midbottom)
    
    def run_dust_animation(self):
        if self.status == 'run':
            self.dust_frame_index += self.animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]
            position = (self.rect.centerx - self.direction.x * dust_particle.get_width(), self.rect.bottom - dust_particle.get_height()) 
            self.display_surface.blit(dust_particle, (position))

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
        
        if keys[pygame.K_UP] and self.direction.y == 0:
            self.jump()

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > self.gravity:
            self.status = 'fall'
        elif self.direction.x != 0:
            self.status = 'run'
        else:
            self.status = 'idle'
        return self.status

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()

    def reset_speed(self):
        self.speed = Player.DEFAULT_SPEED
    