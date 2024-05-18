import pygame
from pygame.math import Vector2
from game_data import levels, AVILABLE, NOT_AVILABLE, NODE_WIDTH, NODE_HEIGHT

class Overworld:
    def __init__(self, start_level: int, max_level: int, surface: pygame.Surface):
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.nodes = pygame.sprite.Group()
        self.icon = pygame.sprite.GroupSingle()

        self.direction = 0
        self.speed = 4
        self.moving = False

        self.setup_nodes()
        self.setup_icons()

    def setup_nodes(self):
        for level, node_data in enumerate(levels.values()):
            if level <= self.max_level:
                node_sprite = Node(node_data['node_pos'], AVILABLE)
                self.nodes.add(node_sprite)
            else:
                node_sprite = Node(node_data['node_pos'], NOT_AVILABLE)
                self.nodes.add(node_sprite)
    
    def setup_icons(self):
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def draw_nodes_path(self):
        path_points = [
            node["node_pos"] for idx, node in enumerate(levels.values()) 
            if idx <= self.max_level
        ]
        pygame.draw.lines(self.display_surface, "red", False, path_points, 5)

    def take_input(self):
        keys = pygame.key.get_pressed()
        
        if not self.moving and keys[pygame.K_RIGHT]:
            self.moving = True
            self.direction = 1
            self.current_level = min(self.current_level + 1, self.max_level)
        elif not self.moving and keys[pygame.K_LEFT]:
            self.direction = -1
            self.moving = True
            self.current_level = max(0, self.current_level - 1)
    
    def update(self):
        cur_x, cur_y = self.icon.sprite.rect.center
        des_x, des_y = self.nodes.sprites()[self.current_level].rect.center

        if self.moving and self.direction > 0 and cur_x < des_x:
            self.icon.sprite.rect.x += self.speed
        elif self.moving and self.direction < 0 and cur_x > des_x:
            self.icon.sprite.rect.x -= self.speed
        else:
            self.moving = False

    def run(self):
        self.draw_nodes_path()
        self.nodes.draw(self.display_surface)
        self.nodes.update(self.display_surface)
        self.icon.draw(self.display_surface)
        self.take_input()
        self.update()
    

    
class Node(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], status: int):
        super().__init__()
        self.image = pygame.Surface((NODE_WIDTH, NODE_HEIGHT))
        self.rect = self.image.get_rect(center=pos)
        self.color = pygame.Color("red") if status else pygame.Color("grey")
    
    def update(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=5)

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill("blue")
        self.rect = self.image.get_rect(center=pos)