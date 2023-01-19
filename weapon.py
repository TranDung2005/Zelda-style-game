import pygame

class WEAPON(pygame.sprite.Sprite):
    def __init__(self, type, player, groups):
        super().__init__(groups)

        self.sprite_type = type
        player_direction = player.state.split('_')[0]
        
        horizontal_offset = pygame.math.Vector2(-12,0)
        vertical_offset = pygame.math.Vector2(0,16)

        path = f'graphics\weapons\{player.weapon_kind}\{player_direction}.png'
        self.image = pygame.image.load(path)

        if player_direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + vertical_offset)
        elif player_direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + vertical_offset)
        elif player_direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + horizontal_offset)
        else:
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + horizontal_offset)
      
        