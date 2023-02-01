from os import walk
import pygame

# Function to import images in folder and convert them into surfaces
def import_folder(path):
    surface_list = []

    for _, __, images in walk(path):
        for image in images:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)

    return surface_list