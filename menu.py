import pygame

pygame.init()


WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT_BLUE = (135, 206, 250)

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Меню')


# Функция для отрисовки кнопки
def draw_button(color, hover_color, x, y, width, height, text):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()[0]
    if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if clicked:
            print("Кнопка была нажата!")
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (x + width // 2, y + height // 2)
    screen.blit(text_surface, text_rect)


image = pygame.image.load('Trash city.png')
image_rect = image.get_rect()

running = True
while running:
    screen.fill((106, 190, 48))

    # Создание кнопки
    start_button_x, start_button_y = 860, 440
    shop_button_x, shop_button_y = 860, 590
    button_width, button_height = 200, 100
    draw_button(GREEN, LIGHT_BLUE, start_button_x, start_button_y, button_width, button_height, "Играть")
    draw_button(GREEN, LIGHT_BLUE, shop_button_x, shop_button_y, button_width, button_height, "Магазин")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(image, (760, 200))

    pygame.display.flip()

pygame.quit()
