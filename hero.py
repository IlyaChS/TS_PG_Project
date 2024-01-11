import pygame
import time
from pathlib import Path


class Hero(pygame.sprite.Sprite):

    def __init__(self, *group, cords):
        super().__init__(*group)
        self.cords = cords
        self.frames = []
        for frameFile in Path('./hero_frames').glob('*.png'):
            self.frames.append(pygame.image.load(frameFile).convert_alpha())
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.curLine = 1
        self.frameTime = 0.15
        self.frameIndex = 0
        self.lastFrameTime = time.time()

    def update(self):
        self.handleAnimation()
        self.handleMovement()

    def handleAnimation(self):
        if time.time() - self.lastFrameTime >= self.frameTime:
            self.frameIndex += 1
            self.frameIndex %= len(self.frames)
            self.lastFrameTime = time.time()
            x, y = self.rect.center
            self.image = self.frames[self.frameIndex]
            self.rect = self.image.get_rect()
            self.rect.center = x, y

    def handleMovement(self):
        if self.rect.bottom > self.cords[self.curLine]:
            self.rect.bottom -= 1
        elif self.rect.bottom < self.cords[self.curLine]:
            self.rect.bottom += 1

