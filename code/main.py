import pygame, sys, json
from settings import *
from world import Level
from pygame import mixer


class Game:
    def __init__(self):
        pygame.init()
        mixer.init()
        self._Screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
        pygame.display.set_caption('Valley Life')
        mixer.music.load("../audio/background.mp3")
        icon = pygame.image.load('../textures/player/icon.png')
        pygame.display.set_icon(icon)
        mixer.music.set_volume(0.04)
        mixer.music.play(-1,0.0)
        self._Clock = pygame.time.Clock()
        self._World = Level(self.restart)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._World._Paused = not self._World._Paused
                if event.type == pygame.MOUSEBUTTONDOWN and self._World._Paused:
                    if self._World._text_rect_return.collidepoint(pygame.mouse.get_pos()):
                        self._World._Paused = not self._World._Paused
                    if self._World._text_rect_new.collidepoint(pygame.mouse.get_pos()):
                        self.restart()
                    if self._World._text_rect_quit.collidepoint(pygame.mouse.get_pos()):
                        self.save()
                        pygame.quit()
                        sys.exit()
            DeltaTime = self._Clock.tick() / 1000
            self._World.run(DeltaTime)
            pygame.display.update()

    def restart(self):
        print("restarting")
        new = json.load(open("../profiles/save1.json"))
        with open("../profiles/new.json", "w") as f:
            f.write(json.dumps(new))

        self._World.__init__(self)

    def save(self):
        save = self._World._Player.save()
        save["map"] = self._World._SoilLayer.save()
        save["location"] = self._World.save()
        save["firstTimePlaying"] = "False"
        with open("../profiles/save1.json", "w") as f:
            f.write(json.dumps(save))

if __name__ == '__main__':
    game = Game()
    game.run()
