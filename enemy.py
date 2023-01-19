import pygame
from settings import *
from mechanics import MECHANICS


class ENEMY(MECHANICS):
    def __init__(self, type, pos, groups, obs_sprites, damage_player, trigger_death_particles):
        super().__init__(groups)

        self.sprite_type = 'enemy'
        self.obs_sprites = obs_sprites
 

        # data
        self.data = ENEMY_DATA
        self.type = type

        self.current_health = self.data[type]['health']
        self.max_health = self.data[type]['health']

        self.speed = self.data[type]['speed']
        self.exp = self.data[type]['exp']
        self.damage = self.data[type]['damage']
        self.attack_type = self.data[type]['attack_type']
        self.attack_sound = self.data[type]['attack_sound']
        self.attack_radius = self.data[type]['attack_radius']
        self.notice_radius = self.data[type]['notice_radius']
        self.resistance = self.data[type]['resistance']


        # animate
        self.import_all_graphics('enemy', type)
        self.state = 'idle'

        self.image = self.animations_data[self.state][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(HITBOX['enemy'][type])


        # attack
        self.attackable = True
        self.attackable_cooldown = self.data[type]['attackable_cooldown']
        self.damage_player = damage_player


        # being able to be attacked
        self.vulnerable = True
        self.invincibility_duration = INVINCIBILITY_DURATION['enemy']


        self.trigger_death_particles = trigger_death_particles


        # audio
        self.sound_path = self.data[type]['attack_sound']

        self.attack_sound = pygame.mixer.Sound(self.sound_path)
        self.die_sound = pygame.mixer.Sound(AUDIO_DATA['enemy_die'])
        self.boss_die_sound = pygame.mixer.Sound(AUDIO_DATA['boss_die'])


    def get_player_distance_direction(self, player):
        enemey_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)

        distance = (player_vec - enemey_vec).magnitude()    # vector to distance

        if distance > 0:
            direction = (player_vec - enemey_vec).normalize()   # avoid moving fast
        else:
            direction = pygame.math.Vector2()

        return(distance, direction) 
    

    def AI(self, player):
        distance = self.get_player_distance_direction(player)[0]
        if distance <= self.attack_radius and self.attackable:   
            if self.state != 'attack':
                self.frame_index = 0
                self.state = 'attack'

        elif distance <= self.notice_radius:    self.state = 'move'
        else:   self.state = 'idle'


        # raccoon notice and attack
        if self.type == 'raccoon':
            player_pos_x = player.rect.centerx
            player_pos_y = player.rect.centery

            if distance <= self.attack_radius and self.attackable:  
                if self.state != 'attack': 
                    self.frame_index = 0
                    self.state = 'attack'

            elif 1435 <= player_pos_x <= 2535 and 80 <= player_pos_y <= 630:  
                self.state = 'move'

            elif 2075 <= player_pos_x <= 3235 and 2505 <= player_pos_y <= 3055:  
                self.state = 'move'

            # player in territory can get damaged and reset when out
            else:   self.current_health = self.data['raccoon']['health']

    def animate(self):
        self.frame_index += self.animation_speed
        animation_list = self.animations_data[self.state]
        
        if self.frame_index >= len(animation_list):
            if self.state == 'attack':  self.attackable = False
            
            self.frame_index = 0

        self.image = animation_list[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)


    def action(self, player):
        if self.state == 'attack': 
            self.attack_sound.play() 
            self.damage_player(self.damage * (100 - player.free_harm)/100, self.attack_type)

        elif self.state == 'move':  self.direction = self.get_player_distance_direction(player)[1]
        else:   self.direction = pygame.math.Vector2()


    def cooldowns(self):
        if not self.attackable:
            self.attackable_cooldown -= 1
            if self.attackable_cooldown <= 0:
                self.attackable = True
                self.attackable_cooldown = self.data[self.type]['attackable_cooldown']
        
        if not self.vulnerable:
            self.invincibility_duration -= 1
            if self.invincibility_duration <= 0:
                self.vulnerable = True
                self.invincibility_duration = INVINCIBILITY_DURATION['enemy']


    def get_damaged(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]

            if attack_type == 'weapon':
                self.current_health -= player.total_damage('weapon')
            else:
                self.current_health -= player.total_damage('magic')
            self.vulnerable = False


    def check_death(self, player):
        if self.current_health <= 0:
            if self.type == 'raccoon':  self.boss_die_sound.play()
            else:   self.die_sound.play()
            
            self.kill()
            self.trigger_death_particles(self.type, self.rect.center)
            player.current_exp += self.exp
                

    def hit_reaction(self):
        if not self.vulnerable: 
            self.direction *= -self.resistance

        self.blink(self.image, self.vulnerable)
   

    def update(self):
        self.hit_reaction()
        self.animate()
        self.cooldowns()
        self.move(self.speed)
     
           
    def enemy_update(self, player):
        self.AI(player)
        self.action(player)
        self.check_death(player)
    