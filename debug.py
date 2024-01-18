import pygame
import random
from itertools import cycle

class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 20))
        self.image.set_colorkey((11, 12, 13))
        self.image.fill((11, 12, 13))
        pygame.draw.ellipse(self.image, pygame.Color('white'), self.image.get_rect())
        self.rect = self.image.get_rect(topleft=(x,y))

    def update(self, dt):
        self.rect.move_ip(dt/10, 0)
        if self.rect.left >= pygame.display.get_surface().get_rect().width:
            self.rect.right = 0

class DayScene:
    def __init__(self):
        self.clouds = pygame.sprite.Group(Cloud(0, 30), Cloud(100, 40), Cloud(400, 50))

    def draw(self, screen):
        screen.fill(pygame.Color('lightblue'))
        self.clouds.draw(screen)

    def update(self, dt):
        self.clouds.update(dt)

class NightScene:
    def __init__(self):
        sr = pygame.display.get_surface().get_rect()
        self.sky = pygame.Surface(sr.size)
        self.sky.fill((50,0,50))
        for x in random.sample(range(sr.width), 50):
            pygame.draw.circle(self.sky, (200, 200, 0), (x, random.randint(0, sr.height)), 1)
        self.clouds = pygame.sprite.Group(Cloud(70, 70), Cloud(60, 40), Cloud(0, 50), Cloud(140, 10), Cloud(100, 20))

    def draw(self, screen):
        screen.blit(self.sky, (0, 0))
        self.clouds.draw(screen)

    def update(self, dt):
        self.clouds.update(dt)


class Fader:

    def __init__(self, scene):
        self.need = scene
        self.scene = scene
        self.fading = None
        self.alpha = 0
        sr = pygame.display.get_surface().get_rect()
        self.veil = pygame.Surface(sr.size)
        self.veil.fill((0, 0, 0))

    def next(self):
        if not self.fading:
            self.fading = 'OUT'
            self.alpha = 0

    def draw(self, screen):
        self.veil.set_alpha(self.alpha)
        screen.blit(self.veil, (0, 0))

    def fadeIn(self):
        self.alpha = 255
        self.alpha -= 0.001
        if self.alpha < 0:
            pass

    def fadeOut(self):
        self.alpha = 0
        self.alpha += 0.001
        if self.alpha > 255:
            pass

    def update(self, dt):
        self.scene.update(dt)

        if self.fading == 'OUT':
            self.alpha += 8
            if self.alpha >= 255:
                self.fading = 'IN'
                self.scene = self.need

        else:
            self.alpha -= 8
            if self.alpha <= 0:
                self.fading = None


def main():
    screen_width, screen_height = 300, 300
    screen = pygame.display.set_mode((screen_width, screen_height))
    img = pygame.image.load('sprites/hero_frames/mainch.png')
    clock = pygame.time.Clock()
    dt = 0
    fading_in = False
    fading_out = False
    fader = Fader(NightScene())

    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_a:
                fading_in = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_d:
                fading_out = True
        screen.blit(img, (0, 0))
        if fading_in:
            fader.fadeIn()
        if fading_out:
            fader.fadeOut()
        fader.draw(screen)
        pygame.display.flip()
        dt = clock.tick(30)

main()