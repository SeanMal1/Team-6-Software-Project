import pygame
from settings import *
from pytmx.util_pygame import load_pygame

class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.image = pygame.transform.scale(surface, (self.image.get_width() * Scale, self.image.get_height() * Scale))
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil']

class SoilLayer:
    def  __init__(self, _AllSprites):

        # Sprite Groups
        self._AllSprites = _AllSprites
        self._SoilSprites = pygame.sprite.Group()

        # Graphics
        self._SoilSurface = pygame.image.load('../textures/soil/o.png')

        self.create_soil_grid()
        self.create_hit_rects()

    def create_soil_grid(self):  # used for management of entities to reduce calculations, Each tile mapped out
        ground = pygame.image.load('../data/Farm.png')
        h_tiles, v_tiles = ground.get_width() // TileSize, ground.get_height() // TileSize
        self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]
        for x, y, _ in load_pygame('../data/Farm.tmx').get_layer_by_name('Farmable').tiles():  # _ ignores the surface
            self.grid[y][x].append('F')

    def create_hit_rects(self):
        self._HitRects = []
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x, y = index_col * (TileSize * Scale), index_row * (TileSize * Scale)  # Scaling
                    rect = pygame.Rect(x, y, (TileSize * Scale), (TileSize * Scale))
                    self._HitRects.append(rect)

    def get_hit(self, point):
        for rect in self._HitRects:
            if rect.collidepoint(point):
                x, y = rect.x // (TileSize * Scale), rect.y // (TileSize * Scale)

                if 'F' in self.grid[y][x]:
                    self.grid[y][x].append('X')
                    self.create_soil_tiles()

    def create_soil_tiles(self):
        self._SoilSprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell:
                    SoilTile(pos=(index_col * TileSize * Scale, index_row * TileSize * Scale),
                             surface=self._SoilSurface,
                             groups=[self._AllSprites, self._SoilSprites])

