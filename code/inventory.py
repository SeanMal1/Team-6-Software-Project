import pygame

class Inventory():
    def __init__(self, inventory):
        self._DisplaySurface = pygame.display.get_surface()
        self._inventory = inventory
        self._open = False
        print("inventory initialised")

    def toggleDisplay(self):
        if not self._open:
            self._open = True
            self._paused = True
            print("displaying")
        else:
            print("closing")
            self._open = False
            self._paused = False

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