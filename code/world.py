import pygame
from settings import *
from player import Player

class Level:
    def __init__(self):
        self._DisplayWorld = pygame.display.get_surface()
        self._AllSprites = pygame.sprite.Group()
        self.setup()
        self._SpriteSheetImage = pygame.image.load('textures/player.png').convert_alpha()

    def setup(self):
        self._Player = Player((640,360), self._AllSprites)

    def run(self,DeltaTime):
        self._DisplayWorld.fill('black')
        self._AllSprites.draw(self._DisplayWorld)
        self._AllSprites.draw(self._SpriteSheetImage)
        self._AllSprites.update(DeltaTime)