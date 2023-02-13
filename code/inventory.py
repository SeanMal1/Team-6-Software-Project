import pygame

class Inventory():
    def __init__(self, inventory, toggle_inventory):
        self._DisplaySurface = pygame.display.get_surface()
        self._font = pygame.font.Font('../font/joystixmonospace.otf', 20)
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
        for index, item in enumerate(self._inventory):
            if self._inventory[item] != 0:
                self._DisplaySurface.blit(self._font.render(item, False, "Black"), (100,100 * index))
                self._DisplaySurface.blit(self._font.render(str(self._inventory[item]), False, "Black"), (200,100 *index))

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