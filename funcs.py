import os
import sys
import pygame
import random

pygame.init()
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h - 20
screen = pygame.display.set_mode((width, height))
screen.fill('black')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def getRandPos():
    s = set()
    while len(s) != 2:
        r = random.randint(0, 2)
        s.add(r)
    return list(s)

