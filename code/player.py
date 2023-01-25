import pygame
from settings import *


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.Surface((48,54))
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)
        self._SpriteSheetImage = pygame.image.load('textures/player.png').convert_alpha()
        #moving attribute
        self._Direction = pygame.math.Vector2()
        self._Position = pygame.math.Vector2(self.rect.center)
        self._Speed = 110

    
    

    def getImage(self,sheet,width,height,scale):
        self._Spriteimage = pygame.Surface((width, height)).convert_alpha()
        self._Spriteimage.blit(sheet, (0,0), (0, 0, width, height))
        self._Spriteimage = pygame.transform.scale(self._Spriteimage, (width *scale, height *scale))
        return self._Spriteimage




    def importAssets(self):
        self._Animations = {'up':[],'down':[],'left':[],'right':[]}

    def input(self):
        keystroke = pygame.key.get_pressed()
        if keystroke[pygame.K_w]:
            self._Direction.y = -1
        elif keystroke[pygame.K_s]:
            self._Direction.y = 1
        else:
            self._Direction.y = 0

        if keystroke[pygame.K_a]:
            self._Direction.x = -1
        elif keystroke[pygame.K_d]:
            self._Direction.x = 1
        else:
            self._Direction.x = 0
        
    def move(self,DeltaTime):
        #normalize vector (cant speed up by holding w and a or w and d and so on)
        if self._Direction.magnitude() > 0:
            self._Direction = self._Direction.normalize()

        #movement on x axis
        self._Position.x += self._Direction.x * self._Speed * DeltaTime
        self.rect.centerx = self._Position.x

        #movement on y axis
        self._Position.y += self._Direction.y * self._Speed * DeltaTime
        self.rect.centery = self._Position.y

    def update(self,DeltaTime):
        self.input()
        frame0 = self.getImage(self._SpriteSheetImage,16,18,3)
        self.image.blit(frame0, (0,0))
        self.move(DeltaTime)