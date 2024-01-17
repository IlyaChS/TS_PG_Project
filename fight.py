import pygame
from random import randint
import time
from pathlib import Path
from funcs import cursor, read_boss_file, write_boss_file


WHITE = (255, 255, 255)


class Hero:
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
        for frameFile in Path(f'./sprites/{name}').glob('*.png'):
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


class Enemy:
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
            self.damage = randint(10, 20)
        self.frames = []
        for frameFile in Path(f'./sprites/{cursor.execute(f"SELECT in_fight FROM {self.level}").fetchone()[0]}').glob('*.png'):
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

    def change_animation_status(self, name, once=False):
        self.once = once
        self.frames = []
        for frameFile in Path(f'./sprites/{name}').glob('*.png'):
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
        self.win = False
        self.boss = boss
        self.stats_applied = False
        self.hero = Hero(power, defense)
        self.enemy = Enemy(self.level, self.boss)
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
        self.hero.Animation()
        self.enemy.Animation()
        if self.hero.atacked and not self.atacked_time_hero and not self.enemy_attacked:
            if not self.hero.en_turn:
                self.hero.change_animation_status('hero_strike', True)
            self.atacked_time_hero = time.time()
            self.enemy_attacked = True

        if self.atacked_time_hero:
            if time.time() - self.atacked_time_hero >= 2:
                if self.enemy.hp > 0:
                    if self.boss:
                        self.enemy.change_animation_status(cursor.execute(f'SELECT b_strike FROM {self.level}').fetchone()[0],
                                                       True)
                    else:
                        self.enemy.change_animation_status(
                            cursor.execute(f'SELECT strike FROM {self.level}').fetchone()[0],
                            True)
                    self.enemy.atack(self.hero)
                    self.atacked_time_hero = False
                    self.atacked_time_enemy = time.time()
                else:
                    self.win = True

        if self.atacked_time_enemy:
            if time.time() - self.atacked_time_enemy >= 2:
                self.hero.atacked = False
                self.atacked_time_enemy = None
                self.enemy_attacked = False

    def plus_stats(self):
        if self.chek_stats is None:
            self.chek_stats = time.time()
        if time.time() - self.chek_stats > 3:
            self.chek_stats = None
            self.result()
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
        self.running = False
        if self.boss and self.win:
            if self.level == 'level1':
                rot, rat = read_boss_file()
                rot = 1
                write_boss_file(rot, rat)
            elif self.level == 'level2':
                rot, rat = read_boss_file()
                rat = 1
                write_boss_file(rot, rat)
            return False
        elif self.boss and not self.win:
            return False
        else:
            return self.win

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

    def start(self):
        pygame.display.set_caption('Бой')
        self.running = True
        while self.running:
            self.screen.fill((25, 25, 25))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.update()
            self.draw()

            pygame.display.flip()


if __name__ == '__main__':
    fight = Fight(pygame.display.set_mode((1920, 1080)), 'level2', 0, 0, True)
    fight.start()












