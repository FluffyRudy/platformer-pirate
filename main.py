import sys
from settings import *
import pygame
from pygame.sprite import Group, GroupSingle
from level import Level
from overworld import Overworld
from level_data import LevelData
from game_data import levels

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.FPS = FPS

        self.max_level = 3
        self.overworld = Overworld(start_level=0, max_level=self.max_level, surface=self.screen)

        level_data = LevelData(level=0)
        self.level = Level(level_data, self.screen) 

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    def run(self):
        while True:
            self.handle_event()
            self.screen.fill(pygame.Color(0, 0, 0, 0))
            self.level.run()
            pygame.display.update()
            self.clock.tick(self.FPS)

def main():
    pygame.init()
    game = Game()
    game.run()

if __name__ == "__main__":
    main()