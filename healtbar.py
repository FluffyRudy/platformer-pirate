import pygame
from pygame.math import Vector2

class Healthbar:
    INNER_COLOR = "red"
    def __init__(self,
        size: tuple[int, int], 
        initial_health: int, 
        color="white", 
        border_thickness=0, 
        border_radius=3):
        self.max_health = initial_health
        self.current_health = initial_health
        self.new_health = initial_health
        self.image = pygame.Surface((size))
        self.width = size[0]
        self.height = size[1]
        self.transition_speed = 2
        self.indicator = 0
        self.color = color
        self.display_position = (0, 0)
        self.border_radius = border_radius
        self.border_thickness = border_thickness

    def update(self, display_position: tuple[int, int]):
        if self.current_health != self.new_health:
            self.current_health += (self.indicator * self.transition_speed)
        self.display_position = Vector2(display_position) - (self.width//2, self.height)

    def draw(self, display_surface: pygame.Surface):
        pygame.draw.rect(self.image, self.INNER_COLOR, (0, 0, self.width, self.height), self.border_thickness, self.border_radius*2)
        pygame.draw.rect(self.image, self.color, (0, 0, self.current_health, self.height), self.border_thickness, self.border_radius*2)
        display_surface.blit(self.image, self.display_position)

    def update_health(self, new_health:int ):
        new_health = self.new_health + new_health 
        self.new_health = min(max(new_health, 0), self.max_health)
        if self.current_health < self.new_health:
            self.indicator = 1
        elif self.current_health > self.new_health:
            self.indicator = -1
        else:
            self.indicator = 0

    def get_current_health(self):
        return self.current_health
