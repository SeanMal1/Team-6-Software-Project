import pygame
from settings import *

class Overlay:
    def __init__(self,player):
        self._DisplaySurface = pygame.display.get_surface()
        self._Player = player
        OverlayPath = '../textures/ui/'

        self._ToolsOverlay = {tool:pygame.image.load(f'{OverlayPath}{tool}.png').convert_alpha() for tool in player._Tools}
        self._SeedsOverlay = {seed:pygame.image.load(f'{OverlayPath}{seed}.png').convert_alpha() for seed in player._Seeds}

    def Display(self):
        #seed
        SeedOverlay = self._SeedsOverlay[self._Player._SelectedSeed]
        SeedScaled = pygame.transform.scale(SeedOverlay,(48,48))
        SeedRect = SeedOverlay.get_rect(midbottom = OverlayPos['seed'])
        self._DisplaySurface.blit(SeedScaled,SeedRect)

        #tool
        ToolOverlay = self._ToolsOverlay[self._Player._SelectedTool]
        ToolScaled = pygame.transform.scale(ToolOverlay,(96,96))
        ToolRect = ToolOverlay.get_rect(midbottom = OverlayPos['tool'])
        self._DisplaySurface.blit(ToolScaled,ToolRect)