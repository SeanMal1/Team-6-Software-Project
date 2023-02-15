import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from tools import *

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
        self._SoilSurfaces = import_folder_dict('../textures/soil/')

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
        self._SoilSprites.empty()  # Empty all soil sprites and redraw so that Tile connections work
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell:

                    # tile options
                    t = 'X' in self.grid[index_row - 1][index_col]
                    b = 'X' in self.grid[index_row + 1][index_col]
                    l = 'X' in self.grid[index_row][index_col - 1]
                    r = 'X' in self.grid[index_row][index_col + 1]
                    tl = 'X' in self.grid[index_row - 1][index_col - 1]
                    tr = 'X' in self.grid[index_row - 1][index_col + 1]
                    bl = 'X' in self.grid[index_row + 1][index_col - 1]
                    br = 'X' in self.grid[index_row + 1][index_col + 1]

                    # Layout
                    # [tl][t ][tr]
                    # [l ][x ][r ]
                    # [bl][b ][br]

                    # Massive If statement block for checking tile location in grid
                    tile_type = 'o'
                    # Centre
                    if all((t,b,l,r)): tile_type = 'x'
                    # Middle Sides
                    elif all((t, b, r, tr, br)) and not l: tile_type = 'lm'
                    elif all((t, b, l, tl, bl)) and not r: tile_type = 'rm'
                    elif all((l, r, t, tl, tr)) and not b: tile_type = 'bm'
                    elif all((l, r, b, bl, br)) and not t: tile_type = 'tm'
                    # Horizontal only
                    elif l and not any((t,b,r)): tile_type = 'r'
                    elif r and not any((t,b,l)): tile_type = 'l'
                    elif r and l and not any((t, b)): tile_type = 'lr'
                    # Vertical only
                    elif t and not any((b, l, r)): tile_type = 'b'
                    elif b and not any((t, l, r)): tile_type = 't'
                    elif t and b and not any((l, r)): tile_type = 'tb'
                    # Corners
                    elif l and b and not any((t, r)): tile_type = 'tr'
                    elif r and b and not any((t, l)): tile_type = 'tl'
                    elif l and t and not any((b, r)): tile_type = 'br'
                    elif r and t and not any((b, l)): tile_type = 'bl'
                    # Complex
                    elif all((t, b, r, tr)) and not l: tile_type = 'tbrtr'
                    elif all((t, b, r, br)) and not l: tile_type = 'tbrbr'
                    elif all((t, b, l, tl)) and not r: tile_type = 'tbltl'
                    elif all((t, b, l, bl)) and not r: tile_type = 'tblbl'
                    elif all((l, r, b, tl)) and not b: tile_type = 'lrbtl'
                    elif all((l, r, b, bl)) and not b: tile_type = 'lrbbl'
                    elif all((l, r, b, br)) and not t: tile_type = 'lrtbr'
                    elif all((l, r, b, bl)) and not t: tile_type = 'lrtbl'
                    # T-Shapes
                    elif all((t, b, r)) and not l: tile_type = 'tbr'
                    elif all((t, b, l)) and not r: tile_type = 'tbl'
                    elif all((l, r, t)) and not b: tile_type = 'lrb'
                    elif all((l, r, b)) and not t: tile_type = 'lrt'


                    SoilTile(pos=(index_col * TileSize * Scale, index_row * TileSize * Scale),
                             surface=self._SoilSurfaces[tile_type],
                             groups=[self._AllSprites, self._SoilSprites])
