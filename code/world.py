import pygame
import json
from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from tools import *
from overlay import Overlay

class Level:
    def __init__(self):
        self._Player = None
        self._DisplayWorld = pygame.display.get_surface()
        self._AllSprites = CameraGroup()
        self._CollisionSprites = pygame.sprite.Group() # To keep track of collide-able sprites
        self._saveFile = json.load(open("../profiles/save1.json"))
        self.setup()
        self._SpriteSheetImage = pygame.image.load(self._saveFile["image"]).convert_alpha()
        self._SpriteSheetImage.set_colorkey([0, 0, 0])
        self._Overlay = Overlay(self._Player)
        self._Paused = False

    def setup(self):
        tmx_data = load_pygame('../data/Farm.tmx')

        # Fence
        for x, y, surface in tmx_data.get_layer_by_name('Fence').tiles():
            Generic(pos=(x * TileSize * 3, y * TileSize * 3), surface=surface, groups=[self._AllSprites, self._CollisionSprites])

        # Water
        water_frames = import_folder('../data/Tilesets/water')
        for x, y, surface in tmx_data.get_layer_by_name('Water').tiles():
            Water(pos=(x * TileSize * 3, y * TileSize * 3), frames=water_frames, groups=self._AllSprites)
            # Generic((x * TileSize * 3, y * TileSize * 3), surface, self._AllSprites, LAYERS['water'])

        # Decoration
        for obj in tmx_data.get_layer_by_name('Decoration'):
            Decoration(pos=(obj.x * 3, obj.y * 3), surface=obj.image, groups=[self._AllSprites, self._CollisionSprites])

        # Trees
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree(pos=(obj.x * 3, obj.y * 3), surface=obj.image, groups=[self._AllSprites, self._CollisionSprites], name=obj.name)

        # Collision Tiles, Borders
        for x, y, surface in tmx_data.get_layer_by_name('Borders').tiles():
            Generic(pos=(x * TileSize * 3, y * TileSize * 3), surface=pygame.Surface((TileSize * 3, TileSize * 3)), groups=self._CollisionSprites)

        # Ground
        Generic(pos=(0, 0),
                surface = pygame.image.load('../data/Farm.png').convert_alpha(),
                groups=self._AllSprites,
                z=LAYERS['ground'])
        self._Player = Player((self._saveFile["position"]["x"], self._saveFile["position"]["y"]), self._AllSprites, self._CollisionSprites)


    def run(self, DeltaTime):
        if not self._Paused:
            self._DisplayWorld.fill('black')
            # self._AllSprites.draw(self._DisplayWorld)
            self._AllSprites.custom_draw(self._Player)
            self._AllSprites.draw(self._SpriteSheetImage)
            self._AllSprites.update(DeltaTime)
            self._Overlay.Display()


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
