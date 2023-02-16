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

    def display_seed(self):
        pygame.draw.rect(self._DisplaySurface, (255, 255, 255, 0), pygame.Rect(ScreenWidth-80, ScreenHeight-80, 70, 70), border_radius=20)
        self._DisplaySurface.blit(pygame.transform.scale(self._SeedsOverlay[self._Player._SelectedSeed],(48,48)), (ScreenWidth-75, ScreenHeight-65))

    def Display(self):
        self.display_tools()
        self.display_seed()