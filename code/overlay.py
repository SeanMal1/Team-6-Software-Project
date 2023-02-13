import pygame
from settings import *

class Overlay:
    def __init__(self,player):
        self._DisplaySurface = pygame.display.get_surface()
        self._Player = player
        OverlayPath = '../textures/ui/'

        self._ToolsOverlay = {tool:pygame.image.load(f'{OverlayPath}{tool}.png').convert_alpha() for tool in player._Tools}
        self._SeedsOverlay = {seed:pygame.image.load(f'{OverlayPath}{seed}.png').convert_alpha() for seed in player._Seeds}

    def display_tools(self):
        pygame.draw.rect(self._DisplaySurface, (255, 255, 255, 0), pygame.Rect(5, ScreenHeight-80, 200, 70), border_radius=20)
        
        for (i, tool) in enumerate(self._Player._Tools):
            self._DisplaySurface.blit(pygame.transform.scale(self._ToolsOverlay[tool],(48,48)), (20 + 60*i, ScreenHeight-70))
            if tool == self._Player._SelectedTool:
                pygame.draw.rect(self._DisplaySurface, (255, 0, 0), pygame.Rect(15 + 60*i, ScreenHeight-75, 58, 58), width=2, border_radius=10)

    def Display(self):
        #seed
        SeedOverlay = self._SeedsOverlay[self._Player._SelectedSeed]
        SeedScaled = pygame.transform.scale(SeedOverlay,(48,48))
        SeedRect = SeedOverlay.get_rect(midbottom = OverlayPos['seed'])
        self._DisplaySurface.blit(SeedScaled,SeedRect)

        #tool
        # ToolOverlay = self._ToolsOverlay[self._Player._SelectedTool]
        # ToolScaled = pygame.transform.scale(ToolOverlay,(96,96))
        # ToolRect = ToolOverlay.get_rect(midbottom = OverlayPos['tool'])
        # self._DisplaySurface.blit(ToolScaled,ToolRect)
        self.display_tools()