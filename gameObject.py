import pygame

# Tile size
tile_width = 64
tile_height = 64

# Indented for objects that game were indented at the edges as in the original 
x_indent = 32
y_indent = 64

class Tile(pygame.sprite.Sprite):
    
    def __init__(self, type, posx, posy):
        super().__init__(tiles_group, all_sprites)
        self.image = Tile.tile_images[type]
        self.rect = self.image.get_rect().move(tile_width * posx + x_indent, tile_height * posy + y_indent)
        