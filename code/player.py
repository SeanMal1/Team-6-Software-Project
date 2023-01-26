import pygame
import json
from settings import *


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.Surface((48,54))

        self._saveFile = json.load(open("../profiles/save1.json"))

        #self.image.fill('white')
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['main']  # check settings
        self._SpriteSheetImage = pygame.image.load(self._saveFile["image"]).convert_alpha()

        #moving attribute
        self._Direction = pygame.math.Vector2()
        self._Position = pygame.math.Vector2(self.rect.center)
        self._Speed = 110
        self._frameIndex = 0
        self._status = "down-Idle"

    
    

    def getImage(self,sheet,frame,width,height,scale, colour):
        self._Spriteimage = pygame.Surface((width, height)).convert_alpha()
        if frame == 0:
            self._Spriteimage.blit(sheet, (0,0), (0, 0, width, height))
        if frame == 1:
            self._Spriteimage.blit(sheet, (0,0), (16, 0, width + 16, height))
        if frame == 2:
            self._Spriteimage.blit(sheet, (0,0), (32, 0, width + 32, height))
        if frame == 3:
            self._Spriteimage.blit(sheet, (0,0), (0, 18, width, height+18))
        if frame == 4:
            self._Spriteimage.blit(sheet, (0,0), (16, 18, width + 16, height + 18))
        if frame == 5:
            self._Spriteimage.blit(sheet, (0,0), (32, 18, width + 32, height + 18))
        if frame == 6:
            self._Spriteimage.blit(sheet, (0,0), (0, 36, width, height + 36))
        if frame == 7:
            self._Spriteimage.blit(sheet, (0,0), (16, 36, width + 16, height + 36))
        if frame == 8:
            self._Spriteimage.blit(sheet, (0,0), (32, 36, width + 32, height + 36))
        if frame == 9:
            self._Spriteimage.blit(sheet, (0,0), (0, 54, width, height + 54))
        if frame == 10:
            self._Spriteimage.blit(sheet, (0,0), (16, 54, width + 16, height + 54))
        if frame == 11:
            self._Spriteimage.blit(sheet, (0,0), (32, 54, width + 32, height + 54))
        self._Spriteimage = pygame.transform.scale(self._Spriteimage, (width *scale, height *scale))
        self._Spriteimage.set_colorkey(colour)
        return self._Spriteimage




    def animate(self,Deltatime):
        frame0 = self.getImage(self._SpriteSheetImage,0,16,18,3,(0,0,255))
        frame1 = self.getImage(self._SpriteSheetImage,1,16,18,3,(0,0,255))
        frame2 = self.getImage(self._SpriteSheetImage,2,16,18,3,(0,0,255))
        frame3 = self.getImage(self._SpriteSheetImage,3,16,18,3,(0,0,255))
        frame4 = self.getImage(self._SpriteSheetImage,4,16,18,3,(0,0,255))
        frame5 = self.getImage(self._SpriteSheetImage,5,16,18,3,(0,0,255))
        frame6 = self.getImage(self._SpriteSheetImage,6,16,18,3,(0,0,255))
        frame7 = self.getImage(self._SpriteSheetImage,7,16,18,3,(0,0,255))
        frame8 = self.getImage(self._SpriteSheetImage,8,16,18,3,(0,0,255))
        frame9 = self.getImage(self._SpriteSheetImage,9,16,18,3,(0,0,255))
        frame10 = self.getImage(self._SpriteSheetImage,10,16,18,3,(0,0,255))
        frame11 = self.getImage(self._SpriteSheetImage,11,16,18,3,(0,0,255))
        self._Animations = {"up":[frame4,frame5],"down":[frame1,frame2],"left":[frame7,frame8],"right":[frame10,frame11],"down-Idle":[frame0],"up-Idle":[frame3],"right-Idle":[frame9],"left-Idle":[frame6]}

        self._frameIndex += 4 * Deltatime
        if self._frameIndex >= len(self._Animations[self._status]):
            self._frameIndex = 0
        self.image = self._Animations[self._status][int(self._frameIndex)]


    def input(self):
        keystroke = pygame.key.get_pressed()
        if keystroke[pygame.K_w]:
            self._Direction.y = -1
            self._status = "up"
        elif keystroke[pygame.K_s]:
            self._Direction.y = 1
            self._status = "down"
        else:
            self._Direction.y = 0

        if keystroke[pygame.K_a]:
            self._Direction.x = -1
            self._status = "left"
        elif keystroke[pygame.K_d]:
            self._Direction.x = 1
            self._status = "right"
        else:
            self._Direction.x = 0
        
    def getStatus(self):
        #if player is not pressing a key add Idle to the status
        if self._Direction.magnitude() == 0:
            self._status = self._status.split("-")[0] + "-Idle"

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
        self.getStatus()
        #frame0 = self.getImage(self._SpriteSheetImage,0,16,18,3,(0,0,255))
        #self.image.blit(frame0, (0,0))
        self.move(DeltaTime)
        self.animate(DeltaTime)