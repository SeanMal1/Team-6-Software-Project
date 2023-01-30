import pygame
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, scale = 3, z = LAYERS['main']):
        super().__init__(groups)
        self.scale = scale
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.image = pygame.transform.scale(surface, (self.image.get_width() *scale, self.image.get_height() * scale))
