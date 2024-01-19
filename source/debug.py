import pygame
import time
from random import randint
from pathlib import Path
import sqlite3
import os
import sys
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)


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
        r = randint(0, 2)
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


class Levels:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.YELLOW = (235, 205, 3)
        self.image = pygame.image.load('data/choose_level_background.png')
        self.mini1 = pygame.image.load('data/background_mini.png')
        self.mini2 = pygame.image.load('data/2background_mini.png')
        self.no_trofei = pygame.image.load('data/trofei_nobosses.png')
        self.rot_trofei = pygame.image.load('data/rot_trofei.png')
        self.rat_trofei = pygame.image.load('data/rat_trofei.png')
        self.rot = None
        self.rat = None

    def update_b_info(self):
        with open('check_bosses.txt') as bosses:
            bosses = bosses.readlines()
            self.rat = int(bosses[1].split()[1])
            self.rot = int(bosses[0].split()[1])

    def draw_button(self, color, hover_color, x, y, width, height, text, callback=None):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]
        if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
            pygame.draw.rect(self.screen, hover_color, (x, y, width, height))
            if clicked and callback:
                play_sound(sound_data['button'], 0.5)
                callback()

        else:
            pygame.draw.rect(self.screen, color, (x, y, width, height))

        text_surface = self.font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x + width // 2, y + height // 2)
        self.screen.blit(text_surface, text_rect)

    def trofei(self):
        self.screen.blit(self.no_trofei, (300, 680))
        self.screen.blit(self.no_trofei, (1200, 680))
        if self.rat:
            self.screen.blit(self.rat_trofei, (1200, 680))
        if self.rot:
            self.screen.blit(self.rot_trofei, (300, 680))

    def level_1(self):
        self.game = Game(self.screen)
        self.game.start('level1')

    def level_2(self):
        self.game = Game(self.screen)
        self.game.start('level2')

    def return_to_menu(self):
        self.running = False
        return True

    def start(self):
        self.running = True
        while self.running:
            self.update_b_info()
            self.screen.blit(self.image, (0, 0))
            self.draw_button(self.BLACK, self.YELLOW, 20, 20, 50, 50, "<", self.return_to_menu)
            self.draw_button(self.BLACK, self.YELLOW, 230, 330, 540, 340, '', self.level_1)
            self.draw_button(self.BLACK, self.YELLOW, 1130, 330, 540, 340, '', self.level_2)
            self.screen.blit(self.mini1, (250, 350))
            self.screen.blit(self.mini2, (1150, 350))
            self.trofei()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.flip()


class Game:
    def __init__(self, screen):
        self.level = None
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.clock = pygame.time.Clock()
        self.dt = 1 / 144
        self.offset = self.height - self.height // 3
        self.moving = True
        self.start_boss = False
        self.font = pygame.font.Font(None, 50)
        # self.barrierSound = sound_data['barrier']
        # /// Параметры спрайтов
        self.cords = {
            0: self.height - self.offset // 3 * 2,
            1: self.height - self.offset // 3,
            2: self.height
        }
        self.all_sprites = pygame.sprite.Group()
        self.barriers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.currency = pygame.sprite.Group()
        self.bossGroup = pygame.sprite.Group()
        self.hero = Hero(cords=self.cords)
        self.poses = getRandPos()
        self.all_sprites.add(self.hero)
        self.object_width, self.object_height = self.hero.rect.width, self.hero.rect.height
        self.hero.rect.left = self.width // 4
        self.hero.rect.bottom = self.height - self.offset // 3
        self.frequencyBar = 3
        self.frequencyCur = 6
        self.frequencyEnm = 12
        self.lastTimeSpawnBar = time.time()
        self.lastTimeSpawnEnm = time.time() + 1.5
        self.lastTimeSpawnCur = time.time() + 4.5
        self.smallFreqCur = 2
        self.smallLTSCur = time.time()
        self.coin = pygame.image.load('data/coin.png')
        # ///
        self.all_sprites.draw(self.screen)
        self.enemy_limit = 6
        self.additional_power = 0
        self.additional_defense = 0

    def start(self, level):
        pygame.mixer.music.load(f'sounds/{cursor.execute(f"SELECT music FROM {level}").fetchone()[0]}')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
        self.running = True
        self.enemy_amount = 0
        self.level = level
        self.back = Background(level=self.level)
        while self.running:
            if self.enemy_amount == self.enemy_limit:
                self.boss()
                self.enemy_amount = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    self.running = False
                if not self.start_boss:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:
                            self.hero.curLine -= 1
                            if self.hero.curLine < 0:
                                self.hero.curLine = 0
                        if event.key == pygame.K_s:
                            self.hero.curLine += 1
                            if self.hero.curLine > 2:
                                self.hero.curLine = 2
                        if event.key == pygame.K_x:
                            self.boss()
            self.update()
            self.draw()
            self.collision()
            self.dt = self.clock.tick(300) / 1000

    def draw(self, update=True):
        self.screen.fill('black')
        self.back.draw(self.screen)
        if self.moving:
            self.drawing_lines()
            self.all_sprites.draw(self.screen)
            self.barriers.draw(self.screen)
            self.enemies.draw(self.screen)
            self.currency.draw(self.screen)
            self.draw_money(self.width - 100, 50)
        if self.start_boss:
            self.all_sprites.draw(self.screen)
            self.bossGroup.draw(self.screen)
        if update:
            pygame.display.flip()

    def update(self):
        if self.moving:
            self.back.update(self.dt)
            self.enemies.update(self.dt)
            self.barriers.update(self.dt)
            self.currency.update(self.dt)
            self.handleSpawnBar()
            self.handleSpawnEnm()
            self.handleSpawnCur()
        if self.start_boss:
            for bar in self.barriers:
                bar.kill()
            self.bossGroup.update(self.dt)
        self.hero.update(self.dt)

    def handleSpawnBar(self):
        if self.lastTimeSpawnBar is None:
            return
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
        if self.lastTimeSpawnEnm is None:
            return
        self.poses = getRandPos()
        if time.time() - self.lastTimeSpawnEnm >= self.frequencyEnm:
            self.lastTimeSpawnEnm = time.time()
            self.enemy_amount += 1
            self.enemies.add(
                Enemy(
                    cords=self.cords,
                    scr_width=self.width,
                    pos=self.poses[0],
                    level=self.level
                ))

    def handleSpawnCur(self):
        if self.lastTimeSpawnCur is None:
            return
        posX = self.width
        self.poses = getRandPos()
        if time.time() - self.lastTimeSpawnCur >= self.frequencyCur:
            for _ in range(3):
                self.currency.add(
                    Currency(
                        cords=self.cords,
                        pos_x=posX,
                        pos_y=self.poses[0]
                    ))
                posX += 90
            self.lastTimeSpawnCur = time.time()

    def handleSpawnBoss(self):
        self.bossGroup.add(
            Boss(
                pos=[self.width, self.height],
                level=self.level
            ))

    def drawing_lines(self):
        pygame.draw.line(self.screen, 'grey', (0, self.height),
                         (self.width, self.height), width=10)
        pygame.draw.line(self.screen, 'grey', (0, self.height - self.offset // 3),
                         (self.width, self.height - self.offset // 3), width=5)
        pygame.draw.line(self.screen, 'grey', (0, self.height - self.offset // 3 * 2),
                         (self.width, self.height - self.offset // 3 * 2), width=5)
        pygame.draw.line(self.screen, 'grey', (0, self.height / 3),
                         (self.width, self.height / 3), width=10)

    def fadeIn(self, width, height):
        fade = pygame.Surface((width, height))
        fade.fill((0, 0, 0))
        for alpha in range(0, 300):
            fade.set_alpha(alpha)
            self.draw(False)
            self.screen.blit(fade, (0, 0))
            pygame.display.flip()
            pygame.time.delay(1)

    def collision(self):
        if pygame.sprite.spritecollide(self.hero, self.barriers, False, pygame.sprite.collide_mask):
            pygame.mixer.music.stop()
            play_sound(sound_data['barrier'], 0.3)
            self.moving = False
            self.fadeIn(self.width, self.height)
            lose = Lose(self.screen, self.level)
            lose.start()
            self.running = False
        if pygame.sprite.spritecollide(self.hero, self.enemies, True, pygame.sprite.collide_mask):
            pygame.mixer.music.pause()
            play_sound(sound_data['enemy'], 0.3)
            delayBar = time.time() - self.lastTimeSpawnBar
            delayEnm = time.time() - self.lastTimeSpawnEnm
            delayCur = time.time() - self.lastTimeSpawnCur
            self.fight = Fight(self.screen, self.level, self.additional_power, self.additional_defense)
            self.fadeIn(self.width, self.height)
            self.fight.start()
            if not self.fight.result():
                self.running = False
                return
            pygame.mixer.music.unpause()
            self.lastTimeSpawnBar = time.time() - delayBar
            self.lastTimeSpawnEnm = time.time() - delayEnm
            self.lastTimeSpawnCur = time.time() - delayCur
            self.dt = self.clock.tick(300) / 1000
            self.additional_power, self.additional_defense = \
                (self.fight.add_stats(self.additional_power, self.additional_defense))
        if pygame.sprite.spritecollide(self.hero, self.currency, True, pygame.sprite.collide_mask):
            play_sound(sound_data['coin'], 0.3)
            money, power, defense = download_stats()
            money += 1
            upload_stats(money, power, defense)
        if pygame.sprite.spritecollide(self.hero, self.bossGroup, True, pygame.sprite.collide_rect):
            pygame.mixer.music.stop()
            play_sound(sound_data['boss'], 0.3)
            self.fight_boss = Fight(self.screen, self.level, self.additional_power, self.additional_defense, boss=True)
            self.fight_boss.start()
            self.running = self.fight_boss.result()

    def boss(self):
        self.handleSpawnBoss()
        self.moving = False
        self.start_boss = True
        pygame.draw.line(self.screen, 'grey', (0, self.height),
                         (self.width, self.height), width=15)
        self.hero.curLine = 2

    def draw_money(self, x, y):
        text = str(download_stats()[0])
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.topright = (x, y)
        self.screen.blit(text_surface, text_rect)
        self.screen.blit(self.coin, (self.width - 80, 25))


class Hero(pygame.sprite.Sprite):

    def __init__(self, *group, cords):
        super().__init__(*group)
        self.cords = cords
        self.frames = []
        for frameFile in Path('sprites/hero_frames').glob('*.png'):
            self.frames.append(pygame.image.load(frameFile).convert_alpha())
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.y = self.rect.bottom
        self.mask = pygame.mask.from_surface(self.image)
        self.curLine = 1
        self.frameTime = 0.15
        self.frameIndex = 0
        self.lastFrameTime = time.time()

    def update(self, dt):
        self.handleAnimation()
        self.handleMovement(dt)

    def handleAnimation(self):
        if time.time() - self.lastFrameTime >= self.frameTime:
            self.frameIndex += 1
            self.frameIndex %= len(self.frames)
            self.lastFrameTime = time.time()
            x = self.rect.centerx
            self.image = self.frames[self.frameIndex]
            self.rect = self.image.get_rect()
            self.rect.center = x, self.y

    def handleMovement(self, dt):
        if abs(self.y - self.cords[self.curLine]) < 3:
            pass
        elif self.y > self.cords[self.curLine]:
            self.y -= 400 * dt
        elif self.y < self.cords[self.curLine]:
            self.y += 400 * dt
        self.rect.bottom = round(self.y)


class Enemy(pygame.sprite.Sprite):

    def __init__(self, *group, cords, scr_width, pos, level):
        super().__init__(*group)
        self.level = level
        self.scrWidth = scr_width
        self.pos = pos
        self.cords = cords
        self.frames = []
        for frameFile in Path(
                f'sprites/{cursor.execute(f"SELECT enemy FROM {self.level}").fetchone()[0]}').glob("*.png"):
            self.frames.append(pygame.image.load(frameFile).convert_alpha())
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.curLine = 1
        self.frameTime = 0.15
        self.frameIndex = 0
        self.lastFrameTime = time.time()
        self.rect.left = self.scrWidth
        self.rect.bottom = self.cords[self.pos]
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


WHITE = (255, 255, 255)


class HeroF:
    def __init__(self, power, defense):
        self.atacked = False
        self.additional_power = power
        self.additional_defense = defense
        self.heal_potion = 3
        self.max_hp = 100
        self.hp = 100
        with open('money X stats') as stat:
            stat = stat.readlines()
            self.base_power = int(stat[1].split()[1])
            self.base_defense = int(stat[2].split()[1])
        self.frames = []
        for frameFile in Path('sprites/hero_in_fight').glob('*.png'):
            self.frames.append(pygame.image.load(frameFile).convert_alpha())
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.frameTime = 0.15
        self.frameIndex = 0
        self.lastFrameTime = time.time()
        self.ones = False
        self.en_turn = False

    def hp_bar(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (1000, 850, self.hp * 4, 30))

    def check_hp(self):
        if self.hp == 0:
            pass

    def draw_button(self, screen, color, hover_color, x, y, width, height, text, enemy, callback):
        if self.atacked:
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]
        if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
            pygame.draw.rect(screen, hover_color, (x, y, width, height))
            if clicked and callback:
                self.atacked = True
                callback(enemy)

        else:
            pygame.draw.rect(screen, color, (x, y, width, height))

        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x + width // 2, y + height // 2)
        screen.blit(text_surface, text_rect)

    def attack(self, enemy):
        self.en_turn = False
        if enemy.hp - (self.additional_power + self.base_power) > 0:
            enemy.hp -= (self.additional_power + self.base_power)
        else:
            enemy.hp = 0

    def heal(self, enemy):
        self.en_turn = True
        if self.hp + 10 > 100:
            self.hp = 100
        else:
            self.hp += 10
        self.heal_potion -= 1

    def change_animation_status(self, name, once=False):
        self.once = once
        self.frames = []
        for frameFile in Path(f'sprites/{name}').glob('*.png'):
            self.frames.append(pygame.image.load(frameFile).convert_alpha())
        self.image = self.frames[0]
        self.frameIndex = 0
        self.lastFrameTime = time.time()
        x, y = self.rect.center
        self.image = self.frames[self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def Animation(self):
        if time.time() - self.lastFrameTime >= self.frameTime:
            self.frameIndex += 1
            if self.frameIndex == len(self.frames) and self.once:
                self.change_animation_status('hero_in_fight')
                return
            self.frameIndex %= len(self.frames)
            self.lastFrameTime = time.time()
            x, y = self.rect.center
            self.image = self.frames[self.frameIndex]
            self.rect = self.image.get_rect()
            self.rect.center = x, y


class EnemyF:
    def __init__(self, level,  boss):
        self.level = level
        self.boss = boss
        if self.boss:
            self.hp = 250
            self.damage = 60
            self.max_hp = self.hp
        else:
            self.hp = randint(10, 100)
            self.max_hp = self.hp
            # self.damage = randint(10, 20)
            self.damage = 100
        self.frames = []
        for frameFile in Path(
                f'sprites/{cursor.execute(f"SELECT in_fight FROM {self.level}").fetchone()[0]}').glob('*.png'):
            self.frames.append(pygame.image.load(frameFile).convert_alpha())
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.frameTime = 0.15
        self.frameIndex = 0
        self.lastFrameTime = time.time()
        self.once = False

    def hp_bar(self, screen):
        if self.boss:
            pygame.draw.rect(screen, (255, 0, 0), (1160, 130, self.hp, 20))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (1160, 130, self.hp * 2, 20))

    def atack(self, hero):
        hero.hp -= max(1, self.damage - (hero.base_defense + hero.additional_defense))
        hero.hp = max(hero.hp, 0)

    def change_animation_status(self, name, once=False):
        self.once = once
        self.frames = []
        for frameFile in Path(f'sprites/{name}').glob('*.png'):
            self.frames.append(pygame.image.load(frameFile).convert_alpha())
        self.image = self.frames[0]
        self.frameIndex = 0
        self.lastFrameTime = time.time()
        x, y = self.rect.center
        self.image = self.frames[self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def Animation(self):
        if time.time() - self.lastFrameTime >= self.frameTime:
            self.frameIndex += 1
            if self.frameIndex == len(self.frames) and self.once:
                if self.boss:
                    self.change_animation_status(cursor.execute(f'SELECT b_in_fight FROM {self.level}').fetchone()[0])
                else:
                    self.change_animation_status(
                        cursor.execute(f'SELECT in_fight FROM {self.level}').fetchone()[0])
                return
            self.frameIndex %= len(self.frames)
            self.lastFrameTime = time.time()
            x, y = self.rect.center
            self.image = self.frames[self.frameIndex]
            self.rect = self.image.get_rect()
            self.rect.center = x, y


class Fight:
    def __init__(self, screen, level, power, defense, boss=None):
        self.level = level
        self.exit = False
        self.win = False
        self.hero_lost = False
        self.boss = boss
        self.stats_applied = False
        self.hero = HeroF(power, defense)
        self.enemy = EnemyF(self.level, self.boss)
        self.atacked_time_hero = None
        self.atacked_time_enemy = None
        self.enemy_attacked = False
        self.screen = screen
        self.additional_power = 0
        self.additional_defense = 0
        self.font = pygame.font.Font(None, 36)
        self.chek_stats = None
        self.hero.change_animation_status('hero_in_fight')
        if self.boss:
            self.enemy.change_animation_status(cursor.execute(f'SELECT b_in_fight FROM {self.level}').fetchone()[0])
        else:
            self.enemy.change_animation_status(cursor.execute(f'SELECT in_fight FROM {self.level}').fetchone()[0])

    def update(self):
        if self.hero_lost:
            return
        self.hero.Animation()
        self.enemy.Animation()
        if self.hero.atacked and not self.atacked_time_hero and not self.enemy_attacked:
            if not self.hero.en_turn:
                play_sound(sound_data['hero_strike'], 0.5)
                self.hero.change_animation_status('hero_strike', True)
            self.atacked_time_hero = time.time()
            self.enemy_attacked = True

        if self.atacked_time_hero:
            if time.time() - self.atacked_time_hero >= 2:
                if self.enemy.hp > 0:
                    play_sound(sound_data['enemy_strike'], 0.3)
                    if self.boss:
                        self.enemy.change_animation_status(cursor.execute(f'SELECT b_strike FROM {self.level}').fetchone()[0],
                                                       True)
                    else:
                        self.enemy.change_animation_status(
                            cursor.execute(f'SELECT strike FROM {self.level}').fetchone()[0],
                            True)
                    self.enemy.atack(self.hero)

                    if self.hero.hp <= 0:
                        self.lost()
                        self.hero_lost = True
                        return
                    self.atacked_time_hero = False
                    self.atacked_time_enemy = time.time()
                else:
                    self.win = True

        if self.atacked_time_enemy:
            if time.time() - self.atacked_time_enemy >= 2:
                self.hero.atacked = False
                self.atacked_time_enemy = None
                self.enemy_attacked = False

    def lost(self):
        self.result()
        self.exit = True

    def plus_stats(self):
        if self.chek_stats is None:
            self.chek_stats = time.time()
        if time.time() - self.chek_stats > 3:
            self.chek_stats = None
            self.exit = True
        if not self.stats_applied:
            self.additional_defense += randint(1, 5)
            self.additional_power += randint(1, 5)
            self.stats_applied = True
        text_surface = self.font.render(f'сила +{self.additional_power}  защита +{self.additional_defense}', True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (300, 850)
        self.screen.blit(text_surface, text_rect)

    def add_stats(self, power, defense):
        power += self.additional_power
        defense += self.additional_defense
        return power, defense

    def result(self):
        self.exit = True
        if self.boss:
            return False
        else:
            return self.win

    def end(self):
        if self.level == 'level1':
            if self.boss and self.win:
                rot, rat = read_boss_file()
                rot = 1
                write_boss_file(rot, rat)
                win = Victory(self.screen, self.level)
                win.start()
            elif self.boss and not self.win:
                lost = Lose(self.screen, self.level)
                lost.start()
            else:
                if not self.win:
                    lost = Lose(self.screen, self.level)
                    lost.start()
        elif self.level == 'level2':
            if self.boss and self.win:
                rot, rat = read_boss_file()
                rat = 1
                write_boss_file(rot, rat)
                win = Victory(self.screen, self.level)
                win.start()
            elif self.boss and not self.win:
                lost = Lose(self.screen, self.level)
                lost.start()
            else:
                if not self.win:
                    lost = Lose(self.screen, self.level)
                    lost.start()

    def draw(self):
        self.screen.blit(self.hero.image, (256, 200))
        self.screen.blit(self.enemy.image, (1150, 200))
        pygame.draw.rect(self.screen, (100, 100, 100), (256, 800, 1200, 150))
        pygame.draw.rect(self.screen, (100, 100, 100), (1140, 125, 230, 50) if not self.boss else (1140, 125, 290, 50))
        self.hero.hp_bar(self.screen)
        self.draw_text(f'{self.hero.hp} / {self.hero.max_hp}', 1000, 900)
        self.enemy.hp_bar(self.screen)
        self.draw_text(f'{self.enemy.hp} / {self.enemy.max_hp}', 1160, 150)
        self.hero.draw_button(self.screen, (150, 150, 150), (175, 175, 175), 300, 825, 200, 100, "Атака", self.enemy, self.hero.attack)
        self.hero.draw_button(self.screen, (150, 150, 150), (175, 175, 175) if self.hero.heal_potion > 0 else (255, 0, 0), 600, 825, 200, 100, "+Здоровье", self.enemy, self.hero.heal if self.hero.heal_potion > 0 else None)
        if self.win:
            self.plus_stats()

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def fadeIn(self, width, height):
        fade = pygame.Surface((width, height))
        fade.fill((0, 0, 0))
        for alpha in range(0, 300):
            fade.set_alpha(alpha)
            self.draw()
            self.screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(1)

    def fadeOut(self, width, height):
        fade = pygame.Surface((width, height))
        fade.fill((0, 0, 0))
        for alpha in range(300, 0, -1):
            fade.set_alpha(alpha)
            self.draw()
            self.screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(1)

    def start(self):
        self.fadeOut(self.screen.get_width(), self.screen.get_height())
        pygame.display.set_caption('Бой')
        self.running = True
        while self.running:
            self.screen.fill((25, 25, 25))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.update()
            self.draw()
            if self.exit:
                self.fadeIn(self.screen.get_width(), self.screen.get_height())
                self.running = False
            pygame.display.flip()
        self.end()


class Lose:
    def __init__(self, screen, level):
        self.shop = Shop(screen)
        self.screen = screen
        self.font = pygame.font.Font(None, 42)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.YELLOW = (235, 205, 3)
        self.image = pygame.image.load(f'data/{cursor.execute(f"SELECT lose FROM {level}").fetchone()[0]}')
        self.image_rect = self.image.get_rect()

    def draw_button(self, color, hover_color, x, y, width, height, text, callback=None):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]
        if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
            pygame.draw.rect(self.screen, hover_color, (x, y, width, height))
            if clicked and callback:
                play_sound(sound_data['button'], 0.5)
                callback()
        else:
            pygame.draw.rect(self.screen, color, (x, y, width, height))

        text_surface = self.font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x + width // 2, y + height // 2)
        self.screen.blit(text_surface, text_rect)

    def start(self):
        play_sound(sound_data['lose'], 0.3)
        self.running = True
        while self.running:
            self.screen.blit(self.image, (0, 0))
            self.draw_button(self.BLACK, self.YELLOW, 755, 600, 450, 200, "К уровням", self.exit)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.flip()

    def exit(self):
        self.running = False


class Victory:
    def __init__(self, screen, level):
        self.shop = Shop(screen)
        self.screen = screen
        self.font = pygame.font.Font(None, 42)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.YELLOW = (235, 205, 3)
        self.image = pygame.image.load(f'data/{cursor.execute(f"SELECT victory FROM {level}").fetchone()[0]}')
        self.image_rect = self.image.get_rect()

    def draw_button(self, color, hover_color, x, y, width, height, text, callback=None):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]
        if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
            pygame.draw.rect(self.screen, hover_color, (x, y, width, height))
            if clicked and callback:
                play_sound(sound_data['button'], 0.5)
                callback()
        else:
            pygame.draw.rect(self.screen, color, (x, y, width, height))

        text_surface = self.font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x + width // 2, y + height // 2)
        self.screen.blit(text_surface, text_rect)

    def start(self):
        play_sound(sound_data['victory'], 0.3)
        self.running = True
        while self.running:
            self.screen.blit(self.image, (0, 0))
            self.draw_button(self.BLACK, self.YELLOW, 755, 600, 450, 200, "К уровням", self.exit)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.flip()

    def exit(self):
        self.running = False


class Shop:
    def __init__(self, screen):
        pygame.init()
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 125)
        self.LIGHT_BLUE = (135, 206, 250)
        self.WIDTH, self.HEIGHT = 1920, 1080
        self.screen = screen
        pygame.display.set_caption('Магазин')
        self.font = pygame.font.Font(None, 36)
        self.weapon = pygame.image.load('data/Sprite.png')
        self.mask = pygame.image.load('data/mask.png')
        self.background = pygame.image.load('data/shopy.png')
        self.read_statistics()

    def draw_button(self, color, hover_color, x, y, width, height, text, clicked, callback=None):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
            pygame.draw.rect(self.screen, hover_color, (x, y, width, height))
            if clicked and callback:
                play_sound(sound_data['button'], 0.3)
                callback()

        else:
            pygame.draw.rect(self.screen, color, (x, y, width, height))

        text_surface = self.font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x + width // 2, y + height // 2)
        self.screen.blit(text_surface, text_rect)

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)


    def buy_power(self):
        with open('money X stats', 'w') as file:
            file.write(f'money: {self.money - 10}\npower: {self.power + 10}\ndefense: {self.defense}')
        self.read_statistics()

    def buy_defense(self):
        with open('money X stats', 'w') as file:
            file.write(f'money: {self.money - 10}\npower: {self.power}\ndefense: {self.defense + 10}')
        self.read_statistics()

    def read_statistics(self):
        self.money, self.power, self.defense = download_stats()

    def return_to_menu(self):
        self.running = False

    def draw(self):
        money, power, defense = download_stats()
        self.draw_text(f'деньги: {money} сила: {power} защита: {defense}', 200, 900)

        power_button_x, power_button_y = 220, 700
        shield_button_x, shield_button_y = 1220, 700
        button_width, button_height = 400, 100
        rich = self.money - 10 >= 0

        self.draw_text('урон', 380, 630)
        self.draw_text('защита', 1380, 630)
        self.draw_button(self.BLUE, self.LIGHT_BLUE if rich else (255, 0, 0), power_button_x, power_button_y, button_width, button_height, "10",
                         self.clicked, self.buy_power if rich else None)
        self.draw_button(self.BLUE, self.LIGHT_BLUE if rich else (255, 0, 0), shield_button_x, shield_button_y, button_width, button_height,
                         "10", self.clicked, self.buy_defense if rich else None)
        self.screen.blit(self.weapon, (200, 200))
        self.screen.blit(self.mask, (1220, 270))

        self.draw_button(self.BLUE, self.LIGHT_BLUE, 20, 20, 50, 50, "<", self.clicked, self.return_to_menu)

    def start(self):
        self.running = True
        while self.running:
            self.screen.blit(self.background, (0, 0))
            self.clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicked = True

            self.draw()

            pygame.display.flip()


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
        self.x = self.rect.left

    def update(self, dt):
        self.handleMovement(dt)

    def handleMovement(self, dt):
        if self.rect.right == 0:
            self.kill()
        self.x -= 400 * dt
        self.rect.left = round(self.x)


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
        self.x -= 400 * dt
        self.rect.left = round(self.x)


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
        self.x1 -= 200 * dt
        self.x2 -= 200 * dt
        if self.rect1.right <= 0:
            self.rect1.left = self.rect2.right - 2
            self.x1 = self.rect1.left
        if self.rect2.right <= 0:
            self.rect2.left = self.rect1.right - 2
            self.x2 = self.rect2.left
        self.rect1.left = round(self.x1)
        self.rect2.left = round(self.x2)


class Menu:
    def __init__(self, screen):
        self.music = True
        self.shop = Shop(screen)
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.YELLOW = (235, 205, 3)
        self.image = pygame.image.load('data/menu_background.png')
        self.image_rect = self.image.get_rect()

    def draw_button(self, color, hover_color, x, y, width, height, text, callback=None):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]
        if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
            pygame.draw.rect(self.screen, hover_color, (x, y, width, height))
            if clicked and callback:
                play_sound(sound_data['button'], 0.5)
                callback()
        else:
            pygame.draw.rect(self.screen, color, (x, y, width, height))

        text_surface = self.font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x + width // 2, y + height // 2)
        self.screen.blit(text_surface, text_rect)

    def start(self):
        self.running = True
        while self.running:
            self.screen.blit(self.image, (0, 0))
            self.draw_button(self.BLACK, self.YELLOW, 793, 422, 328, 114, "Играть", self.start_game)
            self.draw_button(self.BLACK, self.YELLOW, 793, 615, 328, 114, "Магазин", self.open_shop)
            self.draw_button(self.BLACK, self.YELLOW, 793, 808, 328, 114, "Выход", self.exit)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.flip()

    def exit(self):
        self.running = False

    def start_game(self):
        self.levels = Levels(self.screen)
        self.levels.start()

    def open_shop(self):
        self.shop.start()


menu = Menu(screen)
menu.start()
