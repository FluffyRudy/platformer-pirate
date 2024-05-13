from typing import Any
from settings import TILE_SIZE, SCREEN_WIDTH
import pygame
from tiles import Tile
from player import Player

class Level:
    def __init__(self, level_data: Any, surface: pygame.Surface):
        self.display_surface = surface
        self.left_scroll_x = SCREEN_WIDTH // 5
        self.right_scroll_x = SCREEN_WIDTH - self.left_scroll_x
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.world_shift = 0
        self.setup_level(level_data)
    
    def setup_level(self, layout: Any):
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(layout[row_index]):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'P':
                    player = Player((x, y))
                    self.player.add(player)
                if col == 'X':
                    tile =  Tile((x, y), (TILE_SIZE, TILE_SIZE))
                    self.tiles.add(tile)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < self.left_scroll_x and direction_x < 0:
            self.world_shift = player.DEFAULT_SPEED
            player.speed = 0
        elif player_x > self.right_scroll_x and direction_x > 0:
            self.world_shift = -player.DEFAULT_SPEED
            player.speed = 0
        else:
            self.world_shift = 0
            player.reset_speed()
    
    def horizontal_movement_collision(self):
        player = self.player.sprite
        
            
    def draw(self, surface: pygame.Surface):
        self.tiles.update(self.world_shift)
        self.player.update()
        self.scroll_x()

        self.tiles.draw(surface)
        self.player.draw(surface)