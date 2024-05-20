import pygame
from pygame.math import Vector2
from support import import_folder

class Healthbar:
    INNER_COLOR = "red"
    def __init__(self,
        color="white", 
        border_thickness=0, 
        border_radius=3):
        #__init__
        # Load the image onto a surface
        self.image_surface = pygame.image.load('graphics/ui/health_bar.png').convert_alpha()
        self.image = pygame.Surface(self.image_surface.get_size(), pygame.SRCALPHA)

        self.rect = self.image.get_rect(topleft=(0, 0))

        self.transition_speed = 2
        self.indicator = 0
        self.color = color
        self.border_radius = border_radius
        self.border_thickness = border_thickness
        self.vertical_offset = 10
        self.x, self.y = 32, 15
        self.w, self.h = self.rect.width - self.x - 4, 5
        self.max_health = self.w
        self.current_health = self.w
        self.new_health = self.w

        self.uniform_damage = self.max_health // 5 #till 5 times player can take damage

    def update(self):
        if self.current_health != self.new_health:
            self.current_health += (self.indicator * self.transition_speed)
            # Check for overshoot
            if self.indicator == 1 and self.current_health > self.new_health:
                self.current_health = self.new_health
            elif self.indicator == -1 and self.current_health < self.new_health:
                self.current_health = self.new_health

    def draw(self, display_surface: pygame.Surface):
        pygame.draw.rect(self.image, "green", (self.x, self.y+self.vertical_offset, self.current_health, self.h), 0, self.border_radius)
        display_surface.blit(self.image, self.rect.topleft)
        self.image.blit(self.image_surface, (0, self.vertical_offset))

    def update_health(self, new_health: int):
        new_health = self.new_health + new_health 
        self.new_health = min(max(new_health, 1), self.max_health)
        if self.current_health < self.new_health:
            self.indicator = 1
        elif self.current_health > self.new_health:
            self.indicator = -1
        else:
            self.indicator = 0

    def get_current_health(self):
        return self.current_health
