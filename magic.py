import pygame
from settings import TILESIZE, AUDIO_DATA
from random import randint

class MAGIC:
    def __init__(self, player, particles_animation):
        
        self.player = player
        self.particles_animation = particles_animation
        
        self.heal_sound = pygame.mixer.Sound(AUDIO_DATA['heal'])
        self.fire_sound = pygame.mixer.Sound(AUDIO_DATA['fire'])
        self.out_sound = pygame.mixer.Sound(AUDIO_DATA['out'])

    def heal(self, strength, mana_spend, groups):
        if self.player.current_mana >= mana_spend:
            self.heal_sound.play()
            self.player.current_mana -= mana_spend
            self.player.current_health += strength

            self.particles_animation.create_particles('heal', self.player.rect.center, groups)
            self.particles_animation.create_particles('aura', self.player.rect.center, groups)
         
            if self.player.current_health >= self.player.max_health:
                self.player.current_health = self.player.max_health
        
        else:   self.out_sound.play()

    def flame(self, mana_spend, groups):
        if self.player.current_mana >= mana_spend:
            self.fire_sound.play()
            self.player.current_mana -= mana_spend

            player_state = self.player.state.split('_')[0]
            if player_state == 'up':
                dicrection = pygame.math.Vector2(0,-1)
            elif player_state == 'down':
                dicrection = pygame.math.Vector2(0,1)
            elif player_state == 'right':
                dicrection = pygame.math.Vector2(1,0)
            else:
                dicrection = pygame.math.Vector2(-1,0)
        
            for spawn_time in range(1,6):
                if dicrection.x:
                    offset_x = (dicrection.x * spawn_time) * TILESIZE
                    x = self.player.rect.centerx + offset_x + randint(-TILESIZE//3,TILESIZE//3)
                    y = self.player.rect.centery + randint(-TILESIZE//3, TILESIZE//3)
                    self.particles_animation.create_particles('flame', (x,y), groups)
                else:
                    offset_y = (dicrection.y * spawn_time) * TILESIZE
                    x = self.player.rect.centerx + randint(-TILESIZE//3, TILESIZE//3)
                    y = self.player.rect.centery + offset_y + randint(-TILESIZE//3, TILESIZE//3)
                    self.particles_animation.create_particles('flame', (x,y), groups)

        else:   self.out_sound.play()