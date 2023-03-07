from sprites import *
from settings import *
from random import randint
from timer import Timer


class Animal(Generic):
    # TODO:Add interaction(milk(bucket can be purchased)), mooing, spawning in multiple
    def __init__(self, pos, frames, groups, collision_sprites, scale=Scale):

        # Animate
        self._frames = frames
        self._frameIndex = 0
        self._animSpeed = 2

        self.timer = {
            'animal walk': Timer(3000)
        }

        super().__init__(pos=pos, surface=self._frames[self._frameIndex], groups=groups, z=LAYERS['main'])
        self.scale = scale
        self.image = self._frames[self._frameIndex]
        self.rect = self.image.get_rect(topleft=pos)
        # hitbox dramatically smaller on vertical because of overlap of player and sprites
        self.image = pygame.transform.scale(self._frames[self._frameIndex], (self.image.get_width() * scale, self.image.get_height() * scale))
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.15, -self.rect.height * 0.25)
        self.collision_sprites = collision_sprites

        # Move
        self._GoDir = "None"
        self._Direction = pygame.math.Vector2()
        self._Position = pygame.math.Vector2(self.rect.center)
        self._Speed = 110
        self._Distance = 0

    def animate(self, Deltatime):
        self._frameIndex += self._animSpeed * Deltatime
        if self._frameIndex >= len(self._frames):
            self._frameIndex = 0
        self.image = self._frames[int(self._frameIndex)]

    def make_move(self):
        print('choose: ', self._Distance)
        self._ChooseDir = randint(0, 3)
        if self._ChooseDir == 0:
            self._GoDir = "up"
        elif self._ChooseDir == 1:
            self._GoDir = "down"
        elif self._ChooseDir == 2:
            self._GoDir = "left"
        elif self._ChooseDir == 3:
            self._GoDir = "right"
        else:
            self._GoDir = "None"

    def move(self, DeltaTime):
        if self._Distance == 0:
            self.make_move()
            if self._GoDir == "up":
                print('cow up')
                self._Direction.y = -1
                self._Distance = randint(10, 50)

            elif self._GoDir == "down":
                print('cow down')
                self._Direction.y = 1
                self._Distance = randint(10, 50)
            else:
                self._Direction.y = 0
                self._Distance = randint(10, 50)

            if self._GoDir == "left":
                print('cow left')
                self._Direction.x = -1
                self._Distance = randint(10, 50)
            elif self._GoDir == "right":
                print('cow right')
                self._Direction.x = 1
                self._Distance = randint(10, 50)
            else:
                self._Direction.x = 0
                self._Distance = randint(10, 50)

        if self._Distance != 0:
            print(self._Distance)
            # normalize vector (cant speed up by walking diagonally)
            if self._Direction.magnitude() > 0:
                self._Direction = self._Direction.normalize()

            # movement on x axis
            self._Position.x += self._Direction.x * self._Speed * DeltaTime
            self.hitbox.centerx = round(self._Position.x)  # rounding to prevent truncation
            self.rect.centerx = self.hitbox.centerx
            self.collision('horizontal')

            # movement on y axis
            self._Position.y += self._Direction.y * self._Speed * DeltaTime
            self.hitbox.centery = round(self._Position.y)  # rounding to prevent truncation
            self.rect.centery = self.hitbox.centery
            self.collision('vertical')

            self._Distance -= 1

    def collision(self, _Direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):  # Checks if sprite has collision
                if sprite.hitbox.colliderect(self.hitbox):  # Checks if there is a collision
                    if _Direction == 'horizontal':
                        if self._Direction.x > 0:  # player moving to the right
                            self.hitbox.right = sprite.hitbox.left
                        if self._Direction.x < 0:  # player moving to the left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self._Position.x = self.hitbox.centerx
                    if _Direction == 'vertical':
                        if self._Direction.y > 0:  # player moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self._Direction.y < 0:  # player moving up
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self._Position.y = self.hitbox.centery

    def update(self, DeltaTime):
        self.animate(DeltaTime)
        self.move(DeltaTime)
