import pygame

class Timer:
    def __init__(self,duration,func = None):
        self._Duration = duration
        self._Function = func
        self._StartTime = 0
        self._Activate = False
    
    def activate(self):
        self._Activate = True
        self._StartTime = pygame.time.get_ticks()

    def deactivate(self):
        self._Activate = False
        self._StartTime

    def update(self):
        CurrentTime = pygame.time.get_ticks()
        if CurrentTime - self._StartTime >= self._Duration:
            self.deactivate()
            if self._Function:
                self._Function()