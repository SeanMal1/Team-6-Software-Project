import pygame
from settings import *

class Inventory():
    def __init__(self, inventory, toggle_inventory):
        self._DisplaySurface = pygame.display.get_surface()
        self.toggle_inventory = toggle_inventory
        self._inventory = inventory
        
        self._items = list(inventory.keys())[3:] # skips tools part of inventory

        inventory_path = '../textures/inventory/'
        self._inventory_overlay = {item:pygame.image.load(f'{inventory_path}{item}.png') for item in self._items} # list splice skips tools saved in inventory

        self._font = pygame.font.Font('../font/joystixmonospace.otf', 14)

        self._prevKeystroke = None

    def input(self):
        keystroke = pygame.key.get_pressed()

        if self._prevKeystroke is not None:
                if self._prevKeystroke[pygame.K_e] and not keystroke[pygame.K_e]:
                    self.toggle_inventory()

        self._prevKeystroke = keystroke

    def display(self):
        self.input()
        pygame.draw.rect(self._DisplaySurface, (255, 255, 255, 0), pygame.Rect(215, ScreenHeight-80, 280, 70), border_radius=20)
        for i, item in enumerate(self._items):
            self._DisplaySurface.blit(pygame.transform.scale(self._inventory_overlay[item], (58, 58)), (220 + 70*i, ScreenHeight-75))
            self._DisplaySurface.blit(self._font.render(str(self._inventory[item]), False, "Black"), (215+48 + 70*i, ScreenHeight-75+48))



    def addItem(self, item):
        if item in self._inventory:
            self._inventory['item'] += 1
        else:
            self._inventory['item'] = 1

    def removeItem(self, item):
        if item in self._inventory:
            self._inventory['item'] += 1
            if self._inventory['item'] == 0:
                del self._inventory['item']

    def save(self):
        return self._inventory