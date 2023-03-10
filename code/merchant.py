import pygame
from settings import *
from timer import Timer

#Merchant instead of menu
class Merchant():
    def __init__(self,Player,toggle_merchant):

        #general setup
        self._Player = Player
        self.toggle_merchant = toggle_merchant
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/joystixmonospace.otf',30)
        self._prevKeystroke = None

        #options
        self.width = 400
        self.space = 10
        self.padding = 8

        #items
        self.options = list(self._Player._Inventory.keys())[3:] + list(self._Player.seed_inventory.keys())[3:]
        self.sell_border = len(self._Player._Inventory) - 4
        self.setup()

        #movement
        self.index = 0
        self.timer = {
            'merchant' : Timer(200)
        }

       
    # displays money at the bottom
    def display_money(self):
        text_surf = self.font.render(f'${self._Player.money}', False, 'Black')
        text_rect = text_surf.get_rect(midbottom = (ScreenWidth / 2, ScreenHeight - 20))

        pygame.draw.rect(self.display_surface, 'White', text_rect.inflate(10,10))
        self.display_surface.blit(text_surf, text_rect)

    # creates the merchant ui
    def setup(self):
        #create surfaces
        self.text_surfs = []
        self.total_height = 0
        for item in list(self._Player._Inventory.keys())[3:]:
            text_surf = self.font.render(item + ' ' + f'${SalePrices[item]}', False, 'Black')
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + (self.padding * 2)
        for item in list(self._Player.seed_inventory.keys())[3:]:
            text_surf = self.font.render(item + ' ' + f'${PurchasePrices[item]}', False, 'Black')
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + (self.padding * 2)

        self.total_height += (len(self.text_surfs) - 1) * self.space
        self.merchant_top = (ScreenHeight / 2) - (self.total_height / 2)
        self.main_rect = pygame.Rect(((ScreenWidth / 2) - (self.width / 2)) ,self.merchant_top, self.width, self.total_height)

         #buy/sell text surface
        self.buy_text = self.font.render('buy', False, 'Black')
        self.sell_text = self.font.render('sell', False, 'Black') 

    # User Controls
    def input(self):
        keystroke = pygame.key.get_pressed()
        

        if self._prevKeystroke is not None:
                if self._prevKeystroke[pygame.K_RETURN] and not keystroke[pygame.K_RETURN]:
                    self.toggle_merchant()
                if not self.timer['merchant']._Active:
                    if keystroke[pygame.K_UP]:
                        self.index -= 1
                        self.timer['merchant'].activate()
                    if keystroke[pygame.K_DOWN]:
                        self.index += 1
                        self.timer['merchant'].activate()
                        print('change down')
                    if keystroke[pygame.K_SPACE]:
                        self.timer['merchant'].activate()

                        #get item
                        item = self.options[self.index]

                        #sell
                        if self.index <= self.sell_border:
                            if self._Player._Inventory[item] > 0:
                                self._Player._Inventory[item] -=1
                                self._Player.money += SalePrices[item]


                        #buy
                        else:
                            seed_price = PurchasePrices[item]
                            if self._Player.money >= seed_price:
                                self._Player.seed_inventory[item] +=1
                                self._Player.money -= PurchasePrices[item]

                
                

        self._prevKeystroke = keystroke 

    
        #clamp the values
        if self.index < 0:
            self.index = len(self.options) - 1
        if self.index > len(self.options) - 1:
            self.index = 0
            
    def updateTimers(self):
        for timer in self.timer.values():
            timer.update()

    
    
    def show_entry(self, text_surf, amount, top, selected):
        #background
        bg_rect = pygame.Rect(self.main_rect.left, top, self.width, text_surf.get_height() + (self.padding * 2))
        pygame.draw.rect(self.display_surface, 'White', bg_rect, 0, 4)
        
        #text
        text_rect = text_surf.get_rect(midleft = (self.main_rect.left + 20, bg_rect.centery))
        self.display_surface.blit(text_surf, text_rect)
        #amount
        amount_surf = self.font.render(str(amount), False, 'Black')
        amount_rect = amount_surf.get_rect(midright = (self.main_rect.right - 20, bg_rect.centery))

        self.display_surface.blit(amount_surf, amount_rect)

        #selected
        if selected:
            pygame.draw.rect(self.display_surface, 'black', bg_rect, 4, 4)
            if self.index <= self.sell_border: #sell
                pos_rect = self.sell_text.get_rect(midleft = (self.main_rect.left + 235, bg_rect.centery))
                self.display_surface.blit(self.sell_text, pos_rect)
            else: #buy
                pos_rect = self.buy_text.get_rect(midleft = (self.main_rect.left + 235, bg_rect.centery))
                self.display_surface.blit(self.buy_text, pos_rect)



    def update(self):
        self.input()
        self.display_money()
        self.updateTimers()
        #pygame.draw.rect(self.display_surface, 'red', self.main_rect)
        #self.display_surface.blit(pygame.Surface((1000,1000)),(0,0))
        for text_index, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)
            amount_list = list(self._Player._Inventory.values())[3:] + list(self._Player.seed_inventory.values())[3:]
            amount = amount_list[text_index]
            self.show_entry(text_surf, amount, top, self.index == text_index)
            #self.display_surface.blit(text_surf, (100,text_index * 50)) 

 

