import pygame
from settings import *
from player import Player

class Level:
    def __init__(self):
        self._DisplayWorld = pygame.display.get_surface()
        self._AllSprites = CameraGroup()
        self.setup()
        self._SpriteSheetImage = pygame.image.load('../textures/player.png').convert_alpha()

    def setup(self):
        self._Player = Player((640,360), self._AllSprites)

    def run(self, DeltaTime):
        self._DisplayWorld.fill('black')
        # self._AllSprites.draw(self._DisplayWorld)
        self._AllSprites.custom_draw()
        self._AllSprites.draw(self._SpriteSheetImage)
        self._AllSprites.update(DeltaTime)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self):
        for sprite in self.sprites():
            self.display_surface.blit(sprite.image, sprite.rect)
