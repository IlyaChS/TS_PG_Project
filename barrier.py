import pygame
import time
from funcs import load_image


class Barrier(pygame.sprite.Sprite):
    image = load_image('trashbox.png', -1)

    def __init__(self, *group, cords, scr_width, pos):
        super().__init__(*group)
        self.scrWidth = scr_width
        self.cords = cords
        self.pos = pos
        self.image = Barrier.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.lastSpawnTime = time.time()
        self.rect.left = self.scrWidth
        self.rect.bottom = self.cords[self.pos]

    def update(self):
        self.handleMovement()

    def handleMovement(self):
        if self.rect.right == 0:
            self.kill()
        self.rect.left -= 1

