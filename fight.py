import pygame
from random import randint
import time


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

    def hp_bar(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (1000, 850, self.hp * 4, 30))

    def draw_button(self, screen, color, hover_color, x, y, width, height, text, enemy):
        if self.atacked:
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]
        if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
            pygame.draw.rect(screen, hover_color, (x, y, width, height))
            if clicked:
                self.atacked = True
                if x == 300:
                    if enemy.hp - (self.additional_power + self.base_power) > 0:
                        enemy.hp -= (self.additional_power + self.base_power)
                    else:
                        enemy.hp = 0
                if x == 600 and self.heal_potion > 0:
                    self.hp += 10
                    self.heal_potion -= 1

        else:
            pygame.draw.rect(screen, color, (x, y, width, height))

        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x + width // 2, y + height // 2)
        screen.blit(text_surface, text_rect)


class Enemy:
    def __init__(self):
        self.hp = randint(10, 100)
        self.max_hp = self.hp
        self.damage = randint(10, 20)

    def hp_bar(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (1160, 130, self.hp * 2, 20))

    def atack(self, hero):
        hero.hp -= max(1, self.damage - (hero.base_defense + hero.additional_defense))


class Fight:
    def __init__(self, screen, power, defense):
        self.win = False
        self.stats_applied = False
        self.hero = Hero(power, defense)
        self.atacked_time_hero = None
        self.atacked_time_enemy = None
        self.enemy_attacked = False
        self.screen = screen
        self.additional_power = 0
        self.additional_defense = 0
        self.font = pygame.font.Font(None, 36)
        self.hero_image = pygame.image.load('fight_imgs/mainch_faight.png')
        self.chek_stats = None

    def update(self):
        if self.hero.atacked and not self.atacked_time_hero and not self.enemy_attacked:
            self.atacked_time_hero = time.time()
            self.enemy_attacked = True

        if self.atacked_time_hero:
            if time.time() - self.atacked_time_hero >= 2:
                if self.enemy.hp > 0:
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
            self.back_to_game()
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

    def back_to_game(self):
        self.running = False
        return True

    def draw(self):
        pygame.draw.rect(self.screen, (100, 100, 100), (256, 800, 1200, 150))
        pygame.draw.rect(self.screen, (100, 100, 100), (1140, 125, 230, 50))
        self.hero.hp_bar(self.screen)
        self.draw_text(f'{self.hero.hp} / {self.hero.max_hp}', 1000, 900)
        self.enemy.hp_bar(self.screen)
        self.draw_text(f'{self.enemy.hp} / {self.enemy.max_hp}', 1160, 150)
        self.hero.draw_button(self.screen, (150, 150, 150), (175, 175, 175), 300, 825, 200, 100, "Атака", self.enemy)
        self.hero.draw_button(self.screen, (150, 150, 150), (175, 175, 175), 600, 825, 200, 100, "+Здоровье", self.enemy)
        self.screen.blit(self.hero_image, (200, 300))
        self.screen.blit(self.enemy_image, (1150, 200))
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
        self.enemy = Enemy()
        self.enemy_image = pygame.image.load('fight_imgs/enemy2.png')
        while self.running:
            self.screen.fill((25, 25, 25))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update()
            self.draw()

            pygame.display.flip()


if __name__ == '__main__':
    Fight()











