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
from random import randint

class Level:
    def __init__(self):
        self._Player = None
        self._DisplayWorld = pygame.display.get_surface()
        self._AllSprites = CameraGroup()
        self._TreeSprites = pygame.sprite.Group()
        self._CollisionSprites = pygame.sprite.Group() # To keep track of collide-able sprites
        self._InteractionSprites = pygame.sprite.Group()
        self._SoilLayer = SoilLayer(self._AllSprites, self._CollisionSprites)
        self._saveFile = json.load(open("../profiles/save1.json"))
        self.setup()
        self._SpriteSheetImage = pygame.image.load(self._saveFile["image"]).convert_alpha()
        self._SpriteSheetImage.set_colorkey([0, 0, 0])
        self._Overlay = Overlay(self._Player)
        self._DisplaySurface = pygame.display.get_surface()
        self._FullSurface = pygame.Surface((ScreenWidth,ScreenHeight))
        self._DayColour = [255,255,255]
        self._NightColour = (38,101,189)
        self.rain = Rain(self._AllSprites)
        self.raining = randint(0,28) > 3 # rains if randint higher than x
        self._SoilLayer.raining = self.raining
        
        self._heading_font = pygame.font.Font('../font/joystixmonospace.otf', 45)
        self._regular_font = pygame.font.Font('../font/joystixmonospace.otf', 16)


        self._inventory_open = False
        self._Paused = False
        self._main_menu = True
        self._inventory = Inventory(self._Player._Inventory, self.toggle_inventory)
        
    def toggle_inventory(self):
        self._inventory_open = not self._inventory_open

    def setup(self):
        tmx_data = load_pygame('../data/Farm.tmx')

        # Fence
        for x, y, surface in tmx_data.get_layer_by_name('Fence').tiles():
            Generic(pos=(x * TileSize * Scale, y * TileSize * Scale), surface=surface, groups=[self._AllSprites, self._CollisionSprites])

        # Water
        water_frames = import_folder('../data/Tilesets/water')
        for x, y, surface in tmx_data.get_layer_by_name('Water').tiles():
            Water(pos=(x * TileSize * Scale, y * TileSize * Scale), frames=water_frames, groups=self._AllSprites)

        # Decoration
        for obj in tmx_data.get_layer_by_name('Decoration'):
            Decoration(pos=(obj.x * Scale, obj.y * Scale), surface=obj.image, groups=[self._AllSprites, self._CollisionSprites])

        # Trees
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree(pos=(obj.x * Scale, obj.y * Scale), surface=obj.image, groups=[self._AllSprites, self._CollisionSprites,self._TreeSprites], name=obj.name, playerAdd= self.PlayerAdd)

        # House
        for x, y, surface in tmx_data.get_layer_by_name('Building Floor').tiles():
            Generic(pos=(x * TileSize * Scale, y * TileSize * Scale), surface=surface, groups=[self._AllSprites, self._CollisionSprites], z=LAYERS['house bottom'])
        for x, y, surface in tmx_data.get_layer_by_name('Building Wall').tiles():
            Generic(pos=(x * TileSize * Scale, y * TileSize * Scale), surface=surface, groups=[self._AllSprites, self._CollisionSprites], z=LAYERS['house bottom'])
        for x, y, surface in tmx_data.get_layer_by_name('Building Roof').tiles():
            Generic(pos=(x * TileSize * Scale, y * TileSize * Scale), surface=surface, groups=self._AllSprites, z=LAYERS['house top'])

        # Collision Tiles, Borders
        for x, y, surface in tmx_data.get_layer_by_name('Borders').tiles():
            Border(pos=(x * TileSize * Scale, y * TileSize * Scale), surface=pygame.Surface((TileSize * Scale, TileSize * Scale)), groups= self._CollisionSprites)

        # Ground
        Generic(pos=(0, 0),
                surface = pygame.image.load('../data/Farm.png').convert_alpha(),
                groups=self._AllSprites,
                z=LAYERS['ground'])

        # Player
        self._Player = Player(pos=(self._saveFile["position"]["x"], self._saveFile["position"]["y"]),
                              toggle_inventory=self.toggle_inventory,
                              group=self._AllSprites,
                              collision_sprites=self._CollisionSprites,
                              tree_sprites=self._TreeSprites,
                              soil_layer=self._SoilLayer,
                              interaction=self._InteractionSprites)
        for obj in tmx_data.get_layer_by_name('Interaction'):
            if obj.name == 'Trader':  # change to 'Bed', Trader just for testing
                Interaction(pos=(obj.x * Scale, obj.y * Scale), size=(obj.width, obj.height), groups=[self._InteractionSprites, self._AllSprites], name=obj.name)
                # Remove _AllSprites when done debugging

    def PlayerAdd(self,item):
        self._Player._Inventory[item] += 1

    def reset(self): # resetting day
        # Soil
        self._SoilLayer.dry_soil_tiles()
        self._SoilLayer.raining = self.raining
        if self.raining:
            self._SoilLayer.water_all()

    def run(self, DeltaTime):
        if self._main_menu:
            self._DisplayWorld.fill('black')
            self._AllSprites.custom_draw(self._Player)
            self._DisplaySurface.blit(pygame.image.load('../textures/misc/main_menu.png'), (ScreenWidth/2 - 640/2, ScreenHeight/2 - 533/2))
            self._DisplaySurface.blit(self._heading_font.render("Valley Life", False, "Black"), (ScreenWidth/2 - 390/2, ScreenHeight/2 - 55))
            self._DisplaySurface.blit(self._regular_font.render("Press Space to begin.", False, "Black"), (ScreenWidth/2 - 260/2, ScreenHeight/2 + 50))
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self._main_menu = False

        elif not self._Paused:
            self._DisplayWorld.fill('black')
            # self._AllSprites.draw(self._DisplayWorld)
            self._AllSprites.custom_draw(self._Player)
            if self._inventory_open:
                self._inventory.display()
            else:
                self._AllSprites.draw(self._SpriteSheetImage)
                self._AllSprites.update(DeltaTime)
            

                #day to night cycle
                for index, value in enumerate(self._NightColour):
                    if self._DayColour[index] > value:
                        self._DayColour[index] -= 4 * DeltaTime

            self._FullSurface.fill(self._DayColour)
            self._DisplaySurface.blit(self._FullSurface,(0,0), special_flags = pygame.BLEND_RGBA_MULT)

            # overlay/ui
            self._Overlay.Display()
            # rain
            if self.raining:
                self.rain.update()

    def save(self):
        pass

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