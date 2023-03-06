import pygame, sys, json
from settings import *
from world import Level
from pygame import mixer
from player import Player


class Game:
    def __init__(self):
        pygame.init()
        mixer.init()
        self._Screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
        pygame.display.set_caption('Valley Life')
        mixer.music.load("../audio/background.mp3")
        icon = pygame.image.load('../textures/player/icon.png')
        self._heading_font = pygame.font.Font('../font/joystixmonospace.otf', 45)
        self._text_color = "Black"
        self._button_color = (220, 220, 220)
        self._button_hover_color = (180, 180, 180)
        pygame.display.set_icon(icon)
        mixer.music.set_volume(0.04)
        mixer.music.play(-1,0.0)
        self._Clock = pygame.time.Clock()
        self._World = Level(self.restart)
        self._Player = Player(pos=self._World._Position,
                                  toggle_inventory=self._World.toggle_inventory,
                                  group=self._World._AllSprites,
                                  collision_sprites=self._World._CollisionSprites,
                                  tree_sprites=self._World._TreeSprites,
                                  soil_layer=self._World._SoilLayer,
                                  interaction=self._World._InteractionSprites,
                                  toggle_merchant=self._World.toggle_merchant,
                                  Level=self,
                                  restart=self.restart)

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
                    if self._World._text_rect_player_select.collidepoint(pygame.mouse.get_pos()):
                        self._World._PlayerSelect = True
                    if self._World._text_rect_green.collidepoint(pygame.mouse.get_pos()):
                        self._Player._SelectedPlayerColour = ""
                        self._Player._SelectedSpriteSheet = "../textures/player/playerblue.png"
                        self._World._Paused = not self._World._Paused
                        self._World._PlayerSelect = False
                    if self._World._text_rect_blue.collidepoint(pygame.mouse.get_pos()):
                        self._Player._SelectedPlayerColour = "blue"
                        self._Player._SelectedSpriteSheet = "../textures/player/playerlightblue.png"
                        self._World._Paused = not self._World._Paused#
                        self._World._PlayerSelect = False
                    if self._World._text_rect_red.collidepoint(pygame.mouse.get_pos()):
                        self._Player._SelectedPlayerColour = "red"
                        self._Player._SelectedSpriteSheet = "../textures/player/playerred.png"
                        self._World._Paused = not self._World._Paused
                        self._World._PlayerSelect = False
                    if self._World._text_rect_purple.collidepoint(pygame.mouse.get_pos()):
                        self._Player._SelectedPlayerColour = "purple"
                        self._Player._SelectedSpriteSheet = "../textures/player/playerpurple.png"
                        self._World._Paused = not self._World._Paused
                        self._World._PlayerSelect = False
                    if self._World._text_rect_pink.collidepoint(pygame.mouse.get_pos()):
                        self._Player._SelectedPlayerColour = "pink"
                        self._Player._SelectedSpriteSheet = "../textures/player/playerpink.png"
                        self._World._Paused = not self._World._Paused
                        self._World._PlayerSelect = False
                    if self._World._text_rect_orange.collidepoint(pygame.mouse.get_pos()):
                        self._Player._SelectedPlayerColour = "orange"
                        self._Player._SelectedSpriteSheet = "../textures/player/playerorange.png"
                        self._World._Paused = not self._World._Paused
                        self._World._PlayerSelect = False
                    if self._World._text_rect_grey.collidepoint(pygame.mouse.get_pos()):
                        self._Player._SelectedPlayerColour = "grey"
                        self._Player._SelectedSpriteSheet = "../textures/player/playergrey.png"
                        self._World._Paused = not self._World._Paused
                        self._World._PlayerSelect = False
            DeltaTime = self._Clock.tick() / 1000
            self._World.run(DeltaTime)
            pygame.display.update()

    def restart(self):
        print("restarting")
        new = json.load(open("../profiles/new.json"))
        with open("../profiles/save1.json", "w") as f:
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
