import pygame
from settings import *
from ui import UI
from mechanics import MECHANICS


class PLAYER(MECHANICS):
    def __init__(self, pos, groups, obs_sprites, creat_weapon_attack, destroy_weapon_attack, creat_magic):
        super().__init__(groups)

        self.sprite_type = 'player'
        self.obs_sprites = obs_sprites


        # datum
        self.data = PLAYER_DATA
        self.weapon_data = WEAPON_DATA
        self.magic_data = MAGIC_DATA


        # player
        self.current_health = self.data['health']
        self.max_health = self.data['health'] 

        self.current_mana = self.data['mana'] 
        self.max_mana = self.data['mana']

        self.current_exp = self.data['exp']

        self.hand_damage = self.data['hand_damage']
        self.magic_hand_damage = self.data['magic_hand_damage']
        
        self.free_harm = self.data['free_harm']
        self.mana_auto_recovery_amount = self.data['mana_auto_recovery']
        self.speed = self.data['speed']


        # animate
        self.import_all_graphics('player')
        self.state = 'down'

        self.image = self.animations_data[self.state][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(HITBOX['player'])


        # weapon 
        self.weapon_index = 0
        self.weapon_kind = list(self.weapon_data)[self.weapon_index]
        self.weapon_weight = self.weapon_data[self.weapon_kind]['heavy']

        # magic 
        self.magic_index = 0
        self.magic_kind = list(self.magic_data)[self.magic_index]

        self.magic_strength = self.magic_data[self.magic_kind]['strength']
        self.magic_mana =  self.magic_data[self.magic_kind]['mana_spend']


        # attack
        self.attackable_cooldown = PLAYER_ATTACKABLE_COOLDOWN

        self.spawn_weapon_attack = False
        self.creat_weapon_attack = creat_weapon_attack
        self.destroy_weapon_attack = destroy_weapon_attack
        self.weapon_attackable_cooldown =  self.attackable_cooldown + self.weapon_data[self.weapon_kind]['cooldown']

        self.spawn_magic_attack = False
        self.creat_magic = creat_magic
        self.magic_attackable_cooldown =  self.attackable_cooldown + self.magic_data[self.magic_kind]['cooldown']


        # switching
        self.weapon_switch_avalable = True
        self.weapon_switch_cooldown = SWITCH_COOLDOWN

        self.magic_switch_avalable = True
        self.magic_switch_cooldown = SWITCH_COOLDOWN


        # being able to be attacked
        self.vulnerable = True
        self.invincibility_duration = INVINCIBILITY_DURATION['player'] 
        

        self.ui = UI()

        self.die_sound = pygame.mixer.Sound(AUDIO_DATA['player_die'])
        self.switch_weapon_sound = pygame.mixer.Sound(AUDIO_DATA['change_weapon'])
        self.switch_magic_sound = pygame.mixer.Sound(AUDIO_DATA['change_magic'])


    def ui_display(self):
        self.ui.player_health_bar(self.current_health, self.max_health)
        self.ui.player_mana_bar(self.current_mana, self.max_mana)

        self.ui.weapon_magic_choice_box('weapon',(50,SCR_HEIGHT-70), 
                                        self.weapon_index, self.weapon_switch_avalable)
        self.ui.weapon_magic_choice_box('magic', (115,SCR_HEIGHT-60), 
                                        self.magic_index, self.magic_switch_avalable)

        self.ui.player_exp_box((SCR_WIDTH-80,SCR_HEIGHT-50), self.current_exp)
        

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.spawn_weapon_attack and not self.spawn_magic_attack:
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.state = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.state = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.state = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.state = 'left'
            else:
                self.direction.x = 0


            # attack
            if keys[pygame.K_SPACE]:
                self.direction.x = 0
                self.direction.y = 0
                self.spawn_weapon_attack = True
                self.creat_weapon_attack()
                self.weapon_attackable_cooldown = self.attackable_cooldown + self.weapon_data[self.weapon_kind]['cooldown']
          
            # magic
            if keys[pygame.K_LALT]:
                self.direction.x = 0
                self.direction.y = 0
                self.spawn_magic_attack = True
                self.creat_magic(self.magic_kind, self.magic_strength, self.magic_mana)
                self.magic_attackable_cooldown = self.attackable_cooldown + self.magic_data[self.magic_kind]['cooldown']

     
            if keys[pygame.K_q] and self.weapon_switch_avalable:
                self.switch_weapon_sound.play()

                if self.weapon_index < len(self.weapon_data) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
            
                self.weapon_kind = list(self.weapon_data.keys())[self.weapon_index]
                self.weapon_weight = self.weapon_data[self.weapon_kind]['heavy']
                self.weapon_switch_avalable = False   
          
            if keys[pygame.K_e] and self.magic_switch_avalable:
                self.switch_magic_sound.play()
                if self.magic_index < len(self.magic_data) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0
            
                self.magic_kind = list(self.magic_data.keys())[self.magic_index]
                self.magic_switch_avalable = False 
     

    def get_state(self):
        if self.direction.x == self.direction.y == 0:
            if not 'idle' in self.state and not 'attack' in self.state:
                self.state += '_idle'

            if self.spawn_weapon_attack or self.spawn_magic_attack:
                if not 'attack' in self.state:
                    if 'idle' in self.state:
                        self.state = self.state.replace('_idle', '_attack')
                    else:
                        self.state += '_attack'

            elif 'attack' in self.state:
                self.state = self.state.replace('_attack', '')


    def animate(self):
        self.frame_index += self.animation_speed
        animation_list = self.animations_data[self.state]

        if self.frame_index >= len(animation_list):
            self.frame_index = 0

        self.image = animation_list[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
        
        # hit reaction
        self.blink(self.image, self.vulnerable)

      
    def cooldowns(self):
        if self.spawn_weapon_attack:
            self.weapon_attackable_cooldown -= 1
            if self.weapon_attackable_cooldown <= 0:
                self.destroy_weapon_attack()
                self.spawn_weapon_attack = False

        if self.spawn_magic_attack:
            self.magic_attackable_cooldown -= 1
            if self.magic_attackable_cooldown <= 0:
                self.spawn_magic_attack = False
            

        if not self.vulnerable:
            self.invincibility_duration -= 1
            if self.invincibility_duration <= 0:
                self.vulnerable = True
                self.invincibility_duration = INVINCIBILITY_DURATION['player']

        if not self.weapon_switch_avalable:
            self.weapon_switch_cooldown -= 1
            if self.weapon_switch_cooldown <= 0:
                self.weapon_switch_avalable = True
                self.weapon_switch_cooldown = SWITCH_COOLDOWN

        if not self.magic_switch_avalable:
            self.magic_switch_cooldown -= 1
            if self.magic_switch_cooldown <= 0:
                self.magic_switch_avalable = True
                self.magic_switch_cooldown = SWITCH_COOLDOWN


    def has_death(self):
        if self.current_health <= 0:
            self.die_sound.play()
            return(True)
  
    
    def mana_auto_recovery(self):
        if self.current_mana < self.max_mana:
            self.current_mana += self.mana_auto_recovery_amount


    def total_damage(self, type):
        if type == 'weapon':
            weapon_damage = self.weapon_data[self.weapon_kind]['damage'] + self.hand_damage
            return(weapon_damage)
        else:
            magic_damage = self.magic_data[self.magic_kind]['strength'] + self.magic_hand_damage
            return(magic_damage)


    def update(self):
        self.animate()
        self.cooldowns()
        self.input()
        self.get_state()
        self.move(self.speed - self.weapon_weight)
        self.mana_auto_recovery()
        self.ui_display()   
    