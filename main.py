import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('2D Platformer')

original_background = pygame.image.load('background.png').convert()
background = pygame.transform.scale(original_background, (800, 600))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 500
        self.change_x = 0
        self.change_y = 0
        self.jump_count = 10

    def update(self):
        self.calc_grav()
        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            self.change_y = 0

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    def go_left(self):
        self.change_x = -6

    def go_right(self):
        self.change_x = 6

    def stop(self):
        self.change_x = 0


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Collectible(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.spawn_time = pygame.time.get_ticks()
        self.reposition()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > 5000:
            self.reposition()

    def reposition(self):
        self.rect.y = random.choice([180, 280, 380, 480])
        if self.rect.y == 180 or self.rect.y == 380:
            self.rect.x = random.randint(400, 580)
        if self.rect.y == 280 or self.rect.y == 480:
            self.rect.x = random.randint(100, 280)
        self.spawn_time = pygame.time.get_ticks()

    def check_collected(self, player):
        if self.rect.colliderect(player.rect):
            self.reposition()
            return True
        return False


class Collectibles:
    def __init__(self):
        self.collectibles_list = pygame.sprite.Group()
        for _ in range(4):
            self.add()

    def add(self):
        collectible = Collectible()
        self.collectibles_list.add(collectible)

    def update(self, player):
        for collectible in self.collectibles_list:
            collectible.update()
            if collectible.check_collected(player):
                collectible.reposition()
                return True
        return False

    def draw(self, window):
        self.collectibles_list.draw(window)


player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

platforms = pygame.sprite.Group()
platform_list = [
    Platform(200, 20, 100, 500),
    Platform(200, 20, 400, 400),
    Platform(200, 20, 100, 300),
    Platform(200, 20, 400, 200),
]

for platform in platform_list:
    platforms.add(platform)
    all_sprites.add(platform)

collectibles = Collectibles()

running = True
clock = pygame.time.Clock()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.go_left()
            elif event.key == pygame.K_RIGHT:
                player.go_right()
            elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                player.jump()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.stop()

    all_sprites.update()
    collectibles.update(player)

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    collectibles.draw(screen)

    pygame.display.update()

    clock.tick(60)

pygame.quit()
