from sprites import *
from settings import *


class Animal(Generic):
    def __init__(self, pos, frames, groups, scale=Scale):

        # Animate
        self._frames = frames
        self._frameIndex = 0
        self._animSpeed = 4

        super().__init__(pos=pos, surface=self._frames[self._frameIndex], groups=groups, z=LAYERS['main'])
        self.scale = scale
        self.image = self._frames[self._frameIndex]
        self.rect = self.image.get_rect(topleft=pos)
        # hitbox dramatically smaller on vertical because of overlap of player and sprites
        self.image = pygame.transform.scale(self._frames[self._frameIndex], (self.image.get_width() * scale, self.image.get_height() * scale))
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.15, -self.rect.height * 0.25)

    def animate(self, Deltatime):
        self._frameIndex += self._animSpeed * Deltatime
        if self._frameIndex >= len(self._frames):
            self._frameIndex = 0
        self.image = self._frames[int(self._frameIndex)]

    def update(self, DeltaTime):
        self.animate(DeltaTime)
