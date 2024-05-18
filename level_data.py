import sys, os
import pygame
from pytmx import TiledMap, TiledTileLayer, TiledObject
from pytmx import load_pygame
from tiles import Tile
from palmtree import PalmTree
from barrel import Barrel
from coin import Coin
from enemy import Enemy
from river import River
from collections import deque
from typing import Union, NoReturn, Optional

#level filename must be in format level_{n}/level_{n}.tmx
class LevelData:
    def __init__(self, level: int):
        self.__level_id = level
        self.__map_data: Union[None, TiledMap] = None
        self.__get_map_data()
        self.__map_size = self.__calculate_map_size()
    
    def __calculate_map_size(self):
        num_tile_cols = self.__map_data.width
        num_tile_rows = self.__map_data.height
        tile_width = self.__map_data.tilewidth
        tile_height = self.__map_data.tileheight
        return int(tile_width * num_tile_cols), int(tile_height * num_tile_rows)

    def __get_map_data(self) -> Optional[NoReturn]:
        try:
            path = os.path.join(f'map/level_{self.__level_id}', f'level_{self.__level_id}.tmx')
            self.__map_data = load_pygame(path)
        except FileNotFoundError:
            print("File not found...")
            print('Exiting gracefully')
            sys.exit()

    def __get_layernames(self) -> list[str]:
        return list(self.__map_data.layernames.keys())

    def __get_layer_data_by_name(self, name: str) -> TiledTileLayer:
        return self.__map_data.layernames[name]
    
    def __get_image_by_gid(self, gid: int) -> pygame.Surface:
        return self.__map_data.get_tile_image_by_gid(gid)
    
    def get_map_size(self):
        return self.__map_size
    
    def __create_animated_instances(self, layer, parent):
        animated_instances = deque()
        for data in layer:
            properties = self.__map_data.get_tile_properties_by_gid(data.gid)
            pos = int(data.x), int(data.y)
            image = self.__get_image_by_gid(data.gid)
            frames = [self.__get_image_by_gid(frame.gid) for frame in properties['frames']]
            if len(frames) == 0:
                frames.append(image)
            instance = parent(pos, frames)
            animated_instances.append(instance)
        return animated_instances

    def get_start_end_rect(self):
        start_end_layer = self.__get_layer_data_by_name('PlayerRange')
        start_end_rect = deque()

        for data in start_end_layer:
            x, y, gid = int(data.x), int(data.y), data.gid
            image_rect = self.__get_image_by_gid(gid).get_rect(topleft=(x, y))
            start_end_rect.append(image_rect)
        
        return start_end_rect

    def get_terrain_data(self):
        terrain_layer: TiledTileLayer = self.__get_layer_data_by_name('Terrain')
        tiles = deque()
        for x, y, gid in terrain_layer.iter_data():
            image = self.__get_image_by_gid(gid)
            if image:
                tile = Tile((x * image.get_width(), y*image.get_height()), image)
                tiles.append(tile)
        return tiles

    def get_barrel_data(self):
        barrels = deque()
        barrel_layer: list[TiledObject] = self.__get_layer_data_by_name('Barrel')
        
        for barrel in barrel_layer:
            pos = int(barrel.x), int(barrel.y)
            image = self.__get_image_by_gid(barrel.gid)
            barrels.append(Barrel(pos, image))
        return barrels

    def get_palm_tree_data(self):
        palm_tree = {
            "front": self.__get_layer_data_by_name('PalmTreeFront'),
            "back": self.__get_layer_data_by_name('PalmTreeBack')
        }
        return {
            "front": self.__create_animated_instances(palm_tree['front'], PalmTree),
            "back": self.__create_animated_instances(palm_tree['back'], PalmTree)
        }
                
    def get_coins(self):
        coin_layer = self.__get_layer_data_by_name('Coins')
        return self.__create_animated_instances(coin_layer, Coin)
    
    def get_enemies(self):
        enemies_layer = self.__get_layer_data_by_name('Enemies')
        return self.__create_animated_instances(enemies_layer, Enemy)

    def get_enemies_boundries(self):
        boundry_layer: TiledObject = self.__get_layer_data_by_name("EnemyBoundry")
        boundry_rects = deque()

        for data in boundry_layer:
            pos = int(data.x), int(data.y)
            image = self.__get_image_by_gid(data.gid)
            if image:
                rect = image.get_rect(topleft=pos)
                boundry_rects.append(rect)
        
        return boundry_rects

    def get_river(self):
        river_layer = self.__get_layer_data_by_name("River")
        return self.__create_animated_instances(river_layer, River)