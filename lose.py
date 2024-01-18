import pygame
import shop
from funcs import cursor, play_sound, sound_data


class Lose:
    def __init__(self, screen, level):
        self.shop = shop.Shop(screen)
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


if __name__ == '__main__':
    win = Lose(pygame.display.set_mode((1920, 1080)), 'level1')
    win.start()
