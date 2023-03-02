import pygame
from settings import *

class Inventory():
    def __init__(self, inventory, money, toggle_inventory):
        self._DisplaySurface = pygame.display.get_surface()
        self.toggle_inventory = toggle_inventory
        self._inventory = inventory
        self._money = money
        self._font = pygame.font.Font('../font/joystixmonospace.otf', 30)

        self._width = 400
        self._space = 10
        self._padding = 8

        self._prevKeystroke = None

    def input(self):
        keystroke = pygame.key.get_pressed()

        if self._prevKeystroke is not None:
                if self._prevKeystroke[pygame.K_e] and not keystroke[pygame.K_e]:
                    self.toggle_inventory()

        self._prevKeystroke = keystroke

    def display(self):
        self.input()
        self.main_rect = pygame.Rect(((ScreenWidth / 2) - (self._width / 2)) , 100, self._width, 100)
        self._inventory["money"] = self._money

        for i, item in enumerate(self._inventory):
            if i > 2:
                text_surf = self._font.render(item, False, 'Black')
                top = self.main_rect.top + i * (text_surf.get_height() + (self._padding * 2) + self._space)

                #background
                bg_rect = pygame.Rect(self.main_rect.left, top, self._width, text_surf.get_height() + (self._padding * 2))
                pygame.draw.rect(self._DisplaySurface, 'White', bg_rect, 0, 4)
                
                #text
                text_rect = text_surf.get_rect(midleft = (self.main_rect.left + 20, bg_rect.centery))
                self._DisplaySurface.blit(text_surf, text_rect)

                #amount
                amount_surf = self._font.render(str(self._inventory[item]), False, 'Black')
                amount_rect = amount_surf.get_rect(midright = (self.main_rect.right - 20, bg_rect.centery))

                self._DisplaySurface.blit(amount_surf, amount_rect)



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