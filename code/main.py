import pygame, sys
from settings import *
from world import Level


class Game:
    def __init__(self):
        pygame.init()
        self._Screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
        pygame.display.set_caption('Valley Life')
        icon = pygame.image.load('../textures/icon.png')
        pygame.display.set_icon(icon)
        self._Clock = pygame.time.Clock()
        self._World = Level()
        

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save()
                    pygame.quit()
                    sys.exit()
            DeltaTime = self._Clock.tick() / 1000
            self._World.run(DeltaTime)
            pygame.display.update()

    def save(self):
        self._World._Player.save()


if __name__ == '__main__':
    game = Game()
    game.run()