import os
import sys
import pygame
import random
import sqlite3

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


sound_data = {
    'coin': pygame.mixer.Sound('sounds/coin.ogg'),
    'barrier': pygame.mixer.Sound('sounds/Во-время-удара-об-мусорку_1.ogg'),
    'enemy_strike': pygame.mixer.Sound('sounds/Звук-удара-врага_1.ogg'),
    'hero_strike': pygame.mixer.Sound('sounds/Во-время-удара-героя.ogg'),
    'victory': pygame.mixer.Sound('sounds/Во-время-победы_обрез-конец_.ogg'),
    'lose': pygame.mixer.Sound('sounds/lose.ogg'),
    'enemy': pygame.mixer.Sound('sounds/enemy.ogg'),
    'button': pygame.mixer.Sound('sounds/button.ogg'),
    'boss': pygame.mixer.Sound('sounds/boss.ogg')
}


def play_sound(sound, value):
    s = sound
    pygame.mixer.Sound.set_volume(s, value)
    s.play()


con = sqlite3.connect('levels.sqlite')
cursor = con.cursor()


def download_stats():
    with open('money X stats', 'r') as file:
        info = file.readlines()
    return int(info[0].split()[1]), int(info[1].split()[1]), int(info[2].split()[1])


def upload_stats(money, power, defense):
    with open('money X stats', 'w') as file:
        file.write(f'money: {money}\npower: {power}\ndefense: {defense + 10}')


def read_boss_file():
    with open('check_bosses.txt') as file:
        res = file.readlines()
    return int(res[0].split()[1]), int(res[1].split()[1])


def write_boss_file(rot, rat):
    with open('check_bosses.txt', 'w') as file:
        file.write(f'rot: {rot}\nrat: {rat}')
