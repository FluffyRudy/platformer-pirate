import pygame
from random import choice
from support import import_folder

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], idle_frames: list[pygame.Surface]):
        super().__init__()
        action_frames = import_folder('graphics/enemies/Sprites/Fierce Tooth/07-Attack')
        dead_frames = import_folder('graphics/enemies/Sprites/Fierce Tooth/09-Dead Hit')
        self.frames = {"idle": idle_frames, "attack": action_frames, "dead": dead_frames}
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = idle_frames[0]
        self.rect  = self.image.get_rect(topleft=pos)
        self.speed = choice([1, 2, 3]) * choice([-1, 1])
        self.left_boundry = pygame.Rect(0, 0, 0, 0) #only for initialization
        self.right_boundry = pygame.Rect(0, 0, 0, 0)
        self.action = "idle"
        self.change_direction()
        self.is_dead = False

    def move(self):
        self.rect.x += self.speed
    
    def update(self, world_shift):
        self.rect.x += world_shift
        self.animate()
        self.move()
        self.handle_boundry_collision()
        
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames[self.action]):
            if self.action == "attack":
                self.action = "idle"
            elif self.action == "dead":
              self.kill()
            self.frame_index = 0
        self.image = self.frames[self.action][int(self.frame_index)]
        
        if self.speed > 0:
            self.image = pygame.transform.flip(self.frames[self.action][int(self.frame_index)], 180, 0)
       

    def get_status(self):
        pass

    def change_direction(self):
        self.speed *= -1

    def handle_boundry_collision(self):
        if self.rect.colliderect(self.left_boundry) or self.rect.colliderect(self.right_boundry):
            self.change_direction()

    def assign_boundry(self, left: pygame.Rect, right: pygame.Rect):
        self.left_boundry = left
        self.right_boundry = right
    
    def trigger_attack(self):
        if self.action != "attack" and not self.is_dead:
            self.action = "attack"
            self.frame_index = 0
    
    def apply_kill_effect_and_kill(self):
      if self.action != "dead":
        self.action = "dead"
        self.frame_index = 0
        self.is_dead = True
        self.animation_speed = 0.1
        self.speed = 0

