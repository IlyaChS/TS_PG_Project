import pygame
from funcs import load_image, cursor


class Background(pygame.sprite.Sprite):

    def __init__(self, *group, level):
        super().__init__(*group)
        self.image1 = load_image(cursor.execute(f'SELECT background FROM {level}').fetchone()[0])
        self.rect1 = self.image1.get_rect()
        self.image2 = load_image(cursor.execute(f'SELECT background FROM {level}').fetchone()[0])
        self.rect2 = self.image2.get_rect()
        self.rect1.left = 0
        self.rect2.left = self.rect1.right - 2
        self.x1 = self.rect1.left
        self.x2 = self.rect2.left

    def draw(self, screen):
        screen.blit(self.image1, self.rect1)
        screen.blit(self.image2, self.rect2)

    def update(self, dt):
        self.x1 -= 100 * dt
        self.x2 -= 100 * dt
        if self.rect1.right <= 0:
            self.rect1.left = self.rect2.right - 2
            self.x1 = self.rect1.left
        if self.rect2.right <= 0:
            self.rect2.left = self.rect1.right - 2
            self.x2 = self.rect2.left
        self.rect1.left = round(self.x1)
        self.rect2.left = round(self.x2)
