import pygame
from settings import *
from random import randint


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, scale=3, z=LAYERS['main']):
        super().__init__(groups)
        self.scale = scale
        self.image = surface
        # hitbox dramatically smaller on vertical because of overlap of player and sprites
        self.image = pygame.transform.scale(surface, (self.image.get_width() * scale, self.image.get_height() * scale))
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.15, -self.rect.height * 0.1)




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
        self.hitbox = self.rect.copy().inflate(-self.rect.height * 0.5, -self.rect.height * 0.1)
        # same as generic for the while, will be adding functionality later

class Tree(Generic):
    def __init__(self, pos, surface, groups, name):  # name is for the type of tree, e.g small, large
        super().__init__(pos, surface, groups)
        self.hitbox = self.rect.copy().inflate(-self.rect.height * 0.4, -self.rect.height * 0.25)

        #plum
        self._PlumSurface = pygame.image.load('../textures/misc/plum.png')
        self._PlumPosition = PlumPos['Large']
        self._PlumSprites = pygame.sprite.Group()
        self.CreatePlum()

    def CreatePlum(self):
        for pos in self._PlumPosition:
            if randint(0,10) < 2:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                Generic((x,y),self._PlumSurface,[self._PlumSprites,self.groups()[0]],z= LAYERS['fruit'])