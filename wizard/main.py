import pygame
import random
import pygame as pg

run = True
window_x = 600
window_y = 700
window = pygame.display.set_mode((window_x, window_y))
background_level1 = pg.image.load("background.png")
diamond1_picture = pg.image.load("8.png")
diamond2_picture = pg.image.load("9.png")
diamond3_picture = pg.image.load("11.png")
hero_direction = 'STOP'
count_before_dimond = 0

def draw_level1(window, picture):
    window.blit(picture, (0, 0))

class wizard:
    x = 10
    y = 500
    width = 138
    height = 150
    speed = 4
    main_picture = pg.image.load("1_IDLE_000.png")
    left_picture = pg.image.load("3_RUN_000_l.png")
    right_picture = pg.image.load("3_RUN_000.png")
    def stand(self, window):
        window.blit(self.main_picture, (self.x, self.y))

    def move_left(self, window):
        if self.x - self.speed >= 0:
            self.x -= self.speed
        else:
            self.x = 0
        window.blit(self.left_picture, (self.x, self.y))

    def move_right(self, window, width):
        if self.x + self.speed <= width - self.width:
            self.x += self.speed
        else:
            self.x = width - self.width
        self.x += self.speed
        window.blit(self.right_picture, (self.x, self.y))

class diamond():
    x = 0
    y = 0
    speed = 0
    picture = 0

    def __init__(self, picture):
        self.x = random.randint(0, 553)
        self.speed = random.randint(1, 4)
        self.picture = picture

    def show(self, window):
        window.blit(self.picture, (self.x, self.y))

    def fall(self):
        self.y += self.speed

class diamonds:
    diamonds_pictures = [pg.image.load("11.png"), pg.image.load("8.png"), pg.image.load("9.png")]
    diamonds_list = []

    def __init__(self):
        pass

    def add(self):
        self.diamonds_list.append(diamond(self.diamonds_pictures[random.randint(0,2)]))

    def draw(self, window):
        for element in self.diamonds_list:
            element.show(window)

    def fall(self):
        for element in self.diamonds_list:
            element.fall()

    def delete(self, x, y, width):
        pass


hero = wizard()
diamonds_IN_game = diamonds()
diamonds_IN_game.add()

while run:
    if count_before_dimond == 200:
        diamonds_IN_game.add()
        count_before_dimond = 0
    draw_level1(window, background_level1)
    diamonds_IN_game.draw(window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            hero_direction = 'LEFT'
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            hero_direction = 'RIGHT'
        elif event.type == pygame.KEYUP:
            hero_direction = 'STOP'
    if hero_direction == 'LEFT':
        hero.move_left(window)
    elif hero_direction == 'RIGHT':
        hero.move_right(window, window_x)
    else:
        hero.stand(window)
    pg.display.update()
    count_before_dimond += 1
    diamonds_IN_game.fall()
