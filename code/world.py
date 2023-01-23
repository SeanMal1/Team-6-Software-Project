import pygame
from settings import *

class Level:
    def __init__(self):
        self._DisplayWorld = pygame.display.get_surface()
        self._AllSprites = pygame.sprite.Group()

    def run(self,DeltaTime):
        self._DisplayWorld.fill('black')
        self._AllSprites.draw(self._DisplayWorld)
        self._AllSprites.update()