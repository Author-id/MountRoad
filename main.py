import os
import sys
import time

import pygame

pygame.init()
pygame.mixer.init()

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
player = None
clock = pygame.time.Clock()

lvl_completed_sound = pygame.mixer.Sound("data/sounds/lvl_completed.wav")
game_sound = pygame.mixer.Sound("data/sounds/game.wav")
jump_sound = pygame.mixer.Sound("data/sounds/jump.wav")
game_over_sound = pygame.mixer.Sound("data/sounds/game_over.mp3")
finish_sound = pygame.mixer.Sound("data/sounds/finish.wav")

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
            elif level[y][x] == "f":
                Flag(x, y)
            elif level[y][x] == "@":
                House(x, y)
            elif level[y][x] == 'ш':
                Spike(x, y)
            elif level[y][x] in "yо":
                Sign(level[y][x], x, y)
            elif level[y][x] in "йёк":
                Stone(level[y][x], x, y)
            elif level[y][x] in "вгджзи":
                Tree(level[y][x], x, y)
            elif level[y][x] in "лмнп":
                Bush(level[y][x], x, y)
            elif level[y][x] != ".":
                Tile(level[y][x], x, y)


def level_up():  # новый уровень
    global lvl
    if lvl != 2:
        lvl += 1
    for sprite in all_sprites:
        sprite.kill()
    create_level(load_level(f"lvl{lvl}.txt"))
    return


def start_screen():  # начальный экран
    game_sound.play()
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
    lvl_completed_sound.play()
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
    game_sound.play()
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
    finish_sound.play()
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
        self.image = pygame.transform.scale(load_image("@.png", "objects"),
                                            (TILE_SIZE * 3, TILE_SIZE * 3))
        self.rect = self.image.get_rect()
        self.rect.bottom = (y + 1) * TILE_SIZE + 1
        self.rect.left = x * TILE_SIZE


class Tile(pygame.sprite.Sprite):  # блоки
    def __init__(self, tile_type, x, y):
        super().__init__(tile_group, all_sprites)
        self.image = pygame.transform.scale(load_image(f"{tile_type}.png", "tileset"),
                                            (TILE_SIZE, TILE_SIZE))
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
        self.image = pygame.transform.scale(load_image('spike_3.png', 'objects/spikes'),
                                            (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.bottom = (y + 1) * TILE_SIZE
        self.rect.left = x * TILE_SIZE


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(hero_group, all_sprites)

        self.idle_state = []
        self.idle_count = 0
        for i in range(1, 5):
            self.idle_state.append(load_image(f"idle{i}.png", 'hero/idle'))

        self.jump_state = []
        self.jump_count = 0
        for i in range(1, 7):
            self.jump_state.append(load_image(f"jump{i}.png", 'hero/jump'))

        self.run_state = []
        self.run_count = 0
        for i in range(1, 6):
            self.run_state.append(load_image(f"run{i}.png", 'hero/run'))

        self.img_name = self.idle_state[self.idle_count]
        self.image = pygame.transform.scale(self.img_name, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.bottom = (y + 1) * TILE_SIZE
        self.rect.left = x * TILE_SIZE

    def get_state(self, buttons):
        keys = pygame.key.get_pressed()
        states = []
        if buttons["space"]:
            states.append("jump")
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not keys[pygame.K_SPACE]:
            states.append("right")
            states.append('run')
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not keys[pygame.K_SPACE]:
            states.append("left")
            states.append('run')
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            states.append('left')
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            states.append('right')
        else:
            states.append("idle")
        return states

    def update(self, buttons):

        if not self.on_screen() or self.on_spikes():
            self.kill()
            game_over()
        if self.on_finish():
            lvl_completed()
            level_up()

        curr_state = self.get_state(buttons)
        if "idle" in curr_state:
            if self.idle_count < 4:
                self.idle_count += 1
            else:
                self.idle_count = 0
            self.img_name = self.idle_state[self.idle_count - 1]
            self.image = pygame.transform.scale(self.img_name, (TILE_SIZE, TILE_SIZE))

        if ('left' in curr_state or 'right' in curr_state) and 'run' in curr_state:
            self.run(curr_state)

    def run(self, curr_state):
        if self.run_count < 5:
            self.run_count += 0.25
        else:
            self.run_count = 1
        if self.run_count == int(self.run_count):
            self.img_name = self.run_state[int(self.run_count) - 1]
        self.image = pygame.transform.scale(self.img_name, (TILE_SIZE, TILE_SIZE))
        if 'left' in curr_state and 'right' in curr_state:
            pass
        elif 'left' in curr_state:
            self.image = pygame.transform.flip(self.image, 180, 0)
            if pygame.sprite.spritecollideany(self, tile_group) is None:
                self.rect.left -= TILE_SIZE * 0.09
            else:
                self.rect.left += 3
        elif 'right' in curr_state:
            if pygame.sprite.spritecollideany(self, tile_group) is None:
                self.rect.left += TILE_SIZE * 0.09
            else:
                self.rect.left += 3

    def on_screen(self):
        if self.rect.y <= HEIGHT:
            return True
        return False

    def on_spikes(self):
        if pygame.sprite.spritecollideany(self, spike_group):
            return True
        return False

    def on_finish(self):
        if pygame.sprite.spritecollideany(self, flag_group):
            return True
        return False



BACKGROUND = pygame.transform.scale(load_image(f"background_{lvl}.png"), (WIDTH, HEIGHT))
start_screen()
if __name__ == '__main__':
    running = True
    create_level(load_level(f'lvl{lvl}.txt'))
    time_start = time.time()  # начало
    while running:
        keys = {"space": False}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    keys["space"] = True
        screen.blit(BACKGROUND, (0, 0))
        time_now = time.time()
        minutes = str(int((time_now - time_start) // 60))
        seconds = u'%.2f' % ((time_now - time_start) % 60)
        time_font = pygame.font.Font(None, 30)
        time_txt = time_font.render(f"{minutes}.{seconds}", True, (0, 0, 0))
        hero_group.update(keys)
        for group in group_lst:
            group.draw(screen)
        screen.blit(time_txt, (10, 5))
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()