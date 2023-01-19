import pygame
from settings import *
from player import PLAYER
from support import *
from tile import TILE
from random import choice, randint
from weapon import WEAPON
from enemy import ENEMY
from particles import PARTICLE_ANIMATION
from magic import MAGIC
from screen import *


class CAMERA_GROUP(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2()
        
        # background
        self.floor_image = pygame.image.load("graphics/tilemap/ground.png").convert()
        self.floor_rect = self.floor_image.get_rect(topleft=(0,0))
        
    def camera_move(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_image, floor_offset_pos)
        
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)


    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() 
                        if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)


class OPERATION:
    def __init__(self):
        
        self.visible_sprites = CAMERA_GROUP()
        self.obs_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.create_map()

        self.current_attack = None

        self.particles_animation = PARTICLE_ANIMATION()

        self.magic = MAGIC(self.player, self.particles_animation)


        self.game_play = False
        self.game_paused = False
        self.game_over = False

        self.start_scr = START()
        self.upgrade_scr = UPGRADE(self.player)
        self.end_scr = END()


        # audio
        self.start_sound = pygame.mixer.Sound(AUDIO_DATA['start'])
        self.play_sound = pygame.mixer.Sound(AUDIO_DATA['play'])
        self.end_sound = pygame.mixer.Sound(AUDIO_DATA['end'])
        self.paused_sound =  pygame.mixer.Sound(AUDIO_DATA['shop'])
        self.attack_air_sound = pygame.mixer.Sound(AUDIO_DATA['attack_air'])
        self.attack_grass_sound = pygame.mixer.Sound(AUDIO_DATA['attack_grass'])
        self.attack_enemy_sound = pygame.mixer.Sound(AUDIO_DATA['attack'])
        self.attack_enemy_sound.set_volume(0.2)

    def create_map(self):
        layout = {'boundary': import_csv_layout("map/map_FloorBlocks.csv"),
                  'grass': import_csv_layout("map/map_Grass.csv"),
                  'object': import_csv_layout("map/map_Objects.csv"),
                  'entity': import_csv_layout("map/map_Entities.csv")}

        image = {'grass': import_imgs_list("graphics/grass"),
                 'object': import_imgs_list("graphics/objects")}

        for type, layout in layout.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        if type == 'boundary':
                            TILE((x,y), [self.obs_sprites], 'boundary') 

                        if type == 'grass':
                            random_grass = choice(image['grass'])
                            TILE((x,y), [self.visible_sprites,self.obs_sprites,self.attackable_sprites], 
                                        'grass', random_grass)

                        if type == 'object':
                            object_seperate = image['object'][int(col)]
                            TILE((x,y), [self.visible_sprites,self.obs_sprites], 'object', object_seperate)
                        
                        if type == 'entity':
                            if col == '394':
                               self.player = PLAYER((x,y), [self.visible_sprites], self.obs_sprites, 
                                    self.create_attack, self.destroy_attack, self.create_magic)
                            else:

                                if col == '390':    enemy_type = 'bamboo'
                                elif col == '391':    enemy_type = 'spirit'
                                elif col == '392':    enemy_type = 'raccoon'
                                else:    enemy_type = 'squid'

                                self.enemy = ENEMY(enemy_type, (x,y), [self.visible_sprites,self.attackable_sprites], 
                                    self.obs_sprites, self.damage_player, self.trigger_death_particles)
                                                    
    def create_attack(self):
        self.attack_air_sound.play()
        self.current_attack = WEAPON('weapon', self.player, [self.visible_sprites,self.attack_sprites])

    def create_magic(self, type, strength, mana_spend):
        if type == 'heal':
            self.magic.heal(strength, mana_spend, [self.visible_sprites])
        elif type == 'flame':
            self.magic.flame(mana_spend, [self.visible_sprites, self.attack_sprites])


    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, 
                                        self.attackable_sprites, False)

                if collision_sprites:
                    self.attack_air_sound.stop()

                    for target_sprite in collision_sprites: 
                        if target_sprite.sprite_type == 'grass':
                            self.attack_grass_sound.play()
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf_num in range(randint(3, 6)):
                                self.particles_animation.create_particles('leaf', pos-offset, 
                                    [self.visible_sprites])
                            
                            target_sprite.kill()
                            self.player.current_exp += 1

                        else:
                            self.attack_enemy_sound.play()
                            target_sprite.get_damaged(self.player, attack_sprite.sprite_type)

                  
    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.current_health -= amount
            self.player.vulnerable = False
            self.particles_animation.create_particles(attack_type, 
                    self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, enemy_type, pos):
        self.particles_animation.create_particles(enemy_type, pos, [self.visible_sprites])

    
    def play(self):
        self.game_play = True
        self.game_paused = False
        self.game_over = False


    def paused(self):
        self.paused_sound.play()   # upgrade_scr_display
        self.game_paused = not self.game_paused

    def reset(self):
        self.end_sound.stop()
        self.start_sound.play(-1)

        return(OPERATION())
       

    def run(self):
        if not self.game_over:

            if not self.game_play:
                self.start_scr.display()

            if self.game_play:  
                self.visible_sprites.camera_move(self.player)
                
                if self.game_paused:    self.upgrade_scr.display()
                if not self.game_paused:
                    self.visible_sprites.update()
                    self.visible_sprites.enemy_update(self.player)
                    self.player_attack_logic()

                if self.player.has_death():
                    self.play_sound.stop()
                    self.end_sound.play(-1)
                    self.game_play = False
                    self.game_over = True

        if self.game_over:  
            self.visible_sprites.camera_move(self.player) 
            self.end_scr.display()


