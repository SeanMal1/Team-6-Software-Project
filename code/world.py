import pygame
import json
from settings import *
from player import Player

class Level:
    def __init__(self):
        self._saveFile = json.load(open("profiles/save1.json", "r"))
        self._DisplayWorld = pygame.display.get_surface()
        self._AllSprites = pygame.sprite.Group()
        self.setup()
        self._SpriteSheetImage = pygame.image.load(self._saveFile['image']).convert_alpha()

    def setup(self):
        self._Player = Player((self._saveFile['position']['x'], self._saveFile['position']['y']), self._AllSprites)

    def run(self,DeltaTime):
        self._DisplayWorld.fill('black')
        self._AllSprites.draw(self._DisplayWorld)
        self._AllSprites.draw(self._SpriteSheetImage)
        self._AllSprites.update(DeltaTime)