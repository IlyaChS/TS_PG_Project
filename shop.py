import pygame

pygame.init()


WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT_BLUE = (135, 206, 250)

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Магазин')
font = pygame.font.Font(None, 36)



def draw_button(color, hover_color, x, y, width, height, text, clicked):
    with open('money X stats') as statistic:
        statistic = statistic.readlines()
        money = int(statistic[0].split()[1])
        power = int(statistic[1].split()[1])
        defens = int(statistic[2].split()[1])
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
        if money - 10 >= 0:
            pygame.draw.rect(screen, hover_color, (x, y, width, height))

            if clicked:
                #if x == 200:
                if x == 480:
                    with open('money X stats', 'w') as file:
                        file.write(f'money: {money - 10}\npower: {power + 10}\ndefens: {defens}')
                elif x == 1020:
                    with open('money X stats', 'w') as file:
                        file.write(f'money: {money - 10}\npower: {power}\ndefens: {defens + 10}')
        else:
            pygame.draw.rect(screen, (255, 0, 0), (x, y, width, height))

    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (x + width // 2, y + height // 2)
    screen.blit(text_surface, text_rect)


def draw_text(text, x, y):
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


weapon = pygame.image.load('Sprite.png')
mask = pygame.image.load('mask.png')

running = True
while running:
    screen.fill((106, 190, 48))
    clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked = True

    with open('money X stats') as statistic:
        statistic = statistic.readlines()
        money = int(statistic[0].split()[1])
        power = int(statistic[1].split()[1])
        defens = int(statistic[2].split()[1])

    draw_text(f'деньги: {money} сила: {power} защита: {defens}', 200, 900)

    pygame.draw.rect(screen, (70, 255, 70), (460, 150, 440, 700))
    pygame.draw.rect(screen, (70, 255, 70), (1000, 150, 440, 700))

    power_button_x, power_button_y = 480, 700
    shield_button_x, shield_button_y = 1020, 700
    button_width, button_height = 400, 100

    draw_text('урон', 650, 150)
    draw_text('защита', 1180, 150)
    draw_button(GREEN, LIGHT_BLUE, power_button_x, power_button_y, button_width, button_height, "10", clicked)
    draw_button(GREEN, LIGHT_BLUE, shield_button_x, shield_button_y, button_width, button_height, "10", clicked)
    screen.blit(weapon, (480, 200))
    screen.blit(mask, (1020, 200))

    draw_button(GREEN, LIGHT_BLUE, 200, 115, 70, 70, "<", clicked)

    pygame.display.flip()

pygame.quit()
