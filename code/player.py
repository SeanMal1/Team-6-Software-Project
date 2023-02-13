import pygame
import json
from settings import *
from timer import Timer
from inventory import Inventory


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, toggle_inventory, group, collision_sprites, tree_sprites):
        super().__init__(group)
        self.image = pygame.Surface((48,54))
        
        #savefile
        self._saveFile = json.load(open("../profiles/save1.json"))

        self._prevKeystroke = None
        self._inventoryOpen = False
        self.toggle_inventory = toggle_inventory

        #self.image.fill('white')
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['main']  # check settings
        self._SpriteSheetImage = pygame.image.load(self._saveFile["image"]).convert_alpha()
        self._PlayerRightAxeImage1 = pygame.image.load("../textures/player/playerblueaxeright.png").convert_alpha()
        self._PlayerRightAxeImage2 = pygame.image.load("../textures/player/playerblueaxeright2.png").convert_alpha()
        self._PlayerRightAxeImage3 = pygame.image.load("../textures/player/playerblueaxeright3.png").convert_alpha()
        self._PlayerLeftAxeImage1 = pygame.image.load("../textures/player/playerblueaxeleft.png").convert_alpha()
        self._PlayerLeftAxeImage2 = pygame.image.load("../textures/player/playerblueaxeleft2.png").convert_alpha()
        self._PlayerLeftAxeImage3 = pygame.image.load("../textures/player/playerblueaxeleft3.png").convert_alpha()
        self._PlayerUpAxeImage1 = pygame.image.load("../textures/player/playerblueaxeup.png").convert_alpha()
        self._PlayerUpAxeImage2 = pygame.image.load("../textures/player/playerblueaxeup2.png").convert_alpha()
        self._PlayerUpAxeImage3 = pygame.image.load("../textures/player/playerblueaxeup3.png").convert_alpha()
        self._PlayerDownAxeImage1 = pygame.image.load("../textures/player/playerblueaxedown.png").convert_alpha()
        self._PlayerDownAxeImage2 = pygame.image.load("../textures/player/playerblueaxedown2.png").convert_alpha()
        self._PlayerDownAxeImage3 = pygame.image.load("../textures/player/playerblueaxedown3.png").convert_alpha()
        self._PlayerRightHoeImage1 = pygame.image.load("../textures/player/playerbluerighthoe.png").convert_alpha()
        self._PlayerRightHoeImage2 = pygame.image.load("../textures/player/playerbluerighthoe2.png").convert_alpha()
        self._PlayerRightHoeImage3 = pygame.image.load("../textures/player/playerbluerighthoe3.png").convert_alpha()
        self._PlayerLeftHoeImage1 = pygame.image.load("../textures/player/playerbluelefthoe.png").convert_alpha()
        self._PlayerLeftHoeImage2 = pygame.image.load("../textures/player/playerbluelefthoe2.png").convert_alpha()
        self._PlayerLeftHoeImage3 = pygame.image.load("../textures/player/playerbluelefthoe3.png").convert_alpha()
        self._PlayerUpHoeImage = pygame.image.load("../textures/player/playerblueuphoe.png").convert_alpha()
        self._PlayerUpHoeImage2 = pygame.image.load("../textures/player/playerblueuphoe2.png").convert_alpha()
        self._PlayerUpHoeImage3 = pygame.image.load("../textures/player/playerblueuphoe3.png").convert_alpha()
        self._PlayerDownHoeImage = pygame.image.load("../textures/player/playerbluedownhoe.png").convert_alpha()
        self._PlayerDownHoeImage2 = pygame.image.load("../textures/player/playerbluedownhoe2.png").convert_alpha()
        self._PlayerDownHoeImage3 = pygame.image.load("../textures/player/playerbluedownhoe3.png").convert_alpha()
        self._PlayerRightWaterImage = pygame.image.load("../textures/player/playerbluerightwater.png").convert_alpha()
        self._PlayerRightWaterImage2 = pygame.image.load("../textures/player/playerbluerightwater2.png").convert_alpha()
        self._PlayerLeftWaterImage = pygame.image.load("../textures/player/playerblueleftwater.png").convert_alpha()
        self._PlayerLeftWaterImage2 = pygame.image.load("../textures/player/playerblueleftwater2.png").convert_alpha()
        self._playerUpWaterImage = pygame.image.load("../textures/player/playerblueupwater.png").convert_alpha()
        self._playerUpWaterImage2 = pygame.image.load("../textures/player/playerblueupwater2.png").convert_alpha()
        self._PlayerDownWaterImage = pygame.image.load("../textures/player/playerbluedownwater.png").convert_alpha()
        self._PlayerDownWaterImage2 = pygame.image.load("../textures/player/playerbluedownwater2.png").convert_alpha()

        # collision attribute
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.copy().inflate((-20, -40))  # shrink hitbox to player size from sheet size

        #moving attribute
        self._Direction = pygame.math.Vector2()
        self._Position = pygame.math.Vector2(self.rect.center)
        self._Speed = 110
        self._frameIndex = 0
        self._status = self._saveFile["status"]
        self._animSpeed = 4

        #Timing
        self.timer = {
            'tool use' : Timer(350,self.use_tool),
            'tool swap' : Timer(200),
            'seed use' : Timer(350,self.use_seed),
            'seed swap' : Timer(200)
        }

        #Tools
        self._Tools = ['axe','hoe','water']
        self._ToolIndex = 0
        self._SelectedTool = self._Tools[self._ToolIndex]

        #seeds for crops/plants
        self._Seeds = ['wheat', 'corn']
        self._SeedIndex = 0
        self._SelectedSeed = self._Seeds[self._SeedIndex]

        #interaction
        self._TreeSprites = tree_sprites

        #inventory
        self._Inventory = self._saveFile['inventory']
    
    def use_seed(self):
        pass
    
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

    def input(self):
        keystroke = pygame.key.get_pressed()

        if not self.timer['tool use']._Active:
            if keystroke[pygame.K_w]:
                self._Direction.y = -1
                self._status = "up"
                self._animSpeed = 4
            elif keystroke[pygame.K_s]:
                self._Direction.y = 1
                self._status = "down"
                self._animSpeed = 4
            else:
                self._Direction.y = 0

            if keystroke[pygame.K_a]:
                self._Direction.x = -1
                self._status = "left"
                self._animSpeed = 12
            elif keystroke[pygame.K_d]:
                self._Direction.x = 1
                self._status = "right"
                self._animSpeed = 12
            else:
                self._Direction.x = 0

            if keystroke[pygame.K_LSHIFT]:
                    self._Speed = 250
            else : 
                    self._Speed = 110

            #tool utilization
            if keystroke[pygame.K_c]:
                # use time
                self._animSpeed = 12
                self.timer['tool use'].activate()
                self._Direction = pygame.math.Vector2()
                self._frameIndex = 0

            #change tool
            if keystroke[pygame.K_q] and not self.timer['tool swap']._Active:
                self.timer['tool swap'].activate()
                self._ToolIndex += 1
                if self._ToolIndex < len(self._Tools):
                    self._ToolIndex = self._ToolIndex
                else:
                    self._ToolIndex = 0
                print(self._Tools[self._ToolIndex])
                self._SelectedTool = self._Tools[self._ToolIndex]

            #seed utilization
            if keystroke[pygame.K_f]:
                self.timer['seed use'].activate()
                self._Direction = pygame.math.Vector2()
                self._frameIndex = 0
                print('used seed')

            #change seed
            if keystroke[pygame.K_x] and not self.timer['seed swap']._Active:
                self.timer['seed swap'].activate()
                self._SeedIndex += 1
                if self._SeedIndex < len(self._Seeds):
                    self._SeedIndex = self._SeedIndex
                else:
                    self._SeedIndex = 0
                print(self._SelectedSeed)
                self._SelectedSeed = self._Seeds[self._SeedIndex]


            #inventory
            if self._prevKeystroke is not None:
                if self._prevKeystroke[pygame.K_e] and not keystroke[pygame.K_e]:
                    self._inventoryOpen = not self._inventoryOpen
                    self.toggle_inventory()

            self._prevKeystroke = keystroke
     
    def use_tool(self):
        if self._SelectedTool == 'hoe':
            pass
        if self._SelectedTool == 'axe':
            for tree in self._TreeSprites.sprites():
                if tree.rect.collidepoint(self._TargetPosition):
                    tree.BreakTree()
        if self._SelectedTool == 'water':
            pass

    def get_target_pos(self):
        self._TargetPosition = self.rect.center + PlayerToolOffset[self._status.split('-')[0]]

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
        rightaxe1 = self.getImage(self._PlayerRightAxeImage1,0,17,18,3,(0,0,255))
        rightaxe2 = self.getImage(self._PlayerRightAxeImage2,0,14,18,3,(0,0,255))
        rightaxe3 = self.getImage(self._PlayerRightAxeImage3,0,14,18,3,(0,0,255))
        leftaxe1 = self.getImage(self._PlayerLeftAxeImage1,0,17,18,3,(0,0,255))
        leftaxe2 = self.getImage(self._PlayerLeftAxeImage2,0,14,18,3,(0,0,255))
        leftaxe3 = self.getImage(self._PlayerLeftAxeImage3,0,14,18,3,(0,0,255))
        upaxe1 = self.getImage(self._PlayerUpAxeImage1,0,14,18,3,(0,0,255))
        upaxe2 = self.getImage(self._PlayerUpAxeImage2,0,14,18,3,(0,0,255))
        upaxe3 = self.getImage(self._PlayerUpAxeImage3,0,14,18,3,(0,0,255))
        downaxe1 = self.getImage(self._PlayerDownAxeImage1,0,14,18,3,(0,0,255))
        downaxe2 = self.getImage(self._PlayerDownAxeImage2,0,14,18,3,(0,0,255))
        downaxe3 = self.getImage(self._PlayerDownAxeImage3,0,14,18,3,(0,0,255))
        righthoe1 = self.getImage(self._PlayerRightHoeImage1,0,14,18,3,(0,0,255))
        righthoe2 = self.getImage(self._PlayerRightHoeImage2,0,15,18,3,(0,0,255))
        righthoe3 = self.getImage(self._PlayerRightHoeImage3,0,14,18,3,(0,0,255))
        lefthoe1 = self.getImage(self._PlayerLeftHoeImage1,0,14,18,3,(0,0,255))
        lefthoe2 = self.getImage(self._PlayerLeftHoeImage2,0,15,18,3,(0,0,255))
        lefthoe3 = self.getImage(self._PlayerLeftHoeImage3,0,14,18,3,(0,0,255))
        uphoe = self.getImage(self._PlayerUpHoeImage,0,18,18,3,(0,0,255))
        uphoe2 = self.getImage(self._PlayerUpHoeImage2,0,16,18,3,(0,0,255))
        uphoe3 = self.getImage(self._PlayerUpHoeImage,0,14,18,3,(0,0,255))
        downhoe = self.getImage(self._PlayerDownHoeImage,0,14,18,3,(0,0,255))
        downhoe2 = self.getImage(self._PlayerDownHoeImage2,0,14,18,3,(0,0,255))
        downhoe3 = self.getImage(self._PlayerDownHoeImage3,0,14,18,3,(0,0,255))
        rightwater = self.getImage(self._PlayerRightWaterImage,0,20,18,3,(0,0,255))
        rightwater2 = self.getImage(self._PlayerRightWaterImage2,0,19,18,3,(0,0,255))
        leftwater = self.getImage(self._PlayerLeftWaterImage,0,20,18,3,(0,0,255))
        leftwater2 = self.getImage(self._PlayerLeftWaterImage2,0,19,18,3,(0,0,255))
        upwater = self.getImage(self._playerUpWaterImage,0,15,18,3,(0,0,255))
        upwater2 = self.getImage(self._playerUpWaterImage2,0,16,18,3,(0,0,255))
        downwater = self.getImage(self._PlayerDownWaterImage,0,16,21,3,(0,0,255))
        downwater2 = self.getImage(self._PlayerDownWaterImage2,0,15,22,3,(0,0,255))
        self._Animations = {
            "up":[frame4,frame5],
            "down":[frame1,frame2],
            "left":[frame7,frame6,frame8],
            "right":[frame10,frame9, frame11],
            "down-Idle":[frame0],
            "up-Idle":[frame3],
            "right-Idle":[frame9],
            "left-Idle":[frame6],
            "right-axe":[rightaxe3,rightaxe2,rightaxe1],
            "left-axe":[leftaxe1,leftaxe2,leftaxe3],
            "up-axe":[upaxe1,upaxe2,upaxe3],
            "down-axe":[downaxe3,downaxe1,downaxe2],
            "right-hoe":[righthoe1,righthoe2,righthoe3],
            "left-hoe":[lefthoe1,lefthoe2,lefthoe3],
            "up-hoe":[uphoe,uphoe2,uphoe3],
            "down-hoe":[downhoe,downhoe2,downhoe3],
            "right-water":[rightwater,rightwater2],
            "left-water":[leftwater,leftwater2],
            "up-water":[upwater,upwater2],
            "down-water":[downwater,downwater2]
            }

        self._frameIndex += self._animSpeed * Deltatime
        if self._frameIndex >= len(self._Animations[self._status]):
            self._frameIndex = 0
        self.image = self._Animations[self._status][int(self._frameIndex)]

    def getStatus(self):
        #if player is not pressing a key add Idle to the status
        if self._Direction.magnitude() == 0:
            self._status = self._status.split("-")[0] + "-Idle"

        if self.timer['tool use']._Active:
            self._status = self._status.split("-")[0] + '-' + self._SelectedTool

    def updateTimers(self):
        for timer in self.timer.values():
            timer.update()

    def collision(self, _Direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):  # Checks if sprite has collision
                if sprite.hitbox.colliderect(self.hitbox):  # Checks if there is a collision
                    if _Direction == 'horizontal':
                        if self._Direction.x > 0:  # player moving to the right
                            self.hitbox.right = sprite.hitbox.left
                            print("hit right")
                        if self._Direction.x < 0:  # player moving to the left
                            self.hitbox.left = sprite.hitbox.right
                            print("hit left")
                        self.rect.centerx = self.hitbox.centerx
                        self._Position.x = self.hitbox.centerx
                    if _Direction == 'vertical':
                        if self._Direction.y > 0:  # player moving down
                            self.hitbox.bottom = sprite.hitbox.top
                            print("hit top")
                        if self._Direction.y < 0:  # player moving up
                            self.hitbox.top = sprite.hitbox.bottom
                            print("hit bottom")
                        self.rect.centery = self.hitbox.centery
                        self._Position.y = self.hitbox.centery

    def move(self,DeltaTime):
        #normalize vector (cant speed up by holding w and a or w and d and so on)
        if self._Direction.magnitude() > 0:
            self._Direction = self._Direction.normalize()

        #movement on x axis
        self._Position.x += self._Direction.x * self._Speed * DeltaTime
        self.hitbox.centerx = round(self._Position.x) # rounding to prevent truncation
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        #movement on y axis
        self._Position.y += self._Direction.y * self._Speed * DeltaTime
        self.hitbox.centery = round(self._Position.y)  # rounding to prevent truncation
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def update(self,DeltaTime):
        self.input()
        self.getStatus()
        self.updateTimers()
        self.get_target_pos()
        #frame0 = self.getImage(self._SpriteSheetImage,0,16,18,3,(0,0,255))
        #self.image.blit(frame0, (0,0))
        self.move(DeltaTime)
        self.animate(DeltaTime)

    def save(self):
        self._saveFile["status"] = self._status
        self._saveFile['position']['x'] = self._Position.x
        self._saveFile['position']['y'] = self._Position.y
        self._saveFile['inventory'] = self._Inventory
        with open("../profiles/save1.json", "w") as f:
            f.write(json.dumps(self._saveFile))
