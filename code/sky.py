import pygame
from settings import *
from tools import *
from sprites import Generic
from random import randint, choice

class Drop(Generic):
    def __init__(self, surface, pos, moving, groups, z):
        super().__init__(pos, surface, groups, z)
        self.lifetime = randint(400,500)
        self._StartTime = pygame.time.get_ticks()

        # moving
        self.moving = moving
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2,4)
            self.speed = randint(200, 1000)

    def update(self, DeltaTime):
        # movement
        if self.moving:
            self.pos += self.direction * self.speed * DeltaTime
            self.rect.topleft = (round(self.pos.x), (round(self.pos.y)))

        # timer
        if pygame.time.get_ticks() - self._StartTime >= self.lifetime:
            self.kill()

class Rain:
    def __init__(self, _AllSprites):
        self._AllSprites = _AllSprites
        self._RainDrops = import_folder_unscaled('../textures/rain/drops')
        self._RainSplash = import_folder_unscaled('../textures/rain/floor')
        self._FloorWidth, self._FloorHeight = pygame.image.load('../data/Farm.png').get_size()
        self._FloorWidth = self._FloorWidth * Scale
        self._FloorHeight = self._FloorHeight * Scale

    def create_splash(self):
        Drop(
            surface=choice(self._RainSplash),
            pos=(randint(0, self._FloorWidth), randint(0, self._FloorHeight)),
            moving=False,
            groups=self._AllSprites,
            z=LAYERS['rain floor']
        )
    def create_drops(self):
        Drop(
            surface=choice(self._RainDrops),
            pos=(randint(0, self._FloorWidth), randint(0, self._FloorHeight)),
            moving=True,
            groups=self._AllSprites,
            z=LAYERS['rain drops']
        )

    def update(self):
        self.create_splash()
        self.create_drops()
