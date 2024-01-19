import pygame
import shop
import choose_level
from funcs import sound_data, play_sound


class Menu:
    def __init__(self, screen):
        self.music = True
        self.shop = shop.Shop(screen)
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
        self.levels = choose_level.Levels(self.screen)
        self.levels.start()

    def open_shop(self):
        self.shop.start()


pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
pygame.display.set_caption('Меню')

menu = Menu(screen)
menu.start()