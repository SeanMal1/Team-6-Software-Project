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

class Water(Generic):
    def __init__(self, pos, frames, groups):
        
        # Animate
        self.frames = frames
        self.frame_index = 0
        
        # setup
        super().__init__(
                pos = pos,
                surface = self.frames[self.frame_index],
                groups = groups,
                z = LAYERS['water'])