from typing import Any
from copy import deepcopy
from math import hypot
from settings import TILE_SIZE, SCREEN_WIDTH
import pygame
from tiles import Tile
from player import Player
from level_data import LevelData

class Level:
    def __init__(self, level_data: LevelData, surface: pygame.Surface):
        self.display_surface = surface

        self.terrain = level_data.get_terrain_data()
        self.terrain_group = pygame.sprite.Group(self.terrain)

        front_palm_tree = level_data.get_palm_tree_data()['front']
        back_palm_tree  = level_data.get_palm_tree_data()['back']
        self.front_palm_tree_group = pygame.sprite.Group(front_palm_tree)
        self.back_palm_tree_group  = pygame.sprite.Group(back_palm_tree)

        barrel = level_data.get_barrel_data()
        self.barrel_group = pygame.sprite.Group(barrel)
        

        coins = level_data.get_coins()
        self.coin_groups = pygame.sprite.Group(coins)

        river = level_data.get_river()
        self.river_group = pygame.sprite.Group(river)

        enemies = level_data.get_enemies()
        self.enemies_group = pygame.sprite.Group(enemies)
        self.enemy_constraints = level_data.get_enemies_boundries()

        self.player_start_end = level_data.get_start_end_rect()   
        player = Player(self.player_start_end[0].topright)
        self.player = pygame.sprite.GroupSingle(player)
        self.world_shift = 0
        self.scroll_start_pos = self.display_surface.get_width() // 3
        self.lower_bound = 0
        self.upper_bound = self.display_surface.get_width() - self.player_start_end[1].width

        level_data.get_river()
        self.assign_constraint_on_enemy()
        level_data.get_level_label()

        #score
        self.font = pygame.font.Font('font/font.ttf', 30)
        self.score_offset = self.player.sprite.get_player_info_ui_geometry()
        self.score = 0
        self.score_icon = pygame.image.load('graphics/ui/coin.png').convert_alpha()
        
    def run(self):
        self.update()

    def update(self):

        self.player.update()
        self.player.draw(self.display_surface)
        
        self.terrain_group.update(self.world_shift)
        self.terrain_group.draw(self.display_surface)

        self.front_palm_tree_group.update(self.world_shift)
        self.back_palm_tree_group.update(self.world_shift)
        self.front_palm_tree_group.draw(self.display_surface)
        self.back_palm_tree_group.draw(self.display_surface)

        self.barrel_group.update(self.world_shift)
        self.barrel_group.draw(self.display_surface)

        self.coin_groups.update(self.world_shift)
        self.coin_groups.draw(self.display_surface)

        self.river_group.update(self.world_shift)
        self.river_group.draw(self.display_surface)

        self.enemies_group.update(self.world_shift)
        self.enemies_group.draw(self.display_surface)

        self.scroll_x()
        self.display_score()
        self.goal_reached()

        self.horizontal_movement_collision()
        self.vertical_movement_collision()

        self.player_coin_collision()
        self.player_enemy_collision()

        for rect in self.enemy_constraints:
            rect.move_ip(self.world_shift, 0)
        for rect in self.player_start_end:
            rect.move_ip(self.world_shift, 0)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        self.world_shift = 0
        player.reset_speed()

        if (player_x < self.scroll_start_pos and direction_x < 0 and self.player_start_end[0].left < self.lower_bound) or \
        (player_x > self.scroll_start_pos and direction_x > 0 and self.player_start_end[1].left > self.upper_bound):
            self.world_shift = -direction_x * player.DEFAULT_SPEED
            player.speed = 0
        
        if (player_x < self.player_start_end[0].right and direction_x < 0):
            self.player.sprite.speed = 0
            self.player.sprite.rect.right = self.player_start_end[0].right
        elif (player_x > self.player_start_end[1].x and direction_x > 0):
            self.player.sprite.speed = 0
            self.player.sprite.rect.left = self.player_start_end[1].left
    
    def display_score(self):
        score = self.font.render(f'{self.score}', True, 'white')
        self.display_surface.blit(score, (int(self.score_offset[0] * 1.4), 0))
        self.display_surface.blit(self.score_icon, (int(self.score_offset[0] * 1.2), 10))

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += (player.direction.x * player.speed)
        collidable_sprites = self.front_palm_tree_group.sprites() + \
                             self.barrel_group.sprites() + \
                             self.terrain_group.sprites()

        
        for tile_sprite in collidable_sprites:
            if tile_sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = tile_sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = tile_sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.front_palm_tree_group.sprites() + \
                             self.barrel_group.sprites() + \
                             self.terrain_group.sprites()
                             

        for tile_sprite in collidable_sprites:
            if tile_sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = tile_sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = tile_sprite.rect.bottom
                    player.direction.y = player.gravity #to allow sprite to falldown with no delay
                

    def goal_reached(self):
        if self.player.sprite.rect.colliderect(self.player_start_end[1]):
            pass
    
    def left_right_nearest(self, src: pygame.Rect, points: list[pygame.Rect]):
        left_point = None
        right_point = None

        for point in points:
            if point.centerx < src.centerx and (left_point is None or point.centerx > left_point.centerx) and abs(point.bottom - src.top) <= TILE_SIZE:
                left_point = point
            elif point.centerx > src.centerx and (right_point is None or point.centerx < right_point.centerx) and abs(point.bottom - src.top) <= TILE_SIZE:
                right_point = point

        return left_point, right_point

    def assign_constraint_on_enemy(self):
        for sprite in self.enemies_group.sprites():
            left_boundry, right_boundry = self.left_right_nearest(sprite.rect, self.enemy_constraints)
            sprite.assign_boundry(left_boundry, right_boundry)
        
    def player_coin_collision(self):
        collided_coin =  pygame.sprite.spritecollideany(self.player.sprite, self.coin_groups)
        if collided_coin:
            collided_coin.apply_collide_effect_and_kill()
            self.score += collided_coin.value
            collided_coin.devalue()

    def player_enemy_collision(self):
        player = self.player.sprite
        collided_enemy = pygame.sprite.spritecollideany(player, self.enemies_group)
        if collided_enemy:
            enemy_center = collided_enemy.rect.centery
            enemy_top = collided_enemy.rect.top
            player_bottom = player.rect.bottom
            if enemy_top < player_bottom < enemy_center and player.direction.y >= 0:
              collided_enemy.apply_kill_effect_and_kill()
              player.jump()
            else:
                player.get_damage()
