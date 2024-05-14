import os
import pygame

def import_folder(path: str):
    surf_list = []

    sorted_files = sorted(os.listdir(path))
    for file in sorted_files:
        image_path = os.path.join(os.path.abspath(path), file)
        image_surf = pygame.image.load(image_path).convert_alpha()
        surf_list.append(image_surf)

    return surf_list
