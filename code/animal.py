from sprites import *
from settings import *


class Animal(Generic):
    def __init__(self, pos, surface, groups, scale=Scale, z=LAYERS['main']):
        super().__init__(pos, surface, groups, scale, z)
        self.scale = scale
        self.image = surface
        # hitbox dramatically smaller on vertical because of overlap of player and sprites
        self.image = pygame.transform.scale(surface, (self.image.get_width() * scale, self.image.get_height() * scale))
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.15, -self.rect.height * 0.25)
