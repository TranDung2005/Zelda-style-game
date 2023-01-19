import pygame
from math import sin
from support import import_imgs_list


class MECHANICS(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()
 
    
    def import_all_graphics(self, type, enemy_type=None):
        if type == 'player':
            self.animations_data = {'up': [],'down': [],'left': [],'right': [],
            'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
            'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]
            }
            path = f'graphics/player/'
        
        else:
            self.animations_data = {'idle':[], 'move':[], 'attack':[]}
            path = f'graphics/enemies/{enemy_type}/'

        for animation in self.animations_data:
            self.animations_data[animation] = import_imgs_list(path + animation)


    def check_collide(self, moving_direction):
        for obs_sprite in self.obs_sprites:
            if obs_sprite.hitbox.colliderect(self.hitbox):
                
                if moving_direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox.right = obs_sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = obs_sprite.hitbox.right

                if moving_direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox.bottom = obs_sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = obs_sprite.hitbox.bottom

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

            self.hitbox.x += self.direction.x * speed
            self.check_collide('horizontal')
            self.hitbox.y += self.direction.y * speed
            self.check_collide('vertical')

            self.rect.center = self.hitbox.center


    def wave(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:  return(255)
        else:   return(0)

    def blink(self, image, vulnerable):
        value = self.wave()
        if not vulnerable:  image = image.set_alpha(value)
        else:   image = image.set_alpha(255)

