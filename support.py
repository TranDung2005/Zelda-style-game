import pygame
from csv import reader
from os import walk
pygame.init()

def import_csv_layout(path):
    terrain_map = []
    layout = reader(open(path), delimiter=",")
    for row in layout:
        terrain_map.append(row)

    return(terrain_map)

def import_imgs_list(path):
    imgs_list = []
    for _,__,imgs_files in walk(path):
        for img in imgs_files:
            full_path = f'{path}/{img}'
            img_surf = pygame.image.load(full_path).convert_alpha()
            imgs_list.append(img_surf)

    return(imgs_list)
