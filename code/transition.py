import pygame
import settings

#transition class
class Transition:
    def __init__(self, reset, player):
        # setup
        self._DisplaySurface = pygame.display.get_surface()
        self.reset = reset
        self._Player = player
        # overlay img
        self._Image = pygame.Surface((settings.ScreenWidth, settings.ScreenHeight))
        self._Colour = 255
        self._Speed = -2
    #method to start the transition
    def play(self, player):
        # Screen fade to black
        self._Colour += self._Speed
        self._Player = player
        if self._Colour <= 0:
            self._Speed *= -1
            self._Colour = 0  # Prevent negative num and break
        if self._Colour > 255:
            self._Colour = 255
            self._Player._Sleep = False
            self._Speed *= -1

        self._Image.fill((self._Colour, self._Colour, self._Colour))
        self._DisplaySurface.blit(self._Image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    #method to sleep
    def sleep(self):
        self.play(self._Player)
        self.reset()
