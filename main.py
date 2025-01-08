import pygame
import os
import sys
import time

pygame.init()

FPS = 60
TILE_SIZE = 60
WIDTH = 1320
HEIGHT = 12 * TILE_SIZE
MAX_LVL = 2
BLACK = pygame.Color('black')
DARK_GREY = (40, 40, 40)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mountains")
lvl = 1
clock = pygame.time.Clock()

sign_group = pygame.sprite.Group()
bonfire_group = pygame.sprite.Group()
bash_group = pygame.sprite.Group()
tree_group = pygame.sprite.Group()
stone_group = pygame.sprite.Group()
house_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
tile_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
flag_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
group_lst = [tree_group, stone_group, house_group, sign_group,
             tile_group, spike_group, flag_group, bash_group, hero_group]


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
                player
            elif level[y][x] == "f":
                Flag(x, y)
            elif level[y][x] == "@":
                House(x, y)
            elif level[y][x] in "yо":
                Sign(level[y][x], x, y)
            elif level[y][x] in "йёк":
                Stone(level[y][x], x, y)
            elif level[y][x] in "вгджзи":
                Tree(level[y][x], x, y)
            elif level[y][x] in "лмнп":
                Bush(level[y][x], x, y)
            elif level[y][x] == 'ш':
                Spike(x, y)
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
    press_font = pygame.font.Font(None, 30)
    main_font = pygame.font.Font(None, 100)
    press_txt = press_font.render('press any button', True, DARK_GREY)
    screen.blit(press_txt, (WIDTH // 2 - press_txt.get_width() // 2, 130))
    main_txt = main_font.render('Mount Road', True, DARK_GREY)
    screen.blit(main_txt, (WIDTH // 2 - main_txt.get_width() // 2, 70))

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
    c_text = completed.render(f'Level {lvl} completed', True, BLACK)
    screen.blit(c_text, (WIDTH // 2 - c_text.get_width() // 2, HEIGHT // 2 - c_text.get_height() // 2))
    pressed = pygame.font.Font(None, 25)
    p_text = pressed.render('press any button', True, DARK_GREY)
    screen.blit(p_text, (WIDTH // 2 - p_text.get_width() // 2, 410))
    times = pygame.font.Font(None, 40)
    t_text = times.render(f"Your time: {minutes}.{seconds}", True, DARK_GREY)
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
    press_font = pygame.font.Font(None, 40)
    lost = pygame.font.Font(None, 100)
    main_txt = lost.render('Game Over', True, BLACK)
    replay = press_font.render('Press 1 if you want to restart this level', True, DARK_GREY)
    to_menu = press_font.render('Press 2 if you want to go to menu', True, DARK_GREY)
    screen.blit(main_txt, (WIDTH // 2 - main_txt.get_width() // 2, 150))
    screen.blit(replay, (WIDTH // 2 - replay.get_width() // 2, 220))
    screen.blit(to_menu, (WIDTH // 2 - to_menu.get_width() // 2, 260))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
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
    fon = pygame.transform.scale(load_image('finishscreen.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    game = pygame.font.Font(None, 100)
    small_game = pygame.font.Font(None, 50)
    pass_game = game.render("Congratulations!", True, BLACK)
    passing = small_game.render("You've passed the game!", True, DARK_GREY)
    screen.blit(pass_game, (WIDTH // 2 - pass_game.get_width() // 2, HEIGHT // 2 - 200))
    screen.blit(passing, (WIDTH // 2 - passing.get_width() // 2, HEIGHT // 2 - 130))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for sprite in all_sprites:
                    sprite.kill()
                pygame.quit()
                sys.exit()
        clock.tick(FPS)
        pygame.display.flip()


class Sign(pygame.sprite.Sprite):
    def __init__(self, sign_type, x, y):
        super().__init__(sign_group, all_sprites)
        self.image = pygame.transform.scale(load_image(f"{sign_type}.png", "objects/Signs"), (35, 48))
        self.rect = self.image.get_rect()
        self.rect.bottom = (y + 1) * TILE_SIZE + 1
        self.rect.left = x * TILE_SIZE + 10


class Bush(pygame.sprite.Sprite):
    def __init__(self, bash_type, x, y):
        super().__init__(bash_group, all_sprites)
        self.size_x = TILE_SIZE * 3
        self.size_y = TILE_SIZE * 2
        if bash_type == "п":
            self.size_x = TILE_SIZE * 1.5
            self.size_y = 32
        self.image = pygame.transform.scale(load_image(f"{bash_type}.png", "objects/Bushes"),
                                            (self.size_x, self.size_y))
        self.rect = self.image.get_rect()
        self.rect.bottom = (y + 1) * TILE_SIZE
        self.rect.left = x * TILE_SIZE + 3


class Tree(pygame.sprite.Sprite):
    def __init__(self, tree_type, x, y):
        super().__init__(tree_group, all_sprites)
        self.image = pygame.transform.scale(load_image(f"{tree_type}.png", "objects/Trees"),
                                            (TILE_SIZE * 2, TILE_SIZE * 3))
        self.rect = self.image.get_rect()
        self.rect.bottom = (y + 1) * TILE_SIZE + 1
        self.rect.left = x * TILE_SIZE
        if tree_type == "д":
            self.rect.left -= 35
        else:
            self.rect.left -= 18


class Stone(pygame.sprite.Sprite):
    def __init__(self, stone_type, x, y):
        super().__init__(stone_group, all_sprites)
        self.image = pygame.transform.scale(load_image(f"{stone_type}.png", "objects/Stones"),
                                            (TILE_SIZE * 2, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.bottom = (y + 1) * TILE_SIZE + 2
        self.rect.left = x * TILE_SIZE + 10


class House(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(house_group, all_sprites)
        self.image = pygame.transform.scale(load_image("@.png", "objects"), (TILE_SIZE * 3, TILE_SIZE * 3))
        self.rect = self.image.get_rect()
        self.rect.bottom = (y + 1) * TILE_SIZE + 1
        self.rect.left = x * TILE_SIZE


class Tile(pygame.sprite.Sprite):  # блоки
    def __init__(self, tile_type, x, y):
        super().__init__(tile_group, all_sprites)
        self.image = pygame.transform.scale(load_image(f"{tile_type}.png", "tileset"), (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect().move(TILE_SIZE * x, TILE_SIZE * y)


class Flag(pygame.sprite.Sprite):  # финишный флаг
    def __init__(self, x, y):
        super().__init__(flag_group, all_sprites)
        self.image = pygame.transform.scale(load_image("f.png", "objects"), (48, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.bottom = (y + 1) * TILE_SIZE
        self.rect.left = x * TILE_SIZE + 10


class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(spike_group, all_sprites)
        self.image = pygame.transform.scale(load_image('spike.png', 'objects/spikes'), (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.bottom = (y + 1) * TILE_SIZE
        self.rect.left = x * TILE_SIZE


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(hero_group, all_sprites)
        self.image = pygame.transform.scale(load_image('Hero.png', 'hero'), (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.bottom = (y + 1) * TILE_SIZE
        self.rect.left = x * TILE_SIZE


BACKGROUND = pygame.transform.scale(load_image(f"background_{lvl}.png"), (WIDTH, HEIGHT))
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
        for group in group_lst:
            group.draw(screen)
        screen.blit(time_txt, (10, 5))
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
