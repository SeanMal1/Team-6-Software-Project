from os import walk
import pygame
from sprites import Generic
from settings import *

# Function to import images in folder and convert them into surfaces
def import_folder(path):
    surface_list = []

    for _, __, images in walk(path):
        for image in images:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            image_surface = pygame.transform.scale(image_surface, (image_surface.get_width() * Scale, image_surface.get_height() * Scale))
            surface_list.append(image_surface)

    return surface_list

def import_folder_unscaled(path):
    surface_list = []

    for _, __, images in walk(path):
        for image in images:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)

    return surface_list

def import_folder_dict(path):
    surface_dict = {}

    for _, __, images in walk(path):
        for image in images:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            # image_surface = pygame.transform.scale(image_surface, (image_surface.get_width() * Scale, image_surface.get_height() * Scale))
            surface_dict[image.split('.')[0]] = image_surface

    return surface_dict
