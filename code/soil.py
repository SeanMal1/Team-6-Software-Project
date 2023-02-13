import pygame
from settings import *

class SoilLayer:
    def  __init__(self, _AllSprites):

        # Sprite Groups
        self._AllSprites = _AllSprites
        self.soil_sprites = pygame.sprite.Group()

        # Graphics