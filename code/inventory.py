import pygame

class Inventory():
    def __init__(self, inventory):
        self._DisplaySurface = pygame.display.get_surface()
        self._inventory = inventory
        self._open = False
        print("inventory initialised")

    def toggleDisplay(self):
        if not self._open:
            print("displaying")
            self._open = True
        else:
            print("closing")
            self._open = False

    def save(self):
        return self._inventory