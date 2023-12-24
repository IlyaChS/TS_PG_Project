import pygame
from hero import Hero
from back_ground import Background


class Game:
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h - 20
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Musorniy gorod')
        self.offset = self.height - self.height // 3
        running = True
        # /// Параметры спрайтов
        self.all_sprites = pygame.sprite.Group()
        self.font_sprites = pygame.sprite.Group()
        self.back = Background()
        self.hero = Hero()
        self.all_sprites.add(self.hero)
        self.font_sprites.add(self.back)
        self.object_width, self.object_height = self.hero.rect.width, self.hero.rect.height
        self.hero.rect.left = self.width // 2 - self.object_width // 2
        self.hero.rect.bottom = self.height - self.offset // 3
        self.position = [1, self.hero.rect.left, self.hero.rect.bottom]
        # ///
        self.font_sprites.draw(self.screen)
        self.all_sprites.draw(self.screen)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.go_up()
                        print(self.position)
                    if event.key == pygame.K_s:
                        self.go_down()
                        print(self.position)
            self.background()
            self.font_sprites.draw(self.screen)
            self.drawing_lines()
            self.all_sprites.draw(self.screen)
            pygame.display.flip()

    def go_up(self):
        cur_line = self.position[0]
        if cur_line == 1:
            while self.hero.rect.bottom > self.height - self.offset // 3 * 2:
                self.background()
                self.font_sprites.draw(self.screen)
                self.drawing_lines()
                self.all_sprites.draw(self.screen)
                self.hero.rect.bottom -= 1
                pygame.display.flip()
            self.position = [cur_line - 1, self.hero.rect.left, self.hero.rect.bottom]
        if cur_line == 2:
            while self.hero.rect.bottom > self.height - self.offset // 3:
                self.background()
                self.font_sprites.draw(self.screen)
                self.drawing_lines()
                self.all_sprites.draw(self.screen)
                self.hero.rect.bottom -= 1
                pygame.display.flip()
            self.position = [cur_line - 1, self.hero.rect.left, self.hero.rect.bottom]
        else:
            pass

    def go_down(self):
        cur_line = self.position[0]
        if cur_line == 0:
            while self.hero.rect.bottom < self.height - self.offset // 3:
                self.background()
                self.font_sprites.draw(self.screen)
                self.drawing_lines()
                self.all_sprites.draw(self.screen)
                self.hero.rect.bottom += 1
                pygame.display.flip()
            self.position = [cur_line + 1, self.hero.rect.left, self.hero.rect.bottom]
        if cur_line == 1:
            while self.hero.rect.bottom < self.height:
                self.background()
                self.font_sprites.draw(self.screen)
                self.drawing_lines()
                self.all_sprites.draw(self.screen)
                self.hero.rect.bottom += 1
                pygame.display.flip()
            self.position = [cur_line + 1, self.hero.rect.left, self.hero.rect.bottom]
        else:
            pass

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


if __name__ == '__main__':
    Game()
