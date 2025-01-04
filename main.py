import pygame

pygame.init()

FPS = 60
TILE_SIZE = 64
WIDTH = 1250
HEIGHT = 12 * TILE_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mountains")
lvl = 1
clock = pygame.time.Clock()

hero_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
thorns_group = pygame.sprite.Group()
flag_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


def start_screen():
    pass


def lvl_completed():
    pass


def game_over():
    pass


def finish_screen():
    pass
