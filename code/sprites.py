import pygame
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, scale = 3, z = LAYERS['main']):
        super().__init__(groups)
        self.scale = scale
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.image = pygame.transform.scale(surface, (self.image.get_width() * scale, self.image.get_height() * scale))

class Water(Generic):
    def __init__(self, pos, frames, groups):
        
        # Animate
        self._frames = frames
        self._frameIndex = 0
        self._animSpeed = 4
        
        # setup
        super().__init__(
                pos = pos,
                surface = self._frames[self._frameIndex],
                groups = groups,
                z = LAYERS['water'])

    def animate(self, Deltatime):
        self._frameIndex += self._animSpeed * Deltatime
        if self._frameIndex >= len(self._frames):
            self._frameIndex = 0
        self.image = self._frames[int(self._frameIndex)]
        # GET WATER FRAMES SCALED X3

    def update(self, deltaTime):
        self.animate(deltaTime)

class Decoration(Generic):
    def __init__(self, pos, surface, groups):
        super().__init__(pos, surface, groups)
        # same as generic for the while, will be adding functionality later