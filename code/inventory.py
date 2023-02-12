import pygame

class Inventory():
    def __init__(self, inventory, toggle_inventory):
        self._DisplaySurface = pygame.display.get_surface()
        self.toggle_inventory = toggle_inventory
        self._inventory = inventory
        self._prevKeystroke = None

    def input(self):
        keystroke = pygame.key.get_pressed()

        if self._prevKeystroke is not None:
                if self._prevKeystroke[pygame.K_e] and not keystroke[pygame.K_e]:
                    self.toggle_inventory()

        self._prevKeystroke = keystroke

    def display(self):
        self.input()
        self._DisplaySurface.blit(pygame.Surface((1000, 1000)),(0,0))

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