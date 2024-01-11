import pygame
import time
from pathlib import Path


class Enemy(pygame.sprite.Sprite):

    def __init__(self, *group, cords, scr_width, pos):
        super().__init__(*group)
        self.scrWidth = scr_width
        self.pos = pos
        self.cords = cords
        self.frames = []
        for frameFile in Path('./enemy_frames').glob('*.png'):
            self.frames.append(pygame.image.load(frameFile).convert_alpha())
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.curLine = 1
        self.frameTime = 0.15
        self.frameIndex = 0
        self.lastFrameTime = time.time()
        self.rect.left = self.scrWidth
        self.rect.bottom = self.cords[self.pos]

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
        if self.rect.right == 0:
            self.kill()
        self.rect.left -= 1
