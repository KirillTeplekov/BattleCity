import os
import sys
import pygame
from gameObject import *

pygame.init()

# Constants 
FPS = 30

width = 928
height = 896
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

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
               'bushes': load_image('tiles/bushes.png'), 'ice': load_image('tiles/ice.png')}
player_lvl1 = {'lvl1_up': load_image('tanks/player/lvl1/up.png'), 'lvl1_down': load_image('tanks/player/lvl1/down.png'),
               'lvl1_left': load_image('tanks/player/lvl1/left.png'), 'lvl1_right': load_image('tanks/player/lvl1/right.png')}
player_lvl2 = {'lvl2_up': load_image('tanks/player/lvl2/up.png'), 'lvl2_down': load_image('tanks/player/lvl2/down.png'),
               'lvl2_left': load_image('tanks/player/lvl2/left.png'), 'lvl2_right': load_image('tanks/player/lvl2/right.png')}
player_lvl3 = {'lvl3_up': load_image('tanks/player/lvl3/up.png'), 'lvl3_down': load_image('tanks/player/lvl3/down.png'),
               'lvl3_left': load_image('tanks/player/lv3/left.png'), 'lvl3_right': load_image('tanks/player/lvl3/right.png')}

class Players(Tanks):
    def __init__(self, posx, posy):
        super().__init__(player_lvl1['lvl1_up'], posx, posy)
        sell.lvl = 1
    
    def update(self):
        if not(pygame.sprite.spritecollideany(self, colide_group)):
            if self.up:
                self.rect = self.move(-16, 0)
            elif self.down:
                self.rect = self.move(16, 0)
            elif self.left:
                self.rect = self.move(0, -16)
            elif self.right:
                self.rect = self.move(0, 16)
    
player = None

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
                Tile(tiles_image['empty'], x, y, colide_group)
            elif level[y][x] == '#':
                Tile(tiles_image['brick'], x, y, colide_group)
            elif level[y][x] == 'c':
                Tile(tiles_image['concrete'], x, y, colide_group)
            elif level[y][x] == 'w':
                Tile(tiles_image['water'], x, y, colide_group)
            elif level[y][x] == 'i':
                Tile(tiles_image['ice'], x, y, uncolide_group)
            elif level[y][x] == 'b':
                Tile(tiles_image['bushes'], x, y, uncolide_group)
            elif level[y][x] == '@':
                Tile(tiles_image['empty'], x, y, colide_group)
                player = Player(x, y)

# Create borders for game's board    
Border(32, 32, 32, 864)
Border(32, 32, 863, 32)
Border(864, 32, 864, 864)
Border(32, 864, 864, 864, 864)

# Main game's loop
running = True

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.up = True
                player.update()
            elif event.key == pygame.K_DOWN:
                player.down = True
                player.update()                            
            elif event.key == pygame.K_LEFT:
                player.down = True
                player.update()                
            elif event.key == pygame.K_RIGHT:
                player.down = True
                player.update()                
            

    screen.fill(pygame.Color("grey"))
    
    tiles_group.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)