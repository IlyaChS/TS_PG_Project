import pygame
import game


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
        self.game = game.Game(self.screen)
        self.game.start('level1')

    def level_2(self):
        self.game = game.Game(self.screen)
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


if __name__ == '__main__':
    levels = Levels(pygame.display.set_mode((1920, 1080)))
    levels.start()
