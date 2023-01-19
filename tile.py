import pygame
from settings import TILESIZE, HITBOX

class TILE(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, image_type = pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groups)

        self.sprite_type = sprite_type
        self.image = image_type


        if self.sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]-TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)

        self.hitbox = self.rect.inflate(HITBOX[self.sprite_type])
        
        