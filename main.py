import pygame
import os
import sys
import time

pygame.init()

FPS = 60
TILE_SIZE = 64
WIDTH = 1344
HEIGHT = 11 * TILE_SIZE
MAX_LVL = 2
BLACK = pygame.Color('black')
DARK_GREY = (40, 40, 40)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mountains")
lvl = 1
clock = pygame.time.Clock()

heroes_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
spikes_group = pygame.sprite.Group()
flag_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


def load_image(name, directory=None, colorkey=None):
    if directory is not None:
        fullname = os.path.join(f'Data/{directory}', name)
    else:
        fullname = os.path.join('Data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):  # загрузка карты
    filename = "Levels/" + filename
    with open(filename, 'r', encoding="UTF-8") as lvlFile:
        level_map = [line.strip() for line in lvlFile]
    return level_map


def create_level(level):  # создание уровня
    global player
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == "&":
                player = Hero(x, y)
            elif level[y][x] == "t":
                Spike(x, y)
            elif level[y][x] == "f":
                Flag(x, y)
            elif level[y][x] != ".":
                Tile(level[y][x], x, y)


def level_up():  # новый уровень
    global lvl
    lvl += 1
    for sprite in all_sprites:
        sprite.kill()
    create_level(load_level(f"lvl{lvl}.txt"))
    return


def start_screen():  # начальный экран
    # начальная музыка
    # ...
    fon = pygame.transform.scale(load_image('startscreen.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    press_font = pygame.font.Font(None, 25)
    main_font = pygame.font.Font(None, 100)
    press_txt = press_font.render('press any button', True, (40, 40, 40))
    screen.blit(press_txt, (WIDTH // 2 - press_txt.get_width() // 2, 170))
    main_txt = main_font.render('Mountains', True, (0, 0, 0))
    screen.blit(main_txt, (WIDTH // 2 - main_txt.get_width() // 2, 100))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                # игровая музыка
                # ...
                return
        clock.tick(FPS)
        pygame.display.flip()


def lvl_completed():  # уровень пройден
    # музыка победы
    all_sprites.draw(screen)
    completed = pygame.font.Font(None, 100)
    c_text = completed.render(f'Level {lvl} completed', True, (0, 0, 0))
    screen.blit(c_text, (WIDTH // 2 - c_text.get_width() // 2, HEIGHT // 2 - c_text.get_height() // 2))
    pressed = pygame.font.Font(None, 25)
    p_text = pressed.render('press any button', True, (0, 0, 0))
    screen.blit(p_text, (WIDTH // 2 - p_text.get_width() // 2, 410))
    times = pygame.font.Font(None, 40)
    t_text = times.render(f"Your time: {minutes}.{seconds}", True, (0, 0, 0))
    screen.blit(t_text, (WIDTH // 2 - t_text.get_width() // 2, 500))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if lvl == MAX_LVL:
                    finish_screen()
                global time_start
                time_start = time.time()
                return
        clock.tick(FPS)
        pygame.display.flip()


def game_over():  # смерть игрока
    # звучит музыка поражения
    # ...
    fon = pygame.transform.scale(load_image('startscreen.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    press_font = pygame.font.Font(None, 50)
    lost = pygame.font.Font(None, 100)
    main_txt = lost.render('You lost', True, BLACK)
    replay = press_font.render('Press 1 if you want to restart this level', True, DARK_GREY)
    to_menu = press_font.render('Press 2 if you want to go to menu', True, DARK_GREY)
    screen.blit(main_txt, (WIDTH // 2 - main_txt.get_width() // 2, 100))
    screen.blit(replay, (WIDTH // 2 - replay.get_width() // 2, 250))
    screen.blit(to_menu, (WIDTH // 2 - to_menu.get_width() // 2, 350))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                # звучит музыка поражения
                # ...
                for sprite in all_sprites:
                    sprite.kill()
                create_level(load_level(f"lvl{lvl}.txt"))
                global time_start
                time_start = time.time()
                return
        clock.tick(FPS)
        pygame.display.flip()


def finish_screen():  # конечный экран
    # звучит триумфальная музыка
    # ...
    fon = pygame.transform.scale(load_image('startscreen.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    game = pygame.font.Font(None, 100)
    small_game = pygame.font.Font(None, 50)
    pass_game = game.render("Congratulations!", True, BLACK)
    passing = small_game.render("You've passed the game!", True, BLACK)
    screen.blit(pass_game, (WIDTH // 2 - pass_game.get_width() // 2, HEIGHT // 2 - 140))
    screen.blit(passing, (WIDTH // 2 - passing.get_width() // 2, HEIGHT // 2 - 70))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for sprite in all_sprites:
                    sprite.kill()
                pygame.quit()
                sys.exit()
        clock.tick(FPS)
        pygame.display.flip()


class Tile(pygame.sprite.Sprite):  # блоки
    def __init__(self, tile_type, x, y):
        super().__init__(tiles_group, all_sprites)
        self.size_x = 64
        self.size_y = 64
        if tile_type == "g":
            self.size_x = TILE_SIZE
            self.size_y = 16
        elif tile_type == "h":
            self.size_x = 16
            self.size_y = TILE_SIZE
        elif tile_type == "s":
            self.size_x = 32
            self.size_y = 32
        elif tile_type == "w":
            self.size_x = TILE_SIZE * 2
            self.size_y = 32
        self.image = pygame.transform.scale(load_image(f"{tile_type}.png", "tileset"), (self.size_x, self.size_y))
        if self.size_y != TILE_SIZE:
            self.rect = self.image.get_rect().move(TILE_SIZE * x, (TILE_SIZE * y) + self.size_y)
        else:
            self.rect = self.image.get_rect().move(TILE_SIZE * x, TILE_SIZE * y)


class Spike(pygame.sprite.Sprite):  # шипы
    def __init__(self, x, y):
        super().__init__(spikes_group, all_sprites)
        self.image = pygame.transform.scale(load_image("t.png"), (TILE_SIZE, TILE_SIZE // 2))
        self.rect = self.image.get_rect()
        self.rect.bottom = (y + 1) * TILE_SIZE
        self.rect.left = x * TILE_SIZE


class Flag(pygame.sprite.Sprite):  # финишный флаг
    def __init__(self, x, y):
        super().__init__(flag_group, all_sprites)
        self.image = pygame.transform.scale(load_image("f.png"), (50, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.bottom = (y + 1) * TILE_SIZE
        self.rect.left = x * TILE_SIZE + TILE_SIZE // 2 - self.rect.width // 2


class Hero(pygame.sprite.Sprite):  # игрок
    def __init__(self, x, y):
        super().__init__(heroes_group, all_sprites)


BACKGROUND = pygame.transform.scale(load_image("background.png"), (WIDTH, HEIGHT))
start_screen()
if __name__ == '__main__':
    running = True
    create_level(load_level(f'lvl{lvl}.txt'))
    time_start = time.time()  # начало
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(BACKGROUND, (0, 0))
        time_now = time.time()
        minutes = str(int((time_now - time_start) // 60))
        seconds = u'%.2f' % ((time_now - time_start) % 60)
        time_font = pygame.font.Font(None, 30)
        time_txt = time_font.render(f"{minutes}.{seconds}", True, (0, 0, 0))
        tiles_group.draw(screen)
        spikes_group.draw(screen)
        heroes_group.draw(screen)
        flag_group.draw(screen)
        screen.blit(time_txt, (10, 5))
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
