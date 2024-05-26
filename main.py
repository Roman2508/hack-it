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
pygame.font.init()
font = pygame.font.SysFont('Arial', 26)
white = (255, 255, 255)
viole_dark = (47, 14, 51)
text_x = 10
text_y = 10

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

    def wizard_position(self):
        return (self.x, self.y)
    def size(self):
        return (self.width, self.height)
class super_wizard(wizard):
    width = 150
    height = 175
    main_picture = pg.image.load("1_IDLE_000_i.png")
    left_picture = pg.image.load("3_RUN_000_il.png")
    right_picture = pg.image.load("3_RUN_000_i.png")
    jump_picture = pg.image.load("4_JUMP_003.png")

    def jump(self, window):
        window.blit(self.jump_picture, (self.x, self.y-70))


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
    def diamond_position(self):
        return (self.x, self.y)

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

    def delete(self, x, y, width, height):
        count = 0
        lost = 0
        cach = 0
        for element in self.diamonds_list:
            position = element.diamond_position()
            d_x = position[0]
            d_y = position[1]+47
            if d_x > x and d_x < x + width and d_y > y and d_y < y + height:
                del self.diamonds_list[count]
                cach += 1
            elif position[1] > 700:
                del self.diamonds_list[count]
                lost += 1
        count += 1
        return (cach, lost)


hero = wizard()
super_hero = super_wizard()
diamonds_IN_game = diamonds()
diamonds_IN_game.add()
catch = 0
lost = 0
run_level = True

while run:
    while run_level:
        if count_before_dimond == 200:
            diamonds_IN_game.add()
            count_before_dimond = 0
        draw_level1(window, background_level1)
        massage = "Score: " + str(catch) + " / " + str(lost)
        text = font.render(massage, True, white, viole_dark)
        window.blit(text, (text_x, text_y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                run_level = False
                break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                hero_direction = 'LEFT'
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                hero_direction = 'RIGHT'
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                hero_direction = 'UP'
            elif event.type == pygame.KEYUP:
                hero_direction = 'STOP'
        if hero_direction == 'LEFT':
            super_hero.move_left(window)
        elif hero_direction == 'RIGHT':
            super_hero.move_right(window, window_x)
        elif hero_direction == 'UP':
            super_hero.jump(window)
        else:
            super_hero.stand(window)
        diamonds_IN_game.draw(window)
        pg.display.update()
        count_before_dimond += 1
        wizard_position = super_hero.wizard_position()
        wizard_size = super_hero.size()
        result = diamonds_IN_game.delete(wizard_position[0], wizard_position[1], wizard_size[0], wizard_size[1])
        catch += result[0]
        lost += result[1]
        diamonds_IN_game.fall()
        if lost == 6:
            run_level = False
    window.blit(background_level1, (0, 0))
    font = pygame.font.SysFont('Arial', 46)
    massage = "Game over! Your Score: " + str(catch)
    text = font.render(massage, True, white, viole_dark)
    window.blit(text, (text_x, text_y))
    pg.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
