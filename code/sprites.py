import pygame
from settings import *
from random import randint, choice
from timer import Timer

#Creation of the generic sprite class
class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, scale=Scale, z=LAYERS['main']):
        super().__init__(groups)
        #All sprites are scaled up times 3 so instead of of manaully adjusting the size of objects everywhere we just use this instance variable
        self.scale = scale
        #instance variable of the current surface
        self.image = surface
        # hitbox dramatically smaller on vertical because of overlap of player and sprites
        self.image = pygame.transform.scale(surface, (self.image.get_width() * scale, self.image.get_height() * scale))
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        # setting of player hitbox size - for collisions and interactions
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.15, -self.rect.height * 0.25)



# class for interactions with sprites (players and animals) 
# used when utilizing tools to ensure the player is within range for interaction to take place
class Interaction(Generic):
    def __init__(self, pos, size, groups, name, z=LAYERS['main']):
        self.size = size * Scale
        surface = pygame.Surface(size)
        super().__init__(pos, surface, groups)
        self.name = name
        self.z = z

# class for water sprite - extends generic class
#needed its own classes as it has animations for the water textures
class Water(Generic):
    def __init__(self, pos, frames, groups, scale=1):

        # Animate
        self._frames = frames # list of frames looped through to make the animation
        self._frameIndex = 0 # the starting position for looping throught the images
        self._animSpeed = 4 # the speed at which the animations are looped  through
        
        # setup
        super().__init__(pos = pos, surface = self._frames[self._frameIndex], groups = groups, z = LAYERS['water'])
        self.scale = scale
        self.image = self._frames[self._frameIndex]
        # hitbox dramatically smaller on vertical because of overlap of player and sprites
        self.image = pygame.transform.scale(self._frames[self._frameIndex], (self.image.get_width() * scale, self.image.get_height() * scale))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.50, -self.rect.height * 0.1)
        # hitbox code for collision with water when it is sorted out scaling wise

    #function for looping through the different images of the water to appear as if it is moving
    def animate(self, Deltatime):
        self._frameIndex += self._animSpeed * Deltatime
        if self._frameIndex >= len(self._frames):
            self._frameIndex = 0
        self.image = self._frames[int(self._frameIndex)]
        # GET WATER FRAMES SCALED X3

    #function to constantly call the animate method so that it loops forever whilst the game is being played
    def update(self, DeltaTime):
        self.animate(DeltaTime)

# Decoration class  - extends generic 
# for items such as rocks and flowers to give them a small hitbox
class Decoration(Generic):
    def __init__(self, pos, surface, groups):
        super().__init__(pos, surface, groups)
        self.hitbox = self.rect.copy().inflate(-self.rect.height * 0.5, -self.rect.height * 0.1)
        # same as generic for the while, will be adding functionality later

# Border class - extends generic
# used to give the map collisions which in turn keep the player in the intended sections of the map
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

# Particle class - extends generic
# used for animtions on plums and trees and crops when dissapearing
class Particle(Generic):
    def __init__(self, pos, surface, groups, scale=3, z=LAYERS['main'],duration=200,item="plum"):
        super().__init__(pos, surface, groups, scale, z)
        self._StartTime = pygame.time.get_ticks()
        self._Duration = duration
        if item == "plum":
            self._Width = 16
            self._Height = 16
        elif item == "tree-large":
            self._Width = 24
            self._Height = 31
        elif item == "tree-small":
            self._Width = 14
            self._Height = 28
        else:
            self._Width = 16
            self._Height = 16
        # displays the shape of the thing being broken in solid white for a split second 
        MaskSurface = pygame.mask.from_surface(self.image)
        NewSurface = MaskSurface.to_surface()
        NewSurface = pygame.transform.scale(NewSurface,(self._Width*3,self._Height*3))
        # removes the black background of the mask to just display the white
        NewSurface.set_colorkey((0,0,0))   
        self.image = NewSurface

    # update method to constantly update timers
    def update(self,DeltaTime):
        currentTime = pygame.time.get_ticks()
        if currentTime - self._StartTime > self._Duration:
            self.kill()

# Tree class - extends from generic
# Gives attributes to the trees - hitboxes, health, tree stump images, and plums
class Tree(Generic):
    def __init__(self, pos, surface, groups, name, playerAdd):  # name is for the type of tree, e.g small, large
        super().__init__(pos, surface, groups)
        self.hitbox = self.rect.copy().inflate(-self.rect.height * 0.4, -self.rect.height * 0.25)

        #tree features
        self._TreeHealth = 50 # tree health for when the user is breaking down the tree
        self._Alive = True # bool for checking if the user is broken or not 
        self._StumpPath =f'../data/objects/{"028" if name =="small" else "027"}.png' #if the tree is broken the image is replaced by a stump
        self._BrokenTreeSurface = pygame.image.load(self._StumpPath).convert_alpha()
        self._BrokenTreeSurface = pygame.transform.scale(self._BrokenTreeSurface, (10 * 3,10 * 3))
        self._InvulTimer = Timer(200)
        self._TreeName = name

        #plum
        self._PlumSurface = pygame.image.load('../textures/misc/plum.png')
        self._PlumPosition = PlumPos['large']
        self._PlumSprites = pygame.sprite.Group()
        self.CreatePlum()

        self._PlayerAdd = playerAdd

    # method for breaking the tree
    # it is called everytime the axe is registered to be hitting the tree
    def BreakTree(self):
        self._TreeHealth -= 15
        # conditional for checking if there is plums on the tree being interacted with
        if len(self._PlumSprites.sprites()) > 0:
            RandPlum = choice(self._PlumSprites.sprites())
            Particle(pos= RandPlum.rect.topleft,surface=RandPlum.image,groups=self.groups()[0], z=LAYERS['fruit'],item="plum")
            self._PlayerAdd('plum')
            RandPlum.kill()

    # method for checking if a tree is broken or not
    # it also called everytime the axe is registered to be hitting the tree
    def CheckBreak(self):
        # conditional which adds wood to the players inventory if they tree is broken
        if self._TreeHealth <= 0:
            self._PlayerAdd('wood')
            # conditional for checking which type of tree was broken and replacing the tree image with the corresponding stump image
            if self._TreeName == "small":
                self._TreeItem = "tree-small"
            elif self._TreeName == "large":
                self._TreeItem = "tree-large"
            Particle(pos=self.rect.topleft,surface=self.image,groups=self.groups()[0],z=LAYERS['fruit'],duration=200,item=self._TreeItem)
            # updating tree attributes - image, hitbox, and boolean for if its alive or not
            self.image = self._BrokenTreeSurface
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10,-self.rect.height * 0.6)
            self._Alive = False

    # method for constantly checking whether the tree is alive or not - if true the method to check if the tree is broken in called
    def update(self,DeltaTime):
        if self._Alive:
            self.CheckBreak()

    # method for randomly placing and generating plums on trees
    def CreatePlum(self):
        # conditional to check if the tree is alive before plaing any plums on the tree
        if self._Alive:
            for pos in self._PlumPosition:
                # conditional to randomly place plums in the specified locations
                if randint(0,10) < 2:
                    x = pos[0] + self.rect.left
                    y = pos[1] + self.rect.top
                    Generic((x,y),self._PlumSurface,[self._PlumSprites,self.groups()[0]],z= LAYERS['fruit'])