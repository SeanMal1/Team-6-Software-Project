import math

from setuptools import setup
import pygame
import json
from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from tools import *
from overlay import Overlay
from inventory import Inventory
from soil import SoilLayer
from sky import *
from animal import *
from random import randint
from transition import Transition
from merchant import Merchant

class Level:
    def __init__(self, restart):
        self.tmx_data = load_pygame('../data/Farm.tmx')
        self.tmx_house_data = load_pygame('../data/House.tmx')
        # self._Player = None  Commented out in testing Sleep function
        self._DisplaySurface = pygame.display.get_surface()
        self._DisplayWorld = pygame.display.get_surface()
        self._mask = pygame.Surface((180,100),pygame.SRCALPHA)
        self._AllSprites = CameraGroup()
        self._TreeSprites = pygame.sprite.Group()
        self._AnimalSprites = pygame.sprite.Group()
        self._HouseSprites = pygame.sprite.Group()
        self._OutsideHouseSprites = pygame.sprite.Group()
        self._CollisionSprites = pygame.sprite.Group()  # To keep track of collide-able sprites
        self._InteractionSprites = pygame.sprite.Group()
        self._SoilLayer = SoilLayer(self._AllSprites, self._CollisionSprites)
        self._saveFile = json.load(open("../profiles/save1.json"))
        self._Location = self._saveFile["location"]
        self._Position = (self._saveFile["position"]["x"], self._saveFile["position"]["y"])
        self._PopUpBackground = pygame.image.load('../textures/misc/main_menu.png')
        self._PopUpBackground = pygame.transform.scale(self._PopUpBackground, (640 *0.6,533*0.6))
        self.restart = restart
        self._Level_init = True
        self._AnimalList = []
        self.cow_walk_frames = import_folder('../textures/animals/cow/green_cow/green_cow_walk')
        self.cow_idle_frames = import_folder('../textures/animals/cow/green_cow/green_cow_idle')
        self.setup()
        self._SpriteSheetImage = pygame.image.load(self._saveFile["image"]).convert_alpha()
        self._SpriteSheetImage.set_colorkey([0, 0, 0])
        self._Overlay = Overlay(self._Player)
        self._Transition = Transition(self.reset, self._Player)
        self._Sky = Sky()
        self.rain = Rain(self._AllSprites)
        self.raining = randint(0, 28) > 20  # rains if randint higher than x
        self._SoilLayer.raining = self.raining
        
        self._heading_font = pygame.font.Font('../font/joystixmonospace.otf', 45)
        self._regular_font = pygame.font.Font('../font/joystixmonospace.otf', 16)
        self._PopupFontHeader = pygame.font.Font('../font/joystixmonospace.otf', 18)
        self._PopupFontMain = pygame.font.Font('../font/joystixmonospace.otf', 11)
        self._text_color = "Black"
        self._button_color = (220, 220, 220)
        self._button_hover_color = (180, 180, 180)

        self._inventory_open = False
        self._Paused = False
        self._main_menu = True
        self._PopUPmenu = True
        self._PlayerSelect = False
        self._inventory = Inventory(self._Player._Inventory, self._Player.money, self.toggle_inventory)
        
        self._PlayerImage = pygame.image.load("../textures/player/blueplayer.png")
        self._PlayerSelectBG = pygame.image.load("../textures/misc/playerselectbg.jpg")
        
        

        #shop
        self.merchant = Merchant(self._Player, self.toggle_merchant)
        self.shop_active = False

    def toggle_inventory(self):
        self._inventory_open = not self._inventory_open

    def plantCollision(self):
        if self._SoilLayer._PlantSprites:
            for plant in self._SoilLayer._PlantSprites.sprites():
                if plant._PlantGrown and plant.rect.colliderect(self._Player.hitbox):
                    self.PlayerAdd(plant._PlantType)
                    plant.kill()
                    Particle(
                        plant.rect.topleft,
                        plant.image,
                        self._AllSprites,
                        LAYERS['main']
                        )
                    self._SoilLayer.grid[plant.rect.centery // (TileSize * Scale)][plant.rect.centerx // (TileSize * Scale)].remove("P")
                    

    def setup(self):
        if self._Level_init:
            self._Level_init = False
            self._SoilLayer.dry_soil_tiles()

            # Fence
            for x, y, surface in self.tmx_data.get_layer_by_name('Fence').tiles():
                Generic(pos=(x * TileSize * Scale, y * TileSize * Scale), surface=surface, groups=[self._AllSprites, self._CollisionSprites])

            # Water
            water_frames = import_folder('../data/Tilesets/water')
            for x, y, surface in self.tmx_data.get_layer_by_name('Water').tiles():
                Water(pos=(x * TileSize * Scale, y * TileSize * Scale), frames=water_frames, groups=self._AllSprites)

            # Decoration
            for obj in self.tmx_data.get_layer_by_name('Decoration'):
                Decoration(pos=(obj.x * Scale, obj.y * Scale), surface=obj.image, groups=[self._AllSprites, self._CollisionSprites])

            # Trees
            for obj in self.tmx_data.get_layer_by_name('Trees'):
                Tree(pos=(obj.x * Scale, obj.y * Scale), surface=obj.image, groups=[self._AllSprites, self._CollisionSprites,self._TreeSprites], name=obj.name, playerAdd= self.PlayerAdd)

            # Animals
            self._AnimalList.append(
                Animal(pos=(2500, 1200),
                       frames=self.cow_idle_frames,
                       groups=[self._AnimalSprites, self._AllSprites],
                       collision_sprites=self._CollisionSprites))
            self._AnimalList.append(
                Animal(pos=(2300, 1150),
                       frames=self.cow_idle_frames,
                       groups=[self._AnimalSprites, self._AllSprites],
                       collision_sprites=self._CollisionSprites))
            self._AnimalList.append(
                Animal(pos=(2700, 1400),
                       frames=self.cow_idle_frames,
                       groups=[self._AnimalSprites, self._AllSprites],
                       collision_sprites=self._CollisionSprites))
            self._AnimalList.append(
                Animal(pos=(2000, 1600),
                       frames=self.cow_idle_frames,
                       groups=[self._AnimalSprites, self._AllSprites],
                       collision_sprites=self._CollisionSprites))


            # Collision Tiles, Borders
            for x, y, surface in self.tmx_data.get_layer_by_name('Borders').tiles():
                Border(pos=(x * TileSize * Scale, y * TileSize * Scale), surface=pygame.Surface((TileSize * Scale, TileSize * Scale)), groups= self._CollisionSprites)

            # Ground
            Generic(pos=(0, 0),
                    surface = pygame.image.load('../data/Farm.png').convert_alpha(),
                    groups=[self._AllSprites],
                    z=LAYERS['ground'])
            self._SoilLayer.create_soil_grid()

            # Player
            self._Player = Player(pos=self._Position,
                                  toggle_inventory=self.toggle_inventory,
                                  group=self._AllSprites,
                                  collision_sprites=self._CollisionSprites,
                                  tree_sprites=self._TreeSprites,
                                  animal_sprites=self._AnimalSprites,
                                  soil_layer=self._SoilLayer,
                                  interaction=self._InteractionSprites,
                                  toggle_merchant=self.toggle_merchant,
                                  Level=self,
                                  restart=self.restart)

        if self._Location == 'farm':
            for sprite in self._HouseSprites:
                sprite.kill()
            print("Current Location: ", self._Location)
            # House
            for x, y, surface in self.tmx_data.get_layer_by_name('Building Floor').tiles():
                Generic(pos=(x * TileSize * Scale, y * TileSize * Scale), surface=surface, groups=[self._AllSprites, self._CollisionSprites, self._OutsideHouseSprites], z=LAYERS['house bottom'])
            for x, y, surface in self.tmx_data.get_layer_by_name('Building Wall').tiles():
                Generic(pos=(x * TileSize * Scale, y * TileSize * Scale), surface=surface, groups=[self._AllSprites, self._CollisionSprites, self._OutsideHouseSprites], z=LAYERS['house bottom'])
            for x, y, surface in self.tmx_data.get_layer_by_name('Building Roof').tiles():
                Generic(pos=(x * TileSize * Scale, y * TileSize * Scale), surface=surface, groups=[self._AllSprites, self._OutsideHouseSprites], z=LAYERS['house top'])
            # Interaction
            for obj in self.tmx_data.get_layer_by_name('Interaction'):
                Interaction(pos=(obj.x * Scale, obj.y * Scale), size=(obj.width, obj.height), groups=[self._InteractionSprites], name=obj.name)


        # Loading House
        elif self._Location == 'house':
            print("Current Location: ", self._Location)
            for sprite in self._OutsideHouseSprites:
                sprite.kill()

            for x, y, surface in self.tmx_house_data.get_layer_by_name('Floor').tiles():
                Generic(pos=(x * TileSize * Scale, y * TileSize * Scale), surface=surface, groups=[self._AllSprites, self._HouseSprites], z=LAYERS['soil'])
            for x, y, surface in self.tmx_house_data.get_layer_by_name('Walls').tiles():
                Generic(pos=(x * TileSize * Scale, y * TileSize * Scale), surface=surface, groups=[self._AllSprites, self._CollisionSprites, self._HouseSprites])
            for obj in self.tmx_house_data.get_layer_by_name('Furniture'):
                Generic(pos=(obj.x * Scale, obj.y * Scale), surface=obj.image, groups=[self._AllSprites, self._CollisionSprites, self._HouseSprites])
            # for obj in self.tmx_house_data.get_layer_by_name('Floor Furniture'):
            #     Generic(pos=(obj.x * Scale, obj.y * Scale), surface=obj.image, groups=[self._AllSprites, self._HouseSprites], z=LAYERS['house bottom'])
            for obj in self.tmx_house_data.get_layer_by_name('Interaction'):
                # if obj.name == 'Trader':  # change to 'Bed', Trader just for testing
                Interaction(pos=(obj.x * Scale, obj.y * Scale), size=(obj.width, obj.height),
                            groups=[self._InteractionSprites], name=obj.name)

    def load_farm(self):
        self._Location = 'farm'
        self._Transition.play(self._Player)
        self.setup()
        print('HEREHRHEHRHEHRHEHR')

    def load_house(self):
        self._Location = 'house'
        self._Transition.play(self._Player)
        self.setup()

    def PlayerAdd(self,item):
        self._Player._Inventory[item] += 1

    def toggle_merchant(self):
        self.shop_active = not self.shop_active

    def reset(self):  # resetting day
        # Soil
        self._SoilLayer.updatePlants()
        self.raining = randint(0, 28) > 20  # rains if randint higher than x
        self._SoilLayer.raining = self.raining
        self._SoilLayer.dry_soil_tiles()
        

        if self._SoilLayer.raining:
            self._SoilLayer.water_all()
        # Trees
        for tree in self._TreeSprites.sprites():
            for plum in tree._PlumSprites.sprites():  # clear existing plums
                plum.kill()
            tree.CreatePlum()  # spawn new plums

        #sky
        
    def run(self, DeltaTime):
        if self._main_menu:
            self._DisplayWorld.fill('black')
            self._PlayerSelectBG = pygame.transform.scale(self._PlayerSelectBG, (2880,1620))
            self._DisplaySurface.blit(self._PlayerSelectBG,(-650,-290))
            self._DisplaySurface.blit(pygame.image.load('../textures/misc/main_menu.png'), (ScreenWidth/2 - 640/2, ScreenHeight/2 - 533/2))
            self._DisplaySurface.blit(self._heading_font.render("Valley Life", False, "Black"), (ScreenWidth/2 - 390/2, ScreenHeight/2 - 55))
            self._DisplaySurface.blit(self._regular_font.render("Press Space to begin.", False, "Black"), (ScreenWidth/2 - 260/2, ScreenHeight/2 + 50))
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self._main_menu = False
            

        elif not self._Paused:
            self._DisplayWorld.fill('black')
            self._AllSprites.draw(self._DisplayWorld)
            self._AllSprites.custom_draw(self._Player)
            self._Sky.display(DeltaTime)
            
            # daylight reset for sleep
            if self._Transition._Colour <= 0:
                self._Sky._DayColour = [255,255,255]

            if self._saveFile["firstTimePlaying"] == "True":
                if self._PopUPmenu:
                    self._DisplaySurface.blit(self._PopUpBackground, (ScreenWidth - 460, ScreenHeight -700))
                    self._DisplaySurface.blit(self._PopupFontHeader.render("Player Tips", False, "Black"), (ScreenWidth - 720/2, ScreenHeight - 670))
                    self._DisplaySurface.blit(self._PopupFontMain.render('Press "E" to open the inventory!', False, "Black"), (ScreenWidth - 840/2, ScreenHeight - 640))
                    self._DisplaySurface.blit(self._PopupFontMain.render('Press "Q" to open the swap tool!', False, "Black"), (ScreenWidth - 840/2, ScreenHeight - 620))
                    self._DisplaySurface.blit(self._PopupFontMain.render('Press "Mouse 1" to use the tool!', False, "Black"), (ScreenWidth - 840/2, ScreenHeight - 600))
                    self._DisplaySurface.blit(self._PopupFontMain.render('Press "ENTER" to interact with the', False, "Black"), (ScreenWidth - 840/2, ScreenHeight - 570))
                    self._DisplaySurface.blit(self._PopupFontMain.render('door, the bed and trader!', False, "Black"), (ScreenWidth - 840/2, ScreenHeight - 558))
                    self._DisplaySurface.blit(self._PopupFontMain.render('Press "X" to swap seed!', False, "Black"), (ScreenWidth - 840/2, ScreenHeight - 530))
                    self._DisplaySurface.blit(self._PopupFontMain.render('Press "F" to use seed!', False, "Black"), (ScreenWidth - 840/2, ScreenHeight - 510))
                    self._DisplaySurface.blit(self._PopupFontMain.render('Press "H" to eat!', False, "Black"), (ScreenWidth - 840/2, ScreenHeight - 490))
                    self._DisplaySurface.blit(self._PopupFontMain.render('Press "W","A","S","D" to move!', False, "Black"), (ScreenWidth - 840/2, ScreenHeight - 470))
                    self._DisplaySurface.blit(self._PopupFontMain.render('Press "shift" to sprint!', False, "Black"), (ScreenWidth - 840/2, ScreenHeight - 450))

                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                self._PopUPmenu = False

            if self._inventory_open:
                self._inventory.display()
            elif self.shop_active:
                self.merchant.update()
            else:
                self._AllSprites.draw(self._SpriteSheetImage)
                self._AllSprites.update(DeltaTime)
                self.plantCollision()
                
                
            # rain
            if self.raining:
                if self._Location != 'house' and not self.shop_active:
                    self.rain.update()
                    self._SoilLayer.water_all()

            # overlay/ui
            self._Overlay.Display()

            # Sleep/day reset
            if self._Player._Sleep:
                self._Transition.play(self._Player)

            # Animals
            for animal in self._AnimalList:
                if animal._GoDir == "None":
                    animal.image = self.cow_idle_frames[math.trunc(animal._frameIndex)]
                    if animal._ImageFlip:
                        animal.image = pygame.transform.flip(animal.image, True, False)
                else:
                    animal.image = self.cow_walk_frames[math.trunc(animal._frameIndex)]
                    if animal._ImageFlip:
                        animal.image = pygame.transform.flip(animal.image, True, False)




        # Pause Menu
        else:

            self._text_return = self._heading_font.render('Return to Game' , True , self._text_color, self._button_color)
            self._text_rect_return = self._text_return.get_rect(center=(ScreenWidth/2, ScreenHeight/2 - 120))

            self._text_new = self._heading_font.render('New Game' , True , self._text_color, self._button_color)
            self._text_rect_new = self._text_new.get_rect(center=(ScreenWidth/2, ScreenHeight/2))

            self._text_quit = self._heading_font.render('Save and Quit' , True , self._text_color, self._button_color)
            self._text_rect_quit = self._text_quit.get_rect(center=(ScreenWidth/2, ScreenHeight/2 + 120))

            self._text_player_select = self._heading_font.render('Player Select', True, self._text_color,self._button_color)
            self._text_rect_player_select = self._text_player_select.get_rect(center=(ScreenWidth/2, ScreenHeight/2 + 240))
            self._text_green = self._heading_font.render('Green' , True , self._text_color, self._button_color)
            self._text_rect_green = self._text_green.get_rect(center=(ScreenWidth/4, ScreenHeight/6))
            self._text_blue = self._heading_font.render('Blue' , True , self._text_color, self._button_color)
            self._text_rect_blue = self._text_blue.get_rect(center=(ScreenWidth/4, ScreenHeight/6 + 90))
            self._text_red = self._heading_font.render('Red' , True , self._text_color, self._button_color)
            self._text_rect_red = self._text_red.get_rect(center=(ScreenWidth/4, ScreenHeight/6 + (180)))
            self._text_purple = self._heading_font.render('Purple' , True , self._text_color, self._button_color)
            self._text_rect_purple = self._text_purple.get_rect(center=(ScreenWidth/4, ScreenHeight/6 + (270)))
            self._text_pink = self._heading_font.render('Pink' , True , self._text_color, self._button_color)
            self._text_rect_pink = self._text_pink.get_rect(center=(ScreenWidth/4, ScreenHeight/6 + (360)))
            self._text_orange = self._heading_font.render('Orange' , True , self._text_color, self._button_color)
            self._text_rect_orange = self._text_orange.get_rect(center=(ScreenWidth/4, ScreenHeight/6 + (450)))
            self._text_grey = self._heading_font.render('Grey' , True , self._text_color, self._button_color)
            self._text_rect_grey = self._text_grey.get_rect(center=(ScreenWidth/4, ScreenHeight/6 + (540)))

            if self._text_rect_quit.collidepoint(pygame.mouse.get_pos()):
                self._text_quit = self._heading_font.render('Save and Quit' , True , self._text_color, self._button_hover_color)
            else:
                self._text_quit = self._heading_font.render('Save and Quit' , True , self._text_color, self._button_color)

            if self._text_rect_new.collidepoint(pygame.mouse.get_pos()):
                self._text_new = self._heading_font.render('New Game' , True , self._text_color, self._button_hover_color)
            else:
                self._text_new = self._heading_font.render('New Game' , True , self._text_color, self._button_color)

            if self._text_rect_return.collidepoint(pygame.mouse.get_pos()):
                self._text_return = self._heading_font.render('Return to Game' , True , self._text_color, self._button_hover_color)
            else:
                self._text_return = self._heading_font.render('Return to Game' , True , self._text_color, self._button_color)

            if self._text_rect_player_select.collidepoint(pygame.mouse.get_pos()):
                self._text_player_select = self._heading_font.render('Player Select', True, self._text_color, self._button_hover_color)
            else:
                self._text_player_select = self._heading_font.render('Player Select', True, self._text_color, self._button_color)

            if self._text_rect_green.collidepoint(pygame.mouse.get_pos()):
                self._text_green = self._heading_font.render('Green' , True , self._text_color, self._button_hover_color)
                self._PlayerImage = pygame.image.load("../textures/player/greenplayer.png")
            else:
                self._text_green = self._heading_font.render('Green' , True , self._text_color, self._button_color)
            if self._text_rect_blue.collidepoint(pygame.mouse.get_pos()):
                self._text_blue = self._heading_font.render('Blue' , True , self._text_color, self._button_hover_color)
                self._PlayerImage = pygame.image.load("../textures/player/blueplayer.png")
            else:
                self._text_blue = self._heading_font.render('Blue' , True , self._text_color, self._button_color)
            if self._text_rect_red.collidepoint(pygame.mouse.get_pos()):
                self._text_red = self._heading_font.render('Red' , True , self._text_color, self._button_hover_color)
                self._PlayerImage = pygame.image.load("../textures/player/redplayer.png")
            else:
                self._text_red = self._heading_font.render('Red' , True , self._text_color, self._button_color)
            if self._text_rect_purple.collidepoint(pygame.mouse.get_pos()):
                self._text_purple = self._heading_font.render('Purple' , True , self._text_color, self._button_hover_color)
                self._PlayerImage = pygame.image.load("../textures/player/purpleplayer.png")
            else:
                self._text_purple = self._heading_font.render('Purple' , True , self._text_color, self._button_color)
            if self._text_rect_pink.collidepoint(pygame.mouse.get_pos()):
                self._text_pink = self._heading_font.render('Pink' , True , self._text_color, self._button_hover_color)
                self._PlayerImage = pygame.image.load("../textures/player/pinkplayer.png")
            else:
                self._text_pink = self._heading_font.render('Pink' , True , self._text_color, self._button_color)
            if self._text_rect_orange.collidepoint(pygame.mouse.get_pos()):
                self._text_orange = self._heading_font.render('Orange' , True , self._text_color, self._button_hover_color)
                self._PlayerImage = pygame.image.load("../textures/player/orangeplayer.png")
            else:
                self._text_orange = self._heading_font.render('Orange' , True , self._text_color, self._button_color)
            if self._text_rect_grey.collidepoint(pygame.mouse.get_pos()):
                self._text_grey = self._heading_font.render('Grey' , True , self._text_color, self._button_hover_color)
                self._PlayerImage = pygame.image.load("../textures/player/greyplayer.png")
            else:
                self._text_grey = self._heading_font.render('Grey' , True , self._text_color, self._button_color)


            self._DisplaySurface.blit(self._text_return, self._text_rect_return)
            self._DisplaySurface.blit(self._text_new, self._text_rect_new)
            self._DisplaySurface.blit(self._text_quit, self._text_rect_quit)
            self._DisplaySurface.blit(self._text_player_select, self._text_rect_player_select)
            if self._PlayerSelect == True:
                self._DisplaySurface.fill("black")
                self._PlayerSelectBG = pygame.transform.scale(self._PlayerSelectBG, (2880,1620))
                self._DisplaySurface.blit(self._PlayerSelectBG,(-650,-290))
                self._DisplaySurface.blit(self._text_green, self._text_rect_green)
                self._DisplaySurface.blit(self._text_blue, self._text_rect_blue)
                self._DisplaySurface.blit(self._text_red, self._text_rect_red)
                self._DisplaySurface.blit(self._text_purple, self._text_rect_purple)
                self._DisplaySurface.blit(self._text_pink, self._text_rect_pink)
                self._DisplaySurface.blit(self._text_orange, self._text_rect_orange)
                self._DisplaySurface.blit(self._text_grey, self._text_rect_grey)
                self._PlayerImage = pygame.transform.scale(self._PlayerImage, (140,180))
                self._PlayerImage.set_colorkey((0,0,255))
                self._DisplaySurface.blit(self._PlayerImage, (ScreenWidth/2 + 100, ScreenHeight/2 - 100))
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self._Paused = not self._Paused
                    if event.type == pygame.MOUSEBUTTONDOWN and self._Paused:
                        if self._text_rect_player_select.collidepoint(pygame.mouse.get_pos()):
                            self._PlayerSelect = True
                        if self._text_rect_green.collidepoint(pygame.mouse.get_pos()):
                            self._Player._SelectedPlayerColour = ""
                            self._Player._SelectedSpriteSheet = "../textures/player/playerblue.png"
                            self._Paused = not self._Paused
                            self._PlayerSelect = False
                        if self._text_rect_blue.collidepoint(pygame.mouse.get_pos()):
                            self._Player._SelectedPlayerColour = "blue"
                            self._Player._SelectedSpriteSheet = "../textures/player/playerlightblue.png"
                            self._Paused = not self._Paused#
                            self._PlayerSelect = False
                        if self._text_rect_red.collidepoint(pygame.mouse.get_pos()):
                            self._Player._SelectedPlayerColour = "red"
                            self._Player._SelectedSpriteSheet = "../textures/player/playerred.png"
                            self._Paused = not self._Paused
                            self._PlayerSelect = False
                        if self._text_rect_purple.collidepoint(pygame.mouse.get_pos()):
                            self._Player._SelectedPlayerColour = "purple"
                            self._Player._SelectedSpriteSheet = "../textures/player/playerpurple.png"
                            self._Paused = not self._Paused
                            self._PlayerSelect = False
                        if self._text_rect_pink.collidepoint(pygame.mouse.get_pos()):
                            self._Player._SelectedPlayerColour = "pink"
                            self._Player._SelectedSpriteSheet = "../textures/player/playerpink.png"
                            self._Paused = not self._Paused
                            self._PlayerSelect = False
                        if self._text_rect_orange.collidepoint(pygame.mouse.get_pos()):
                            self._Player._SelectedPlayerColour = "orange"
                            self._Player._SelectedSpriteSheet = "../textures/player/playerorange.png"
                            self._Paused = not self._Paused
                            self._PlayerSelect = False
                        if self._text_rect_grey.collidepoint(pygame.mouse.get_pos()):
                            self._Player._SelectedPlayerColour = "grey"
                            self._Player._SelectedSpriteSheet = "../textures/player/playergrey.png"
                            self._Paused = not self._Paused
                            self._PlayerSelect = False
            

    def save(self):
        print("returning: ", self._Location)
        return self._Location

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()


    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - ScreenWidth / 2
        self.offset.y = player.rect.centery - ScreenHeight / 2

        for layer in LAYERS.values():  # iterate through LAYERS and draw in order the sprites
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery): # Sorted, based on sprites y pos, to see which sprite is in front.
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

                    #hitbox,collision box and interaction box debug visuals
                    '''
                    if sprite == player:
                        pygame.draw.rect(self.display_surface,'red',offset_rect,5)
                        hitbox_rect =player.hitbox.copy()
                        hitbox_rect.center = offset_rect.center
                        pygame.draw.rect(self.display_surface,'green',hitbox_rect,5)
                        target_pos = offset_rect.center + PlayerToolOffset[player._status.split('-')[0]]
                        pygame.draw.circle(self.display_surface,'blue',target_pos,5)
                    '''
