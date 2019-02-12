import os
import sys
import pygame
from gameObject import *

pygame.init()

# Constants
FPS = 30

width = 928
height = 896
v = 456
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


screen_images = [load_image('other/start_screen1.png'),
                 load_image('other/start_screen2.png')]


def start_screen():
    screen_num = 0
    sprite = pygame.sprite.Sprite()
    sprite.image = screen_images[screen_num]
    sprite.rect = sprite.image.get_rect()
    all_sprites.add(sprite)
    sprite.rect.x = 0
    sprite.rect.y = height

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if sprite.rect.y >= 0:
            screen.fill(pygame.Color('black'))
            sprite.rect = sprite.rect.move(0, -(v // 60))
            all_sprites.draw(screen)
        else:
            running = False
        clock.tick(60)
        pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print(screen_num)
                    screen_num = (screen_num + 1) % 2
                    print(screen_num)
                    sprite.image = screen_images[screen_num]
                elif event.key == pygame.K_DOWN:
                    screen_num = (screen_num + 1) % 2
                    sprite.image = screen_images[screen_num]

        clock.tick(60)
        all_sprites.draw(screen)
        pygame.display.flip()

    all_sprites.empty()


def game_over():
    pass


player = None
castle_flag = None


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
    global castle_flag
    for y in range(13):
        for x in range(13):
            if level[y][x] == '.':
                Tile(tile_images['empty'], x, y, uncollide_group)
            elif level[y][x] == '#':

                Brick(x, y)
            elif level[y][x] == 'c':
                Tile(tile_images['concrete'], x, y, collide_group)
            elif level[y][x] == 'w':
                Water(x, y)
            elif level[y][x] == 'i':
                Tile(tile_images['ice'], x, y, ice_group)
            elif level[y][x] == 'b':
                Tile(tile_images['bushes'], x, y, bushes_group)
            elif level[y][x] == 'F':
                castle_flag = Flag(x, y)
            elif level[y][x] == '@':
                Tile(tile_images['empty'], x, y, uncollide_group)
                player = Player(x, y)
    uncollide_group.add(bushes_group)
    uncollide_group.add(ice_group)
    collide_group.add(brick_group)
    return level[13]


if __name__ == "__main__":
    # Create borders for game's board
    Border(0, 0, width, x_indent, 'h')
    Border(0, 0, y_indent, height, 'v')
    Border(x_indent, height - y_indent, width, x_indent, 'h')
    Border(tile_width * 13 + x_indent, 0, y_indent, height, 'v')

    enemy_count = generate_level('level1.txt').split()
    tank_count = []
    for i in range(int(enemy_count[0])):
        tank_count.append('standard')
    for i in range(int(enemy_count[1])):
        tank_count.append('btr')
    for i in range(int(enemy_count[0])):
        tank_count.append('rapidfire')
    for i in range(int(enemy_count[0])):
        tank_count.append('heavy')
    enemy_on_lvl = int(enemy_count[0]) + int(enemy_count[1]) + int(
        enemy_count[2]) + int(enemy_count[3])
    enemy_on_board = 0
    respawn_timer = 120
    # Main game's loop
    running = True
    while running:
        if enemy_on_board <= 4 and respawn_timer >= 120:
            type = tank_count.pop(tank_count.index(choice(tank_count)))
            Enemy(type)
            enemy_on_board += 1

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
        castle_flag.update()
        bullet_group.add(bullet_player_group)
        bullet_group.add(bullet_enemy_group)
        for water in water_group:
            water.update()

        for bullet in bullet_player_group:
            bullet.update()

        for bullet in bullet_enemy_group:
            bullet.update()

        for boom in boom_group:
            boom.update()

        for brick in brick_group:
            brick.update()

        for enemy in enemy_group:
            enemy.update()

        screen.fill(pygame.Color("grey"))
        screen.fill(pygame.Color('black'),
                    pygame.Rect(x_indent, y_indent, tile_width * 13,
                                tile_height * 13))

        collide_group.draw(screen)
        uncollide_group.draw(screen)
        water_group.draw(screen)
        player_group.draw(screen)
        enemy_group.draw(screen)
        bullet_enemy_group.draw(screen)
        bullet_player_group.draw(screen)
        bushes_group.draw(screen)
        boom_group.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)
