import pygame
from funcs import load_image


class Hero(pygame.sprite.Sprite):
    image = load_image('creature.png', -1)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Hero.image
        self.rect = self.image.get_rect()

