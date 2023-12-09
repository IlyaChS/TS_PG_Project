import pygame


class Game:
    def __init__(self):
        pygame.init()
        self.size = width, height = 400, 300
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Musorniy gorod')
        running = True
        self.object_width, self.object_height = 20, 20
        self.position = [1, 200, 150]
        self.screen.fill((0, 0, 0))
        pygame.draw.circle(self.screen, (255, 0, 0), (200, 150), self.object_height)
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
            pygame.display.flip()

    def go_up(self):
        speed = 100
        clock = pygame.time.Clock()
        cur_line, x_pos, y_pos = self.position
        if cur_line == 1:
            while y_pos > self.object_height:
                self.screen.fill((0, 0, 0))
                pygame.draw.circle(self.screen, (255, 0, 0), (200, y_pos), self.object_height)
                y_pos -= speed * clock.tick() / 1000
                pygame.display.flip()
            self.position = [cur_line - 1, x_pos, y_pos]
        if cur_line == 2:
            while y_pos > self.size[-1] // 2:
                self.screen.fill((0, 0, 0))
                pygame.draw.circle(self.screen, (255, 0, 0), (200, y_pos), self.object_height)
                y_pos -= speed * clock.tick() / 1000
                pygame.display.flip()
            self.position = [cur_line - 1, x_pos, y_pos]
        else:
            pass

    def go_down(self):
        speed = 100
        clock = pygame.time.Clock()
        cur_line, x_pos, y_pos = self.position
        if cur_line == 0:
            while y_pos < self.size[-1] // 2:
                self.screen.fill((0, 0, 0))
                pygame.draw.circle(self.screen, (255, 0, 0), (200, y_pos), self.object_height)
                y_pos += speed * clock.tick() / 1000
                pygame.display.flip()
            self.position = [cur_line + 1, x_pos, y_pos]
        if cur_line == 1:
            while y_pos < self.size[-1] - self.object_height:
                self.screen.fill((0, 0, 0))
                pygame.draw.circle(self.screen, (255, 0, 0), (200, y_pos), self.object_height)
                y_pos += speed * clock.tick() / 1000
                pygame.display.flip()
            self.position = [cur_line + 1, x_pos, y_pos]
        else:
            pass


if __name__ == '__main__':
    Game()
