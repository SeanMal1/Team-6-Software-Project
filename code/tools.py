from os import walk
import pygame
from sprites import Generic

# Function to import images in folder and convert them into surfaces
def import_folder(path):
    surface_list = []
    scale = 3

    for _, __, images in walk(path):
        for image in images:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            image_surface = pygame.transform.scale(image_surface, (image_surface.get_width() * scale, image_surface.get_height() * scale))
            surface_list.append(image_surface)

    return surface_list