import pygame
from settings import *
from random import randint, choice
from timer import Timer


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, scale=Scale, z=LAYERS['main']):
        super().__init__(groups)
        self.scale = scale
        self.image = surface
        # hitbox dramatically smaller on vertical because of overlap of player and sprites
        self.image = pygame.transform.scale(surface, (self.image.get_width() * scale, self.image.get_height() * scale))
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.15, -self.rect.height * 0.25)


class Interaction(Generic):
    def __init__(self, pos, size, groups, name):
        self.size = size * Scale
        surface = pygame.Surface(size)
        super().__init__(pos, surface, groups)
        self.name = name

class Water(Generic):
    def __init__(self, pos, frames, groups, scale=1):

        # Animate
        self._frames = frames
        self._frameIndex = 0
        self._animSpeed = 4
        
        # setup
        super().__init__(pos = pos, surface = self._frames[self._frameIndex], groups = groups, z = LAYERS['water'])
        self.scale = scale
        self.image = self._frames[self._frameIndex]
        # hitbox dramatically smaller on vertical because of overlap of player and sprites
        self.image = pygame.transform.scale(self._frames[self._frameIndex], (self.image.get_width() * scale, self.image.get_height() * scale))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.50, -self.rect.height * 0.1)
        # hitbox code for collision with water when it is sorted out scaling wise

    def animate(self, Deltatime):
        self._frameIndex += self._animSpeed * Deltatime
        if self._frameIndex >= len(self._frames):
            self._frameIndex = 0
        self.image = self._frames[int(self._frameIndex)]
        # GET WATER FRAMES SCALED X3

    def update(self, DeltaTime):
        self.animate(DeltaTime)

class Decoration(Generic):
    def __init__(self, pos, surface, groups):
        super().__init__(pos, surface, groups)
        self.hitbox = self.rect.copy().inflate(-self.rect.height * 0.5, -self.rect.height * 0.1)
        # same as generic for the while, will be adding functionality later

class Border(Generic):
    def __init__(self, pos, surface, groups, scale=1):
        super().__init__(pos, surface, groups)
        self.scale = scale
        self.image = surface
        # hitbox dramatically smaller on vertical because of overlap of player and sprites
        self.image = pygame.transform.scale(surface, (self.image.get_width() * scale, self.image.get_height() * scale))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy()
        # same as generic for the while except for scaling

class Particle(Generic):
    def __init__(self, pos, surface, groups, scale=3, z=LAYERS['main'],duration=200,item="plum"):
        super().__init__(pos, surface, groups, scale, z)
        self._StartTime = pygame.time.get_ticks()
        self._Duration = duration
        if item == "plum":
            self._Width = 16
            self._Height = 16
        elif item == "tree":
            self._Width = 24
            self._Height = 31
        else:
            self._Width = 16
            self._Height = 16
        MaskSurface = pygame.mask.from_surface(self.image)
        NewSurface = MaskSurface.to_surface()
        NewSurface = pygame.transform.scale(NewSurface,(self._Width*3,self._Height*3))
        NewSurface.set_colorkey((0,0,0))   
        self.image = NewSurface

    def update(self,DeltaTime):
        currentTime = pygame.time.get_ticks()
        if currentTime - self._StartTime > self._Duration:
            self.kill()


class Tree(Generic):
    def __init__(self, pos, surface, groups, name, playerAdd):  # name is for the type of tree, e.g small, large
        super().__init__(pos, surface, groups)
        self.hitbox = self.rect.copy().inflate(-self.rect.height * 0.4, -self.rect.height * 0.25)

        #tree features
        self._TreeHealth = 50
        self._Alive = True
        self._BrokenTreeSurface = pygame.image.load(f'../data/objects/027.png').convert_alpha()
        self._BrokenTreeSurface = pygame.transform.scale(self._BrokenTreeSurface, (10 * 3,10 * 3))
        self._InvulTimer = Timer(200)

        #plum
        self._PlumSurface = pygame.image.load('../textures/misc/plum.png')
        self._PlumPosition = PlumPos['Large']
        self._PlumSprites = pygame.sprite.Group()
        self.CreatePlum()

        self._PlayerAdd = playerAdd

    def BreakTree(self):
        self._TreeHealth -= 15
        if len(self._PlumSprites.sprites()) > 0:
            RandPlum = choice(self._PlumSprites.sprites())
            Particle(pos= RandPlum.rect.topleft,surface=RandPlum.image,groups=self.groups()[0], z=LAYERS['fruit'],item="plum")
            self._PlayerAdd('plum')
            RandPlum.kill()

    def CheckBreak(self):
        if self._TreeHealth <= 0:
            self._PlayerAdd('wood')
            Particle(pos=self.rect.topleft,surface=self.image,groups=self.groups()[0],z=LAYERS['fruit'],duration=200,item="tree")
            self.image = self._BrokenTreeSurface
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10,-self.rect.height * 0.6)
            self._Alive = False

    def update(self,DeltaTime):
        if self._Alive:
            self.CheckBreak()

    def CreatePlum(self):
        for pos in self._PlumPosition:
            if randint(0,10) < 2:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                Generic((x,y),self._PlumSurface,[self._PlumSprites,self.groups()[0]],z= LAYERS['fruit'])