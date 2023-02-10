import pygame

class Timer:
    def __init__(self,duration,func = None):
        self._Duration = duration
        self.func = func
        self._StartTime = 0
        self._Active = False
    
    def activate(self):
        self._Active = True
        self._StartTime = pygame.time.get_ticks()

    def deactivate(self):
        self._Active = False
        self._StartTime = 0

    def update(self):
        CurrentTime = pygame.time.get_ticks()
        if CurrentTime - self._StartTime >= self._Duration:
            if self.func and self._StartTime != 0:
                self.func()
            self.deactivate()