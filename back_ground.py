import pygame
from funcs import load_image


class Background(pygame.sprite.Sprite):
    image = load_image('background3.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Background.image
        self.rect = self.image.get_rect()
