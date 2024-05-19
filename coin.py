import pygame
from support import import_folder

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int],  frames: list[pygame.Surface]):
        super().__init__()
        self.frames = {"idle": frames, "collected": import_folder("graphics/treasure/coin-effect")}
        self.frame_index = 0
        self.animation_speed = 0 if len(frames) == 0 else 0.1
        self.status = "idle"
        self.image = self.frames[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

    def animation(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames[self.status]):
            if self.status == "collected":
              self.kill()
            self.frame_index = 0
        self.image = self.frames[self.status][int(self.frame_index)]
        if self.status == "collected":
          self.image = pygame.transform.scale2x(self.image)

    def update(self, world_shift):
        self.rect.x += world_shift
        self.animation()
      
    def apply_collide_effect_and_kill(self):
      if self.status != "collected":
        self.status = "collected"
        self.frame_index = 0
