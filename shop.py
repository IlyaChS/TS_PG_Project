import pygame


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
        with open('money X stats') as statistic:
            statistic = statistic.readlines()
            self.money = int(statistic[0].split()[1])
            self.power = int(statistic[1].split()[1])
            self.defense = int(statistic[2].split()[1])

    def return_to_menu(self):
        self.running = False

    def draw(self):
        self.draw_text(f'деньги: {self.money} сила: {self.power} защита: {self.defense}', 200, 900)

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


if __name__ == '__main__':
    shop = Shop(pygame.display.set_mode((1920, 1080)))
    shop.start()
