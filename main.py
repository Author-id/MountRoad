import pygame
import os
import sys
import time

pygame.init()
pygame.mixer.init()

FPS = 60
TILE_SIZE = 60
WIDTH = 1320
HEIGHT = 12 * TILE_SIZE
MAX_LVL = 2
HEIGHT_JUMP = 18
FREE_FALL = 13
BLACK = pygame.Color('black')
DARK_GREY = (40, 40, 40)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mount Road")
lvl = 1
player = None
clock = pygame.time.Clock()

start_sound = pygame.mixer.Sound("data/sounds/start.wav")
main_sound = pygame.mixer.Sound("data/sounds/main.wav")
lvl_completed_sound = pygame.mixer.Sound("data/sounds/lvl_completed.wav")
jump_sound = pygame.mixer.Sound("data/sounds/jump.wav")
jump_sound.set_volume(0.15)
game_over_sound = pygame.mixer.Sound("data/sounds/game_over.mp3")
game_over_sound.set_volume(0.25)
finish_sound = pygame.mixer.Sound("data/sounds/finish.wav")
finish_sound.set_volume(0.25)

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
    start_sound.play(-1)
    start_sound.set_volume(0.5)
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
                start_sound.stop()
                main_sound.play(-1)
                main_sound.set_volume(0.25)
                return
        clock.tick(FPS)
        pygame.display.flip()


def lvl_completed():  # уровень пройден
    lvl_completed_sound.play()
    lvl_completed_sound.set_volume(0.15)
    all_sprites.draw(screen)
    completed = pygame.font.Font(None, 100)
    c_text = completed.render(f'Level {lvl} completed', True, BLACK)
    screen.blit(c_text, (WIDTH // 2 - c_text.get_width() // 2, HEIGHT // 2 - c_text.get_height() // 2))
    pressed = pygame.font.Font(None, 40)
    p_text = pressed.render('press any button', True, DARK_GREY)
    screen.blit(p_text, (WIDTH // 2 - p_text.get_width() // 2, 440))
    times = pygame.font.Font(None, 55)
    t_text = times.render(f"Time: {minutes}.{seconds}", True, BLACK)
    screen.blit(t_text, (WIDTH // 2 - t_text.get_width() // 2, 400))

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
    game_over_sound.play()
    game_over_sound.set_volume(0.15)
    all_sprites.draw(screen)
    press_font = pygame.font.Font(None, 40)
    lost = pygame.font.Font(None, 100)
    main_txt = lost.render('Game Over', True, BLACK)
    replay = press_font.render('press 1 - to restart this level', True, DARK_GREY)
    to_menu = press_font.render('press 2 - go to menu', True, DARK_GREY)
    screen.blit(main_txt, (WIDTH // 2 - main_txt.get_width() // 2, 250))
    screen.blit(replay, (WIDTH // 2 - replay.get_width() // 2, 320))
    screen.blit(to_menu, (WIDTH // 2 - to_menu.get_width() // 2, 360))

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
    finish_sound.set_volume(0.15)
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
        self.speed = 4
        self.free_fall = False
        self.is_jump = False
        self.height_jump = HEIGHT_JUMP
        self.new_state = ["idle"]

        self.idle_state = []
        self.idle_count = 0
        for i in range(1, 5):
            self.idle_state.append(load_image(f"idle{i}.png", 'hero/idle'))

        self.jump_state = []
        self.jump_count = 0
        for i in range(1, 7):
            self.jump_state.append(load_image(f"jump{i}.png", 'hero/jump'))

        self.curr_image = 0
        self.img_name = self.idle_state[self.idle_count]
        self.image = pygame.transform.scale(self.img_name, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.bottom = (y + 1) * TILE_SIZE
        self.rect.left = x * TILE_SIZE

    def get_state(self, buttons):
        keys = pygame.key.get_pressed()
        states = []
        if (buttons["space"] and pygame.sprite.spritecollideany(self, tile_group)) or self.is_jump:
            states.append("jump")
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            states.append("right")
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            states.append("left")
        if len(states) == 0:
            states.append("idle")
        return states

    def update(self, buttons):
        if not self.on_screen() or self.on_spikes():
            self.kill()
            game_over()
        if self.on_finish():
            self.kill()
            lvl_completed()
            level_up()

        self.rect.bottom += 1
        curr_state = self.get_state(buttons)
        self.rect.bottom -= 1

        if curr_state != self.new_state:
            self.idle_count = 0
            self.jump_count = 0
            # self.run_count = 0
            self.curr_image = 0
            self.new_state = curr_state

        if "idle" in curr_state:
            self.idle(curr_state)

        elif "jump" in curr_state:
            self.jump(curr_state)

        if not self.is_jump and not self.collide_mask_check(self, tile_group):
            self.image = pygame.transform.scale(self.jump_state[3], (TILE_SIZE, TILE_SIZE))
            self.rect.bottom += FREE_FALL
            if pygame.sprite.spritecollideany(self, tile_group):
                self.rect.bottom -= self.rect.bottom % TILE_SIZE
                self.image = pygame.transform.scale(self.idle_state[self.curr_image], (TILE_SIZE, TILE_SIZE))

    def idle(self, curr_state):
        self.idle_count = (self.idle_count + 1) % 9
        if self.idle_count == 8:
            self.curr_image = (self.curr_image + 1) % len(self.idle_state)
            self.image = pygame.transform.flip(self.idle_state[self.curr_image], "left" in curr_state, 0)
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))

    def jump(self, curr_state):
        self.is_jump = True

        self.rect.y -= self.height_jump
        self.height_jump -= 1
        if pygame.sprite.spritecollideany(self, tile_group):
            if self.height_jump > 0:
                self.rect.bottom += self.height_jump
                self.height_jump = 0
            elif self.height_jump < 0:
                self.rect.bottom -= self.rect.bottom % TILE_SIZE
                self.height_jump = HEIGHT_JUMP
                self.is_jump = False

        if "right" in curr_state:
            self.rect.x += self.speed
            if pygame.sprite.spritecollideany(self, tile_group):
                self.rect.x -= self.speed

        elif "left" in curr_state:
            self.rect.x -= self.speed
            if pygame.sprite.spritecollideany(self, tile_group):
                self.rect.x += self.speed

        if self.jump_count < 3 or self.jump_count > 4:
            self.jump_count += 1
            clock.tick(FPS)
            if self.jump_count == 7:
                self.jump_count = 0
        elif 3 <= self.jump_count <= 4:
            if self.height_jump > 0:
                if self.height_jump > (HEIGHT_JUMP - 2):
                    self.jump_count = 2
                else:
                    self.jump_count = 3
            else:
                if self.height_jump > -(HEIGHT_JUMP - 1):
                    self.jump_count = 4
                else:
                    self.jump_count = 5
        self.img_name = self.jump_state[self.jump_count - 1]
        self.image = pygame.transform.flip(self.img_name, "left" in curr_state, 0)
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))

    def collide_mask_check(self, sprite, sprite_group):
        curr_mask = pygame.mask.from_surface(sprite.image)
        for item in sprite_group:
            sprite_mask = pygame.mask.from_surface(item.image)
            offset = (item.rect.x - sprite.rect.x, item.rect.y - sprite.rect.y)
            if curr_mask.overlap(sprite_mask, offset):
                return True
        return False

    def on_screen(self):
        if self.rect.y <= HEIGHT:
            return True
        return False

    def on_spikes(self):
        if self.collide_mask_check(self, spike_group):
            return True
        return False

    def on_finish(self):
        if self.collide_mask_check(self, flag_group):
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
