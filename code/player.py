import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.image = pygame.Surface((30,56))
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)