import os
import sys
import pygame
from gameObject import Tile

pygame.init()

# Constants 
FPS = 30

width = height = 960 
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

player = None

# Function, which load image to sprite
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image

# Image dict for gameObject 
tile_images = {'brick': load_image('tiles/brick.png', -1), 'empty': load_image('tiles/empty_block.png'), 'concrete': load_image('tiles/concrete.png'),
               'bushes': load_image('tiles/bushes.png'), 'ice': load_image('tiles/ice.png'), 'water': load_image('tiles/water.png')}
enemy_images = {}

# Game's group
all_sprites = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

# Function, which read level from text file and generate this level
def generate_level(filename):
    
    # Read level
    filename = "data/levels/" + filename
    mapFile = open(filename, 'r')
    level = mapFile.readlines()
    mapFile.close()
    
    for i in range(len(level)):
        level[i] = level[i].rstrip('\r\n')
    
    # Generate level
    global player
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile(tiles_image['empty'], x, y)
            elif level[y][x] == '#':
                Tile(tiles_image['brick'], x, y)
            elif level[y][x] == 'c':
                Tile(tiles_image['concrete'], x, y)
            elif level[y][x] == 'w':
                Tile(tiles_image['water'], x, y)
            elif level[y][x] == 'i':
                Tile(tiles_image['ice'], x, y)
            elif level[y][x] == 'b':
                Tile(tiles_image['bushes'], x, y)                
            elif level[y][x] == '@':
                Tile(tiles_image['empty'], x, y)
                player = Player(x, y)
    
# Main game's loop
running = True

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pass
            if event.key == pygame.K_RIGHT:
                pass
            if event.key == pygame.K_UP:
                pass
            if event.key == pygame.K_DOWN:
                pass

    screen.fill(pygame.Color("grey"))
    
    tiles_group.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)