import pygame
from funcs import load_image


class Currency(pygame.sprite.Sprite):
    image = load_image('coin.png', -1)

    def __init__(self, *group, cords, pos_x, pos_y):
        super().__init__(*group)
        self.cords = cords
        self.posX = pos_x
        self.posY = pos_y
        self.image = Currency.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left = self.posX
        self.rect.bottom = self.cords[self.posY]
        self.x = self.rect.left

    def update(self, dt):
        self.handleMovement(dt)

    def handleMovement(self, dt):
        if self.rect.right == 0:
            self.kill()
        self.x -= 300 * dt
        self.rect.left = round(self.x)
