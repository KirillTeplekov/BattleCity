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

player_images = {'lvl1_up': load_image(path_to_player + 'lvl1/up.png'), 'lvl1_down': load_image(path_to_player + 'lvl1/down.png'),
               'lvl1_left': load_image(path_to_player + 'lvl1/left.png'), 'lvl1_right': load_image(path_to_player + 'lvl1/right.png'),
               'lvl2_up': load_image(path_to_player + 'lvl2/up.png'), 'lvl2_down': load_image(path_to_player + 'lvl2/down.png'),
               'lvl2_left': load_image(path_to_player + 'lvl2/left.png'), 'lvl2_right': load_image(path_to_player + 'lvl2/right.png'),
               'lvl3_up': load_image(path_to_player + 'lvl3/up.png'), 'lvl3_down': load_image(path_to_player + 'lvl3/down.png'),
               'lvl3_left': load_image(path_to_player + 'lvl3/left.png'), 'lvl3_right': load_image(path_to_player + 'lvl3/right.png')}

enemy_images = {}  

class Player(Tanks):
    def __init__(self, posx, posy):
        super().__init__(player_images['lvl1_up'], posx, posy)
        self.atack = False
        self.lvl = 1
        self.speed = 8
        self.movement = False
        self.add(player_group)
        self.atack_count = 30
        
    def update(self):
        if self.atack and self.atack_count >= 30:
            bullet = Bullet('fast', self)
            self.atack_count = 0
        self.atack_count += 1
        
        if self.movement and not(pygame.sprite.spritecollideany(self, collide_group)):
            if self.direction == 'u':
                self.image = player_images['lvl' + str(self.lvl) + '_up']
                self.rect = self.rect.move(0, -self.speed) 
            elif self.direction == 'd':
                self.image = player_images['lvl' + str(self.lvl) + '_down']
                self.rect = self.rect.move(0, self.speed)
            elif self.direction == 'l':
                self.image = player_images['lvl' + str(self.lvl) + '_left']                
                self.rect = self.rect.move(-self.speed, 0)
            elif self.direction == 'r':
                self.image = player_images['lvl' + str(self.lvl) + '_right']
                self.rect = self.rect.move(self.speed, 0)
    
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
                Tile(tile_images['empty'], x, y, uncollide_group)
            elif level[y][x] == '#':
                Tile(tile_images['brick'], x, y, collide_group)
            elif level[y][x] == 'c':
                Tile(tile_images['concrete'], x, y, collide_group)
            elif level[y][x] == 'w':
                Water(x, y)
            elif level[y][x] == 'i':
                Tile(tile_images['ice'], x, y, ice_group)
            elif level[y][x] == 'b':
                Bushes(tile_images['bushes'], x, y)
            elif level[y][x] == '@':
                Tile(tile_images['empty'], x, y, uncollide_group)
                player = Player(x, y)
    
    uncollide_group.add(bushes_group)
    uncollide_group.add(ice_group)
    collide_group.add(water_group)       

# Create borders for game's board    
Border(32, 32, 32, 864)
Border(32, 32, 863, 32)
Border(864, 32, 864, 864)
Border(32, 864, 864, 864)
generate_level('level1.txt')
# Main game's loop
running = True

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.movement = True
                player.direction = 'u'
            elif event.key == pygame.K_DOWN:
                player.movement = True
                player.direction = 'd'                     
            elif event.key == pygame.K_LEFT:
                player.movement = True
                player.direction = 'l'
            elif event.key == pygame.K_RIGHT:
                player.movement = True
                player.direction = 'r'    
            elif event.key == pygame.K_SPACE:
                player.atack = True
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player.movement = False            
            elif event.key == pygame.K_DOWN:
                player.movement = False
            elif event.key == pygame.K_LEFT:
                player.movement = False
            elif event.key == pygame.K_RIGHT:
                player.movement = False
            elif event.key == pygame.K_SPACE:
                player.atack = False
                
    player.update()
    for sprite in bullet_group:
        sprite.update()
    for sprite in water_group:
        sprite.update()

    screen.fill(pygame.Color("grey"))
    
    collide_group.draw(screen)
    uncollide_group.draw(screen)
    
    player_group.draw(screen)
    bullet_group.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)