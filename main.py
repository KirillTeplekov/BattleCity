import os
import sys
import pygame
from gameObject import *

pygame.init()
pygame.mixer.init()

# Constants
FPS = 30

width = 928
height = 896
v = 456
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Music
background = pygame.mixer.Sound('data/sounds/background.ogg')
steel = pygame.mixer.Sound('data/sounds/steel.ogg')
brick = pygame.mixer.Sound('data/sounds/brick.ogg')
bonus = pygame.mixer.Sound('data/sounds/bonus.ogg')
explosion = pygame.mixer.Sound('data/sounds/explosion.ogg')
fire = pygame.mixer.Sound('data/sounds/fire.ogg')
gameover = pygame.mixer.Sound('data/sounds/gameover.ogg')
gamestart = pygame.mixer.Sound('data/sounds/gamestart.ogg')


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


def terminate():
    pygame.quit()
    sys.exit()


screen_images = [load_image('other/start_screen1.png'),
                 load_image('other/start_screen2.png')]


def start_screen():
    all_sprites = pygame.sprite.Group()
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
                terminate()
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
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    steel.play()
                    screen_num = (screen_num + 1) % 2
                elif event.key == pygame.K_DOWN:
                    steel.play()
                    screen_num = (screen_num + 1) % 2
                sprite.image = screen_images[screen_num]
                if event.key == pygame.K_SPACE:
                    if screen_num == 0:
                        steel.play()
                        return True
                    else:
                        terminate()
        clock.tick(60)
        all_sprites.draw(screen)
        pygame.display.flip()

    all_sprites.empty()


pause_image = load_image('other/pause.png')
back_image = load_image('other/back.png')


def pause_screen():
    fon_sprites = pygame.sprite.Group()
    fon = pygame.sprite.Sprite()
    fon.image = pause_image
    fon.rect = fon.image.get_rect()
    fon_sprites.add(fon)
    fon.rect.x = 0
    fon.rect.y = 0

    back_btn_group = pygame.sprite.Group()
    back = pygame.sprite.Sprite()
    back.image = back_image
    back.rect = back.image.get_rect()
    back_btn_group.add(back)
    back.rect.x = 451
    back.rect.y = 468

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                posx, posy = pygame.mouse.get_pos()
                if back.rect.x < posx < (
                            back.rect.x + tile_width) and back.rect.y < posy < (
                            back.rect.y + tile_height):
                    return True

        clock.tick(60)
        fon_sprites.draw(screen)
        back_btn_group.draw(screen)
        pygame.display.flip()

    fon_sprites.empty()


game_over_image = load_image('other/game_over.png')


def game_over():
    fon_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    sprite.image = game_over_image
    sprite.rect = sprite.image.get_rect()
    fon_sprites.add(sprite)
    sprite.rect.x = 0
    sprite.rect.y = height

    gameover.set_volume(1)
    gameover.play()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if sprite.rect.y >= 0:
            screen.fill(pygame.Color('black'))
            sprite.rect = sprite.rect.move(0, -(v // 60))
            fon_sprites.draw(screen)
        else:
            running = False
        clock.tick(60)
        pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fon_sprites.empty()
                    return
        clock.tick(60)
        fon_sprites.draw(screen)
        pygame.display.flip()


win_image = load_image('other/win.png')


def win_screen():
    fon_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    sprite.image = win_image
    sprite.rect = sprite.image.get_rect()
    fon_sprites.add(sprite)
    sprite.rect.x = 0
    sprite.rect.y = height

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if sprite.rect.y >= 0:
            screen.fill(pygame.Color('black'))
            sprite.rect = sprite.rect.move(0, -(v // 60))
            fon_sprites.draw(screen)
        else:
            running = False
        clock.tick(60)
        pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fon_sprites.empty()
                    return
        clock.tick(60)
        all_sprites.draw(screen)
        pygame.display.flip()


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


level = True
levels = True
if __name__ == "__main__":

    game = True
    while game:
        levels = start_screen()
        level_num = 0
        while levels:
            gamestart.set_volume(1)
            gamestart.play()
            # Create borders for game's board
            Border(0, 0, width, x_indent, 'h')
            Border(0, 0, y_indent, height, 'v')
            Border(x_indent, height - y_indent, width, x_indent, 'h')
            Border(tile_width * 13 + x_indent, 0, y_indent, height, 'v')
            enemy_count = generate_level(
                'level' + str(level_num) + '.txt').split()
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

            # timers
            respawn_timer = 120
            stop_timer = 0

            pause = False

            level = True
            while level:
                background.set_volume(0.1)
                background.play()
                if pause:
                    state = pause_screen()
                    if state:
                        levels = False
                        break
                    else:
                        pause = False
                else:
                    if player.hp == 0:
                        levels = False
                        game_over()
                        break
                    if len(tank_count) == 0 and len(enemy_group) == 0:
                        win_screen()
                        break
                    if len(
                            enemy_group) <= 4 and respawn_timer >= 120 and tank_count:
                        type = tank_count.pop(
                            tank_count.index(choice(tank_count)))
                        if type == 'standard' and randint(1, 5) == 1:
                            Enemy(type, True)
                        else:
                            Enemy(type)
                        respawn_timer = 0
                    respawn_timer += 1

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            terminate()
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
                                fire.set_volume(1)
                                fire.play()
                                player.atack = True
                            elif event.key == pygame.K_ESCAPE:
                                pause = True

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
                    for bonus in bonus_group:
                        bonus.update(player)
                    for shield in shield_group:
                        shield.update()

                    screen.fill(pygame.Color("grey"))
                    screen.fill(pygame.Color('black'),
                                pygame.Rect(x_indent, y_indent,
                                            tile_width * 13,
                                            tile_height * 13))

                    collide_group.draw(screen)
                    uncollide_group.draw(screen)
                    water_group.draw(screen)
                    player_group.draw(screen)
                    shield_group.draw(screen)
                    enemy_group.draw(screen)
                    bonus_group.draw(screen)
                    bullet_enemy_group.draw(screen)
                    bullet_player_group.draw(screen)
                    bushes_group.draw(screen)
                    boom_group.draw(screen)

                    if castle_flag.state == 'off':
                        levels = False
                        game_over()
                        break
                    pygame.display.flip()

                    clock.tick(FPS)

            all_sprites.empty()
            enemy_group.empty()
            player_group.empty()
            uncollide_group.empty()
            collide_group.empty()
            water_group.empty()
            brick_group.empty()
            bushes_group.empty()
            bullet_group.empty()
            bullet_enemy_group.empty()
            bullet_player_group.empty()
            bonus_group.empty()
            boom_group.empty()
            shield_group.empty()
            level_num = 3 - ((level_num + 1) % 3)
