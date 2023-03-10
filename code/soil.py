import pygame, json
from settings import *
from pytmx.util_pygame import load_pygame
from tools import *
from random import choice
from pygame import mixer

class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.image = pygame.transform.scale(surface, (self.image.get_width() * Scale, self.image.get_height() * Scale))
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil']

class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil water']

class Plant(pygame.sprite.Sprite):
    def __init__(self, plantType, groups, soil, checkWatered):
        super().__init__(groups)
        self._PlantType = plantType
        self._Frames = import_folder(f'../textures/plants/{plantType}')
        self._Soil = soil
        self._CheckWatered = checkWatered
        self._PlantAge = 0
        self._MaxPlantAge = len(self._Frames) - 1
        self._PlantGrowthSpeed = PlantGrowthSpeed[self._PlantType]
        self._PlantGrown = False

        self.image = self._Frames[self._PlantAge]

        self.y_offset = -16 if plantType == 'corn' else -8
        self.rect = self.image.get_rect(midbottom = soil.rect.midbottom + pygame.math.Vector2(0,self.y_offset))
        self.z = LAYERS['ground plant']
    
    def grow(self):
        if self._CheckWatered(self.rect.center):
            self._PlantAge += self._PlantGrowthSpeed

            if int(self._PlantAge) > 0:
                self.z = LAYERS['main']
                self.hitbox = self.rect.copy().inflate(-26, -self.rect.height * 0.4)

            if self._PlantAge >= self._MaxPlantAge:
                self._PlantAge = self._MaxPlantAge
                self._PlantGrown = True

            self.image = self._Frames[int(self._PlantAge)]
            self.image.get_rect(midbottom = self._Soil.rect.midbottom + pygame.math.Vector2(0,self.y_offset))
            
class SoilLayer:
    def  __init__(self, _AllSprites, CollisionSprites):

        # Sprite Groups
        self._AllSprites = _AllSprites
        self._CollisionSprites = CollisionSprites
        self._SoilSprites = pygame.sprite.Group()
        self._WaterSprites = pygame.sprite.Group()
        self._PlantSprites = pygame.sprite.Group()
        mixer.init()

        # Graphics
        self._SoilSurfaces = import_folder_dict('../textures/soil/')
        self._WaterSurfaces = import_folder('../textures/soil_water/')

        self._saveFile = json.load(open("../profiles/save1.json"))

        self.create_soil_grid()
        self.create_hit_rects()

    def create_soil_grid(self):  # used for management of entities to reduce calculations, Each tile mapped out
        if self._saveFile['map'] == "None":
            ground = pygame.image.load('../data/Farm.png')
            h_tiles, v_tiles = ground.get_width() // TileSize, ground.get_height() // TileSize
            self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]
            for x, y, _ in load_pygame('../data/Farm.tmx').get_layer_by_name('Farmable').tiles():  # _ ignores the surface
                self.grid[y][x].append('F')
        else:
            self.grid = self._saveFile['map']
            self.create_soil_tiles()

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
                    if self.raining:
                        self.water_all()

    def water(self, _TargetPosition):
        for soil_sprite in self._SoilSprites.sprites():
            if soil_sprite.rect.collidepoint(_TargetPosition):
                x, y = soil_sprite.rect.x // (TileSize * Scale), soil_sprite.rect.y // (TileSize * Scale)
                self.grid[y][x].append('W')  # Appends 'W' to Grid to know which tile is watered
                pos = soil_sprite.rect.topleft
                surface = choice(self._WaterSurfaces)
                WaterTile(pos, surface, [self._AllSprites, self._WaterSprites])

    def water_all(self):  # Water all tiles when raining
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell and 'W' not in cell:
                    cell.append('W')
                    x, y = index_col * TileSize * Scale, index_row * TileSize * Scale
                    WaterTile((x, y), choice(self._WaterSurfaces), [self._AllSprites, self._WaterSprites])
                    print('W')

    def dry_soil_tiles(self):  # TO be called at day start
        for sprite in self._WaterSprites.sprites():
            sprite.kill()

        for row in self.grid:
            for cell in row:
                if 'W' in cell:
                    for char in cell:
                        if char == 'W':
                            cell.remove('W')

    def CheckWatered(self,pos):
        x, y = pos[0] // (TileSize * Scale), pos[1] // (TileSize * Scale)
        cell = self.grid[y][x]
        isWatered = 'W' in cell
        return isWatered

    def PlantSeed(self,targetPosition, Seed):
        for soilSprite in self._SoilSprites.sprites():
            if soilSprite.rect.collidepoint(targetPosition):
                x, y = soilSprite.rect.x // (TileSize * Scale), soilSprite.rect.y // (TileSize * Scale)
                if 'P' not in self.grid[y][x]:
                    self.grid[y][x].append('P')
                    PlantSound = mixer.Sound("../audio/plant.wav")
                    PlantSound.set_volume(0.02)
                    PlantSound.play()
                    Plant(Seed, [self._AllSprites, self._PlantSprites, self._CollisionSprites], soilSprite ,self.CheckWatered)
    
    def updatePlants(self):
        #THIS METHOD NEEDS TO BE CALLED ON DAY RESET
        for plant in self._PlantSprites.sprites():
            plant.grow()

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
                    elif all((l, r, t, tl)) and not b: tile_type = 'lrbtl'
                    elif all((l, r, t, tr)) and not b: tile_type = 'lrbtr'
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

                if 'W' in cell:
                    self.water((index_col * TileSize * Scale, index_row * TileSize * Scale))

    def save(self):
        return self.grid