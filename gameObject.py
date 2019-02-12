import pygame
from main import load_image
from random import choice, randint

# Game's group
all_sprites = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
uncollide_group = pygame.sprite.Group()
collide_group = pygame.sprite.Group()
ice_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
brick_group = pygame.sprite.Group()
bushes_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
bullet_enemy_group = pygame.sprite.Group()
bullet_player_group = pygame.sprite.Group()
boom_group = pygame.sprite.Group()

# Direction
DIRECTION = ['u', 'd', 'l', 'r']  # 'u' - up, 'd' - down, 'l' - left, 'r' - r

# Path
path_to_player = 'tanks/player/'
path_to_enemy = 'tanks/enemy/'

# Tile size
tile_width = 64
tile_height = 64

# Indented for objects that game were indented at the edges as in the original 
x_indent = 32
y_indent = 32

# Image dict for gameObject
tile_images = {'empty': load_image('tiles/empty_block.png'),
               'concrete': load_image('tiles/concrete.png'),
               'bushes': load_image('tiles/bushes.png'),
               'ice': load_image('tiles/ice.png')}

player_images = {'lvl1_up': load_image(path_to_player + 'lvl1/up.png'),
                 'lvl1_down': load_image(path_to_player + 'lvl1/down.png'),
                 'lvl1_left': load_image(path_to_player + 'lvl1/left.png'),
                 'lvl1_right': load_image(path_to_player + 'lvl1/right.png'),
                 'lvl2_up': load_image(path_to_player + 'lvl2/up.png'),
                 'lvl2_down': load_image(path_to_player + 'lvl2/down.png'),
                 'lvl2_left': load_image(path_to_player + 'lvl2/left.png'),
                 'lvl2_right': load_image(path_to_player + 'lvl2/right.png'),
                 'lvl3_up': load_image(path_to_player + 'lvl3/up.png'),
                 'lvl3_down': load_image(path_to_player + 'lvl3/down.png'),
                 'lvl3_left': load_image(path_to_player + 'lvl3/left.png'),
                 'lvl3_right': load_image(path_to_player + 'lvl3/right.png')}

enemy_images = {'btr': {'btr_u': load_image(path_to_enemy + 'btr/up.png'),
                        'btr_d': load_image(path_to_enemy + 'btr/down.png'),
                        'btr_l': load_image(path_to_enemy + 'btr/left.png'),
                        'btr_r': load_image(path_to_enemy + 'btr/right.png')},
                'heavy': {
                    'heavy_u': load_image(path_to_enemy + 'heavy/up.png'),
                    'heavy_d': load_image(path_to_enemy + 'heavy/down.png'),
                    'heavy_l': load_image(path_to_enemy + 'heavy/left.png'),
                    'heavy_r': load_image(path_to_enemy + 'heavy/right.png')},
                'rapidfire': {'rapidfire_u': load_image(
                    path_to_enemy + 'rapidfire/up.png'),
                    'rapidfire_d': load_image(
                        path_to_enemy + 'rapidfire/down.png'),
                    'rapidfire_l': load_image(
                        path_to_enemy + 'rapidfire/left.png'),
                    'rapidfire_r': load_image(
                        path_to_enemy + 'rapidfire/right.png')},
                'standard': {'standard_u': load_image(
                    path_to_enemy + 'standard/up.png'),
                    'standard_d': load_image(
                        path_to_enemy + 'standard/down.png'),
                    'standard_l': load_image(
                        path_to_enemy + 'standard/left.png'),
                    'standard_r': load_image(
                        path_to_enemy + 'standard/right.png')}}


class Border(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, dir):
        super().__init__(collide_group)
        if dir == 'h':
            self.image = pygame.Surface([0, 0])
            self.rect = pygame.Rect(x, y, w, h)
        else:
            self.image = pygame.Surface([0, 0])
            self.rect = pygame.Rect(x, y, w, h)


# Tiles
class Tile(pygame.sprite.Sprite):
    def __init__(self, image, posx, posy, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect().move(tile_width * posx + x_indent,
                                               tile_height * posy + y_indent)
        self.mask = pygame.mask.from_surface(self.image)


class Water(Tile):
    image_1 = pygame.image.load('data/tiles/water.png')
    image_2 = pygame.image.load('data/tiles/water_2.png')

    def __init__(self, posx, posy):
        super().__init__(Water.image_2, posx, posy, water_group)
        self.image_1 = Water.image_1
        self.image_2 = Water.image_2
        self.index = 0

    def update(self):
        if self.index < 3:
            self.image = self.image_1
            self.index += 1
        elif self.index < 6:
            self.image = self.image_2
            self.index += 1
        else:
            self.index = 0


class Flag(Tile):
    flag_on = load_image('other/flag_on.png')
    flag_off = load_image('other/flag_off.png')

    def __init__(self, posx, posy):
        super().__init__(Flag.flag_on, posx, posy, collide_group)

    def update(self):
        if pygame.sprite.spritecollideany(self, bullet_group):
            self.image = Flag.flag_off
            game_over()


class Brick(Tile):
    brick_images = {'brick_0': load_image('tiles/brick_1.png'),
                    'brick_1': load_image('tiles/brick_2.png'),
                    'brick_2': load_image('tiles/brick_3.png'),
                    'brick_3': load_image('tiles/brick_4.png')}

    def __init__(self, posx, posy):
        super().__init__(Brick.brick_images['brick_0'], posx, posy,
                         brick_group)
        self.state = 0  # 0 - 0 hit, 1 - 1 hit, 2 - 2 hit, 3 - 3 hit, 4 - destroy

    def update(self):
        if pygame.sprite.spritecollideany(self, bullet_group):
            for bullet in bullet_group:
                if pygame.sprite.collide_rect(self, bullet):
                    bullet.boom()
            self.state += 1
            if self.state == 4:
                self.kill()
            else:
                self.image = Brick.brick_images['brick_' + str(self.state)]


# Tanks
class Tanks(pygame.sprite.Sprite):
    def __init__(self, image, posx, posy):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect().move(tile_width * posx + x_indent,
                                               tile_height * posy + y_indent)
        self.hp = 0
        self.direction = ''  # 'u' - up, 'd' - down, 'l' - left, 'r' - r


class Player(Tanks):
    def __init__(self, posx, posy):
        super().__init__(player_images['lvl1_up'], posx, posy)
        self.hp = 3
        self.direction = 'u'
        self.atack = False
        self.lvl = 1
        self.speed = 8
        self.movement = False
        self.add(player_group)
        self.atack_count = 30

    def update(self):
        move_pos = (0, 0)

        if self.atack and self.atack_count >= 30:
            bullet = Bullet('fast', self)
            self.atack_count = 0
        self.atack_count += 1

        if self.movement:
            self.rotate()
            if self.direction == 'u':
                new_pos = (self.rect.x, self.rect.y - self.speed)
            elif self.direction == 'd':
                new_pos = (self.rect.x, self.rect.y + self.speed)
            elif self.direction == 'l':
                new_pos = (self.rect.x - self.speed, self.rect.y)
            elif self.direction == 'r':
                new_pos = (self.rect.x + self.speed, self.rect.y)

            player_rect = pygame.Rect(new_pos, [64, 64])

            # collisions with tiles
            if player_rect.collidelist(list(collide_group)) != -1:
                return
            if player_rect.collidelist(list(water_group)) != -1:
                return

            # if no collision, move player
            self.rect.topleft = (new_pos)

    def rotate(self):
        if self.direction == 'u':
            self.image = player_images['lvl' + str(self.lvl) + '_up']
        elif self.direction == 'd':
            self.image = player_images['lvl' + str(self.lvl) + '_down']
            self.stop = ''
        elif self.direction == 'l':
            self.image = player_images['lvl' + str(self.lvl) + '_left']
            self.stop = ''
        elif self.direction == 'r':
            self.image = player_images['lvl' + str(self.lvl) + '_right']


class Enemy(Tanks):
    hp = {'btr': 1, 'rapidfire': 1, 'standard': 1, 'heavy': 4}
    speed = {'btr': 12, 'rapidfire': 8, 'standard': 8, 'heavy': 8}
    bullet_speed = {'btr': 'standard', 'rapidfire': 'fast',
                    'standard': 'standard', 'heavy': 'standard'}
    spawn_place = [(5, 5), (5, 5), (5, 5)]

    def __init__(self, type):
        self.type = type
        self.direction = choice(DIRECTION)
        self.image = enemy_images[type][type + '_' + self.direction]
        posx, posy = choice(Enemy.spawn_place)
        super().__init__(self.image, posx, posy)
        self.hp = Enemy.hp[type]
        self.speed = Enemy.speed[type]
        self.bullet_speed = Enemy.bullet_speed[type]
        self.add(enemy_group)
        self.step_count = 0
        self.atack_count = 30

    def update(self):
        if self.step_count == 0:
            step_count, self.direction = self.movement_control()
        self.rotate()
        if self.atack_count >= 120:
            bullet = Bullet(Enemy.bullet_speed[self.type], self)
            self.atack_count = 0
        self.atack_count += 1

        if self.direction == 'u':
            new_pos = (self.rect.x, self.rect.y - self.speed)
        elif self.direction == 'd':
            new_pos = (self.rect.x, self.rect.y + self.speed)
        elif self.direction == 'l':
            new_pos = (self.rect.x - self.speed, self.rect.y)
        elif self.direction == 'r':
            new_pos = (self.rect.x + self.speed, self.rect.y)

        enemy_rect = pygame.Rect(new_pos, [64, 64])

        if enemy_rect.collidelist(list(bullet_player_group)) != -1:
            for bullet in bullet_player_group:
                if pygame.sprite.collide_rect(self, bullet):
                    bullet.boom()
            self.hp -= 1

        if self.hp == 0:
            self.kill()

            # collisions with others object
        if enemy_rect.collidelist(list(collide_group)) != -1:
            return
        if enemy_rect.collidelist(list(player_group)) != -1:
            return
        for enemy in enemy_group:
            if self != enemy and enemy_rect.colliderect(enemy.rect):
                return

        # if no collision, move player
        self.rect.topleft = (new_pos)
        self.step_count -= 1

    def movement_control(self):
        direction_list = ['u', 'd', 'l', 'r']
        step_count = randint(1, 6)
        direction = choice(direction_list)
        return step_count, direction

    def rotate(self):
        self.image = enemy_images[self.type][self.type + '_' + self.direction]


class Bullet(pygame.sprite.Sprite):
    bullet_images = {'u': pygame.image.load('data/other/bullet_up.png'),
                     'd': pygame.image.load('data/other/bullet_down.png'),
                     'l': pygame.image.load('data/other/bullet_left.png'),
                     'r': pygame.image.load('data/other/bullet_right.png')}
    boom_images = [pygame.image.load('data/other/boom_1.png'),
                   pygame.image.load('data/other/boom_2.png'),
                   pygame.image.load('data/other/boom_3.png')]

    def __init__(self, type_1, owner):
        super().__init__(all_sprites)

        self.direction = owner.direction
        self.image = Bullet.bullet_images[self.direction]
        if type(owner) == Player:
            bullet_player_group.add(self)
        elif type(owner) == Enemy:
            bullet_enemy_group.add(self)

        if self.direction == 'u':
            self.rect = self.image.get_rect().move(
                owner.rect.x + tile_height * 0.5 - 4, owner.rect.y + 16)
        elif self.direction == 'd':
            self.rect = self.image.get_rect().move(
                owner.rect.x + tile_height * 0.5 - 4,
                owner.rect.y + tile_width - 16)
        elif self.direction == 'l':
            self.rect = self.image.get_rect().move(owner.rect.x + 16,
                                                   owner.rect.y + tile_width * 0.5 - 4)
        elif self.direction == 'r':
            self.rect = self.image.get_rect().move(
                owner.rect.x + tile_height - 16,
                owner.rect.y + tile_width * 0.5 - 4)

        if type == 'fast':
            self.speed = 24
        else:
            self.speed = 18

    def update(self):
        if pygame.sprite.spritecollideany(self, collide_group):
            self.boom()
        else:
            if self.direction == 'u':
                self.rect = self.rect.move(0, -self.speed)
            elif self.direction == 'd':
                self.rect = self.rect.move(0, self.speed)
            elif self.direction == 'l':
                self.rect = self.rect.move(-self.speed, 0)
            elif self.direction == 'r':
                self.rect = self.rect.move(self.speed, 0)

    def boom(self):
        Boom(self.rect.x, self.rect.y, self.direction)
        self.kill()


class Boom(pygame.sprite.Sprite):
    boom_images = [pygame.image.load('data/other/boom_1.png'),
                   pygame.image.load('data/other/boom_2.png'),
                   pygame.image.load('data/other/boom_3.png')]

    def __init__(self, posx, posy, direction):
        super().__init__(boom_group)
        self.boom = 0
        self.image = Boom.boom_images[self.boom]
        self.direction = direction
        if self.direction == 'u':
            self.rect = self.image.get_rect().move(
                posx - tile_height * 0.5 + 4, posy - 16)
        elif self.direction == 'd':
            self.rect = self.image.get_rect().move(
                posx - tile_height * 0.5 + 4,
                posy - tile_width + 16)
        elif self.direction == 'l':
            self.rect = self.image.get_rect().move(posx - 16,
                                                   posy - tile_width * 0.5 + 4)
        elif self.direction == 'r':
            self.rect = self.image.get_rect().move(
                posx - tile_height + 16,
                posy - tile_width * 0.5 + 4)

    def update(self):
        if self.boom == 0:
            self.boom = 1
            self.image = Bullet.boom_images[self.boom]
        elif self.boom == 1:
            self.boom = 2
            self.image = Bullet.boom_images[self.boom]
            self.kill()
