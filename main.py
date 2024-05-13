import sys
from settings import *
import pygame
from pygame.sprite import Group, GroupSingle
from tiles import Tile
from level import Level

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.FPS = FPS
        self.level = Level(level_map, self.screen) 

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    def run(self):
        while True:
            self.handle_event()
            self.screen.fill("black")
            self.level.run(self.screen)
            pygame.display.update()
            self.clock.tick(self.FPS)

def main():
    pygame.init()
    game = Game()
    game.run()

if __name__ == "__main__":
    main()