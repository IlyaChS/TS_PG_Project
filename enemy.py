import pygame
import time
from pathlib import Path
from funcs import cursor


class Enemy(pygame.sprite.Sprite):

    def __init__(self, *group, cords, scr_width, pos, level):
        super().__init__(*group)
        self.level = level
        self.scrWidth = scr_width
        self.pos = pos
        self.cords = cords
        self.frames = []
        for frameFile in Path(cursor.execute(f'SELECT enemy FROM {self.level}').fetchone()[0]).glob('*.png'):
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
        self.x = self.rect.left

    def update(self, dt):
        self.handleAnimation()
        self.handleMovement(dt)

    def handleAnimation(self):
        if time.time() - self.lastFrameTime >= self.frameTime:
            self.frameIndex += 1
            self.frameIndex %= len(self.frames)
            self.lastFrameTime = time.time()
            y = self.rect.centery
            self.image = self.frames[self.frameIndex]
            self.rect = self.image.get_rect()
            self.rect.center = self.x, y

    def handleMovement(self, dt):
        if self.rect.right == 0:
            self.kill()
        self.x -= 300 * dt
        self.rect.left = round(self.x)
