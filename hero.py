import pygame
import time
from pathlib import Path


class Hero(pygame.sprite.Sprite):

    def __init__(self, *group, cords):
        super().__init__(*group)
        self.cords = cords
        self.frames = []
        for frameFile in Path('sprites/hero_frames').glob('*.png'):
            self.frames.append(pygame.image.load(frameFile).convert_alpha())
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.y = self.rect.bottom
        self.mask = pygame.mask.from_surface(self.image)
        self.curLine = 1
        self.frameTime = 0.15
        self.frameIndex = 0
        self.lastFrameTime = time.time()

    def update(self, dt):
        self.handleAnimation()
        self.handleMovement(dt)

    def handleAnimation(self):
        if time.time() - self.lastFrameTime >= self.frameTime:
            self.frameIndex += 1
            self.frameIndex %= len(self.frames)
            self.lastFrameTime = time.time()
            x = self.rect.centerx
            self.image = self.frames[self.frameIndex]
            self.rect = self.image.get_rect()
            self.rect.center = x, self.y

    def handleMovement(self, dt):
        if abs(self.y - self.cords[self.curLine]) < 3:
            pass
        elif self.y > self.cords[self.curLine]:
            self.y -= 400 * dt
        elif self.y < self.cords[self.curLine]:
            self.y += 400 * dt
        self.rect.bottom = round(self.y)
