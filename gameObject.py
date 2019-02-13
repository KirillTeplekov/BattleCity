import pygame
from main import *
from random import choice, randint

pygame.mixer.init()

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
bonus_group = pygame.sprite.Group()
boom_group = pygame.sprite.Group()
shield_group = pygame.sprite.Group()

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
               'bushes': load_image('tiles/bushes.png')}

player_images = {'lvl1_u': load_image(path_to_player + 'lvl1/up.png'),
                 'lvl1_d': load_image(path_to_player + 'lvl1/down.png'),
                 'lvl1_l': load_image(path_to_player + 'lvl1/left.png'),
                 'lvl1_r': load_image(path_to_player + 'lvl1/right.png'),
                 'lvl2_u': load_image(path_to_player + 'lvl2/up.png'),
                 'lvl2_d': load_image(path_to_player + 'lvl2/down.png'),
                 'lvl2_l': load_image(path_to_player + 'lvl2/left.png'),
                 'lvl2_r': load_image(path_to_player + 'lvl2/right.png'),
                 'lvl3_u': load_image(path_to_player + 'lvl3/up.png'),
                 'lvl3_d': load_image(path_to_player + 'lvl3/down.png'),
                 'lvl3_l': load_image(path_to_player + 'lvl3/left.png'),
                 'lvl3_r': load_image(path_to_player + 'lvl3/right.png')}

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
                        path_to_enemy + 'standard/right.png')},
                'standard_bonus': {'bonus_u': load_image(
                    path_to_enemy + 'standard/bonus_up.png'),
                    'bonus_d': load_image(
                        path_to_enemy + 'standard/bonus_down.png'),
                    'bonus_l': load_image(
                        path_to_enemy + 'standard/bonus_left.png'),
                    'bonus_r': load_image(
                        path_to_enemy + 'standard/bonus_right.png')}}


# Game's board border
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


# Castle's flag
class Flag(Tile):
    flag_on = load_image('other/flag_on.png')
    flag_off = load_image('other/flag_off.png')

    def __init__(self, posx, posy):
        super().__init__(Flag.flag_on, posx, posy, collide_group)
        self.state = 'on'

    def update(self):
        if pygame.sprite.spritecollideany(self, bullet_group):
            self.image = Flag.flag_off
            self.state = 'off'


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


class Bonus(Tile):
    bonus_images = {'helmet': load_image('other/bonus/helmet.png'),
                    'tank': load_image('other/bonus/tank.png'),
                    'star': load_image('other/bonus/star.png'),
                    'grenade': load_image('other/bonus/grenade.png')}

    def __init__(self, posx, posy):
        bonus = ['helmet', 'tank', 'star', 'grenade']
        self.bonus_type = choice(bonus)
        super().__init__(Bonus.bonus_images[self.bonus_type],
                         (posx - x_indent) // tile_width,
                         (posy - y_indent) // tile_height,
                         bonus_group)

    def update(self, player):
        if pygame.sprite.spritecollideany(self, player_group):
            bonus.play()
            if self.bonus_type == 'helmet':
                player.shield = True
                Shield(player)
            if self.bonus_type == 'tank':
                player.hp += 1
            if self.bonus_type == 'star':
                player.lvl += 1
            if self.bonus_type == 'grenade':
                for enemy in enemy_group:
                    enemy.kill()
            self.kill()


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
        super().__init__(player_images['lvl1_u'], posx, posy)
        # Main parametres
        self.hp = 3
        self.lvl = 1
        self.speed = 8
        self.damage = 1
        self.bullet_type = 'standard'
        self.atack_count = 30
        self.direction = 'u'

        # Flag for handler of a user's action
        self.atack = False
        self.movement = False

        # For shield
        self.shield = True
        self.shield_timer = 0
        Shield(self)

        self.add(player_group)

    def update(self):
        if self.shield_timer == 60:
            self.shield = False
            self.shield_timer = 0
            shield_group.empty()

        if self.shield:
            self.shield_timer += 1

        if pygame.sprite.spritecollideany(self, bullet_enemy_group):
            for bullet in bullet_enemy_group:
                if pygame.sprite.collide_rect(self, bullet):
                    if self.shield:
                        self.shield = False
                    else:
                        self.rect.topleft = (
                        5 * tile_width + x_indent, 12 * tile_height + y_indent)
                        self.hp -= 1
                    bullet.boom()
        if self.hp == 0:
            self.kill()

        if self.atack and self.atack_count >= 30:
            bullet = Bullet(self.bullet_type, self)
            self.atack_count = 0
        self.atack_count += 1

        move_pos = (0, 0)
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

            # collisions with game's object
            if player_rect.collidelist(list(collide_group)) != -1:
                return
            if player_rect.collidelist(list(enemy_group)) != -1:
                return
            if player_rect.collidelist(list(water_group)) != -1:
                return

            # if no collision, move player
            self.rect.topleft = (new_pos)

    def rotate(self):
        self.image = player_images[
            'lvl' + str(self.lvl) + '_' + self.direction]


class Enemy(Tanks):
    hp = {'btr': 1, 'rapidfire': 1, 'standard': 1, 'heavy': 4}
    speed = {'btr': 12, 'rapidfire': 8, 'standard': 8, 'heavy': 8}
    bullet_speed = {'btr': 'standard', 'rapidfire': 'fast',
                    'standard': 'standard', 'heavy': 'standard'}
    spawn_place = [(0, 0), (7, 0), (12, 0)]

    def __init__(self, type, bonus=False):
        self.type = type
        self.bonus = bonus
        self.direction = choice(DIRECTION)
        self.image = enemy_images[type][type + '_' + self.direction]
        posx, posy = choice(Enemy.spawn_place)
        super().__init__(self.image, posx, posy)
        self.hp = Enemy.hp[type]
        self.speed = Enemy.speed[type]
        self.bullet_speed = Enemy.bullet_speed[type]
        self.add(enemy_group)
        self.flash = 0
        self.step_count = 0
        self.atack_count = 30

    def update(self):
        if pygame.sprite.spritecollideany(self, bullet_player_group):
            for bullet in bullet_player_group:
                if pygame.sprite.collide_rect(self, bullet):
                    bullet.boom()
                    if self.bonus:
                        Bonus(self.rect.x, self.rect.y)
            self.hp -= 1
        if self.hp == 0:
            explosion.play()
            self.kill()

        if self.step_count == 0:
            self.step_count, self.direction = self.movement_control()
            self.rotate()

        if self.bonus:
            if self.flash < 3:
                self.image = enemy_images[self.type + '_bonus'][
                    'bonus_' + self.direction]
                self.flash += 1
            elif self.flash < 6:
                self.image = enemy_images[self.type][
                    self.type + '_' + self.direction]
                self.flash += 1
            else:
                self.flash = 0

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

        # collisions with others object
        if enemy_rect.collidelist(list(collide_group)) != -1:
            print(self.direction)
            print(self.step_count)
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
    bullet_images = {'u': load_image('other/bullet_up.png'),
                     'd': load_image('other/bullet_down.png'),
                     'l': load_image('other/bullet_left.png'),
                     'r': load_image('other/bullet_right.png')}

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
            brick.play()
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
    boom_images = [load_image('other/boom_1.png'),
                   load_image('other/boom_2.png'),
                   load_image('other/boom_3.png')]

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
            self.image = Boom.boom_images[self.boom]
        elif self.boom == 1:
            self.boom = 2
            self.image = Boom.boom_images[self.boom]
            self.kill()


class Shield(pygame.sprite.Sprite):
    shield_1 = load_image('other/shield_1.png')
    shield_2 = load_image('other/shield_2.png')

    def __init__(self, owner):
        super().__init__(shield_group)
        self.owner = owner
        self.image = Shield.shield_1
        self.rect = self.image.get_rect().move(self.owner.rect.x,
                                               self.owner.rect.y)

    def update(self):
        self.rect.topleft = self.owner.rect.topleft
        if (self.owner.shield_timer % 4) <= 1:
            self.image = Shield.shield_1
        else:
            self.image = Shield.shield_2
