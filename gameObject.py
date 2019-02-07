import pygame

# Game's group
all_sprites = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
uncolide_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
colide_group = pygame.sprite.Group()

# Tile size
tile_width = 64
tile_height = 64

# Indented for objects that game were indented at the edges as in the original 
x_indent = 32
y_indent = 32

class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        self.add(colide_group)                
        if x1 == x2:
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)    

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, posx, posy, group):
        super().__init__(group, all_sprites)
        self.image = image
        self.rect = self.image.get_rect().move(tile_width * posx + x_indent, tile_height * posy + y_indent)

class Water(Tile):
    image_1 = pygame.image.load('tiles/water.png')
    image_2 = pygame.image.load('tiles/water_2.png')
    
    def __init__(self, posx, posy, group):
        super().__init__(Water.image_2, posx, posy, group)
        self.image_1 = Water.image_1
        self.image_2 = Water.image_2
        self.index = 0
        
    def update(self):
        if self.index == 0:
            self.image = self.image_1
            self.index = 1
        elif self.index == 1:
            self.image = self.image_2
            self.index = 0
            
class Tanks(pygame.sprite.Sprite):
    def __init__(self, image, posx, posy):
        super().__init__(tiles_group, all_sprites)
        self.image = image
        self.rect = self.image.get_rect().move(tile_width * posx + x_indent, tile_height * posy + y_indent)
        
        self.v = 0
        
        self.up = True
        self.down = False
        self.left = False
        self.right = False


class Enemy(Tanks):
    def __init__(self, type, posx, posy):
        super().__init__(type, posx, posy)
        pass
        