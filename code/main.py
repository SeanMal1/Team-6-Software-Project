import pygame, sys, json
from settings import *
from world import Level
from pygame import mixer

#class for the game
class Game:
    #initialization method for a number of varaibles
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

    #method of a number of tasks to be executed whilst the game is running
    def run(self):
        while True:
            #listens for events like game quit or key presses
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #listens for key presses
                if event.type == pygame.KEYDOWN:
                    #if escape pressed pause game
                    if event.key == pygame.K_ESCAPE:
                        self._World._Paused = not self._World._Paused
                #if the mouse button is clicked whilst over an option run the appropriate peice of code
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
            
            #implementation of delta time
            DeltaTime = self._Clock.tick() / 1000
            self._World.run(DeltaTime)
            pygame.display.update()

    #method to restart the game and rewrite the save file
    def restart(self):
        print("restarting")
        #create new json file
        new = json.load(open("../profiles/new.json"))
        #load new json file
        with open("../profiles/save1.json", "w") as f:
            f.write(json.dumps(new))

        self._World.__init__(self)

    #method to save data to the json save file
    def save(self):
        save = self._World._Player.save()
        save["map"] = self._World._SoilLayer.save()
        save["location"] = self._World.save()
        save["firstTimePlaying"] = "False"
        save["sky"] = self._World._Sky.save()
        with open("../profiles/save1.json", "w") as f:
            f.write(json.dumps(save))

#where the game is ran
if __name__ == '__main__':
    game = Game()
    game.run()
