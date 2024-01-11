import sys
import time

import pygame
from funcs import getRandPos
from hero import Hero
from back_ground import Background
from barrier import Barrier
from enemy import Enemy


class Game:
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Musorniy gorod')
        self.offset = self.height - self.height // 3
        running = True
        # /// Параметры спрайтов
        self.cords = {
            0: self.height - self.offset // 3 * 2,
            1: self.height - self.offset // 3,
            2: self.height
        }
        self.all_sprites = pygame.sprite.Group()
        self.font_sprites = pygame.sprite.Group()
        self.barriers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.back = Background()
        self.hero = Hero(cords=self.cords)
        self.poses = getRandPos()
        self.all_sprites.add(self.hero)
        self.font_sprites.add(self.back)
        self.object_width, self.object_height = self.hero.rect.width, self.hero.rect.height
        self.hero.rect.left = self.width // 2 - self.object_width // 2
        self.hero.rect.bottom = self.height - self.offset // 3
        self.lastTimeSpawnBar = time.time()
        self.lastTimeSpawnEnm = time.time() + 1.5
        self.frequencyBar = 3
        self.frequencyEnm = 12
        # ///
        self.font_sprites.draw(self.screen)
        self.all_sprites.draw(self.screen)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.hero.curLine -= 1
                        if self.hero.curLine < 0:
                            self.hero.curLine = 0
                    if event.key == pygame.K_s:
                        self.hero.curLine += 1
                        if self.hero.curLine > 2:
                            self.hero.curLine = 2
            self.update()
            self.draw()
            self.collision()

    def draw(self):
        self.background()
        self.font_sprites.draw(self.screen)
        self.drawing_lines()
        self.all_sprites.draw(self.screen)
        self.barriers.draw(self.screen)
        self.enemies.draw(self.screen)
        pygame.display.flip()

    def update(self):
        self.all_sprites.update()
        self.barriers.update()
        self.enemies.update()
        self.handleSpawnBar()
        self.handleSpawnEnm()

    def handleSpawnBar(self):
        self.poses = getRandPos()
        if time.time() - self.lastTimeSpawnBar >= self.frequencyBar:
            self.lastTimeSpawnBar = time.time()
            self.barriers.add(
                Barrier(
                    cords=self.cords,
                    scr_width=self.width,
                    pos=self.poses[0]
                ),
                        Barrier(
                    cords=self.cords,
                    scr_width=self.width,
                    pos=self.poses[1]
                        ))

    def handleSpawnEnm(self):
        self.poses = getRandPos()
        if time.time() - self.lastTimeSpawnEnm >= self.frequencyEnm:
            self.lastTimeSpawnEnm = time.time()
            self.enemies.add(
                        Enemy(
                    cords=self.cords,
                    scr_width=self.width,
                    pos=self.poses[0]
                        )
            )

    def drawing_lines(self):
        pygame.draw.line(self.screen, 'white', (0, self.height),
                         (self.width, self.height), width=10)
        pygame.draw.line(self.screen, 'white', (0, self.height - self.offset // 3),
                         (self.width, self.height - self.offset // 3), width=5)
        pygame.draw.line(self.screen, 'white', (0, self.height - self.offset // 3 * 2),
                         (self.width, self.height - self.offset // 3 * 2), width=5)
        pygame.draw.line(self.screen, 'white', (0, self.height / 3),
                         (self.width, self.height / 3), width=10)

    def background(self):
        if self.back.rect.right == self.width:
            self.back.kill()
            new_back = Background()
            self.back = new_back
            self.font_sprites.add(self.back)
        self.back.rect.left -= 1

    def collision(self):
        if pygame.sprite.spritecollide(self.hero, self.barriers, False, pygame.sprite.collide_mask):
            print(1)
            sys.exit()
        if pygame.sprite.spritecollide(self.hero, self.enemies, False, pygame.sprite.collide_mask):
            print(2)
            sys.exit()


if __name__ == '__main__':
    Game()
