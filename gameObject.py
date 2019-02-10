import pygame

# Game's group
all_sprites = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
uncollide_group = pygame.sprite.Group()
collide_group = pygame.sprite.Group()
ice_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
bushes_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

# path
path_to_player = 'tanks/player/'
path_to_enemy = 'tanks/enemy/'

# Tile size
tile_width = 64
tile_height = 64

# Indented for objects that game were indented at the edges as in the original 
x_indent = 32
y_indent = 32


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(collide_group)
        if x1 == x2:
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)

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


class Bushes(Tile):
    pass


# Tanks
class Tanks(pygame.sprite.Sprite):
    def __init__(self, image, posx, posy):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect().move(tile_width * posx + x_indent,
                                               tile_height * posy + y_indent)

        self.direction = ''  # 'u' - up, 'd' - down, 'l' - left, 'r' - r
        self.stop = ''  # The direction in which it is forbidden to go


class Enemy(Tanks):
    def __init__(self, type, posx, posy):
        super().__init__(None, posx, posy, enemy_group)
        pass


class Bullet(pygame.sprite.Sprite):
    bullet_images = {'u': pygame.image.load('data/other/bullet_up.png'),
                     'd': pygame.image.load('data/other/bullet_down.png'),
                     'l': pygame.image.load('data/other/bullet_left.png'),
                     'r': pygame.image.load('data/other/bullet_right.png')}
    boom_images = [pygame.image.load('data/other/boom_1.png'),
                   pygame.image.load('data/other/boom_2.png'),
                   pygame.image.load('data/other/boom_3.png')]

    def __init__(self, type, owner):
        super().__init__(bullet_group)

        self.direction = owner.direction
        self.image = Bullet.bullet_images[self.direction]

        self.boom = 0

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
            self.image = Bullet.boom_images[self.boom]

            if self.direction == 'u':
                self.rect = self.image.get_rect().move(
                    self.rect.x - tile_height * 0.5 + 4, self.rect.y - 16)
            elif self.direction == 'd':
                self.rect = self.image.get_rect().move(
                    self.rect.x - tile_height * 0.5 + 4,
                    self.rect.y - tile_width + 16)
            elif self.direction == 'l':
                self.rect = self.image.get_rect().move(self.rect.x - 16,
                                                       self.rect.y - tile_width * 0.5 + 4)
            elif self.direction == 'r':
                self.rect = self.image.get_rect().move(
                    self.rect.x - tile_height + 16,
                    self.rect.y - tile_width * 0.5 + 4)

            if self.boom == 0:
                self.boom = 1
                self.image = Bullet.boom_images[self.boom]
            elif self.boom == 1:
                self.boom = 2
                self.image = Bullet.boom_images[self.boom]
                self.kill()
        elif self.boom == 0:
            if self.direction == 'u':
                self.rect = self.rect.move(0, -self.speed)
            elif self.direction == 'd':
                self.rect = self.rect.move(0, self.speed)
            elif self.direction == 'l':
                self.rect = self.rect.move(-self.speed, 0)
            elif self.direction == 'r':
                self.rect = self.rect.move(self.speed, 0)