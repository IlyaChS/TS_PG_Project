import pygame
from pathlib import Path
import time
from funcs import cursor


class Boss(pygame.sprite.Sprite):
    def __init__(self, *group, pos, level):
        super().__init__(*group)
        self.level = level
        self.pos = pos
        self.frames = []
        for frameFile in Path(f'sprites/{cursor.execute(f"SELECT boss FROM {self.level}").fetchone()[0]}').glob("*.png"):
            self.frames.append(pygame.image.load(frameFile).convert_alpha())
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.left = self.pos[0]
        self.rect.bottom = self.pos[1]
        self.frameTime = 0.15
        self.frameIndex = 0
        self.lastFrameTime = time.time()
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
        self.x -= 400 * dt
        self.rect.left = round(self.x)
