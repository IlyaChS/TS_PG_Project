import time
import fight
import pygame
from funcs import getRandPos, sound_data, download_stats, upload_stats, play_sound, cursor
from hero import Hero
from back_ground import Background
from barrier import Barrier
from enemy import Enemy
from currency import Currency
from boss import Boss
from lose import Lose

pygame.init()


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
            self.fight = fight.Fight(self.screen, self.level, self.additional_power, self.additional_defense)
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
            self.fight_boss = fight.Fight(self.screen, self.level, self.additional_power, self.additional_defense, boss=True)
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


if __name__ == '__main__':
    game = Game(pygame.display.set_mode((1920, 1080)))
    game.start('level2')