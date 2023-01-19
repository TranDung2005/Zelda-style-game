import pygame
from settings import *
from ui import UI


class START(UI):
    def __init__(self):
        super().__init__()

        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE['header'])
        self.current_pos = SCR_HEIGHT*1/4

        self.bg_img = pygame.image.load("graphics/screen/bg_start_scr.png").convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (SCR_WIDTH,SCR_HEIGHT))
        self.bg_rect = self.bg_img.get_rect(topleft=(0,0))

        self.logo_surf = pygame.image.load("graphics/screen/logo.png").convert_alpha()
        self.logo_surf = pygame.transform.scale(self.logo_surf, (SCR_WIDTH//3,SCR_HEIGHT//3))
        

    def logo(self, centerx, centery):
        self.pop_up(self.logo_surf)

        y_oscillate = self.oscillate(centery)
        self.logo_rect = self.logo_surf.get_rect(center=(centerx,y_oscillate))

        self.display_surface.blit(self.logo_surf, self.logo_rect)


    def display(self):
        self.display_surface.blit(self.bg_img, self.bg_rect)

        self.logo(SCR_WIDTH*3/4, SCR_HEIGHT*1/4)
        self.write('play --p--', (SCR_WIDTH*3/4, SCR_HEIGHT*1/4 + 150), blink=True)



class UPGRADE(UI):
    def __init__(self, player):
        super().__init__()

        self.player = player
        self.current_pos = SCR_HEIGHT // 5


        # datum
        self.magic_upgrade_data = UPGRADE_DATA['magic']
        self.weapon_upgrade_data = UPGRADE_DATA['weapon']
        self.weapon_data = WEAPON_DATA
        self.magic_data = MAGIC_DATA

        self.import_level_data('weapon')
        self.import_level_data('magic')

        self.weapon_images_list = self.import_all_graphics(self.weapon_data, True)
        self.magic_images_list = self.import_all_graphics(self.magic_data, True)


        # selected
        self.weapon_box_selected = True
        self.magic_box_selected = False


        # upgrade
        self.upgrade_avalable = True
        self.upgrade_cooldown = SWITCH_COOLDOWN

        
        # weapon
        self.weapon_index = 0
        self.weapon_kind = list(self.weapon_data)[self.weapon_index]

        self.weapon_cost = self.weapon_upgrade_data['cost']
        self.weapon_damage_upgrade = self.weapon_upgrade_data['damage']
            
        # magic
        self.magic_index = 0
        self.magic_kind = list(self.magic_data)[self.magic_index]

        self.magic_cost = self.magic_upgrade_data[self.magic_kind]['cost']
        self.magic_strength_upgrade = self.magic_upgrade_data[self.magic_kind]['strength']

        self.free_harm_upgrade = self.magic_upgrade_data['heal']['free_harm']
        self.hand_damage_upgrade = self.magic_upgrade_data['flame']['hand_damage']


        # switching
        self.weapon_switch_avalable = True
        self.weapon_SWITCH_COOLDOWN = SWITCH_COOLDOWN

        self.magic_switch_avalable = True
        self.magic_SWITCH_COOLDOWN = SWITCH_COOLDOWN

        
        # audio
        self.upgrade_sound = pygame.mixer.Sound(AUDIO_DATA['upgrade'])
        self.switch_sound = pygame.mixer.Sound(AUDIO_DATA['switch'])
        self.select_sound = pygame.mixer.Sound(AUDIO_DATA['select'])
        self.out_sound = pygame.mixer.Sound(AUDIO_DATA['out'])
    

    def import_level_data(self, type):
        if type == 'weapon':    
            self.weapon_level_data = {'sword':[], 'lance':[], 'axe':[], 'rapier':[], 'sai':[]}
            for level in self.weapon_level_data:
                self.weapon_level_data[level] = 1

        else:   
            self.magic_level_data = {'heal':[], 'flame':[]}
            for level in self.magic_level_data:
                self.magic_level_data[level] = 1


    def upgrade_mechanics(self):
        if self.weapon_box_selected:
            if self.player.current_exp >= self.weapon_cost:
                self.upgrade_sound.play()
                self.player.current_exp -= self.weapon_cost

                self.weapon_level_data[self.weapon_kind] += 1
                self.weapon_data[self.weapon_kind]['damage'] += self.weapon_damage_upgrade

            else:   self.out_sound.play()

        if self.magic_box_selected:
            if self.player.current_exp >= self.magic_cost:
                self.upgrade_sound.play()
                self.player.current_exp -= self.magic_cost

                self.magic_level_data[self.magic_kind] += 1
                self.magic_data[self.magic_kind]['strength'] += self.magic_strength_upgrade

                if self.magic_kind == 'heal':   self.player.free_harm += self.free_harm_upgrade
                else:   self.player.hand_damage += self.hand_damage_upgrade

            else:   self.out_sound.play()


    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_q]:
            self.switch_sound.stop()
            self.switch_sound.play()

            if self.weapon_box_selected and self.weapon_switch_avalable:
                if self.weapon_index < len(self.weapon_data) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
            
                self.weapon_kind = list(self.weapon_data.keys())[self.weapon_index]
                self.weapon_cost = self.weapon_upgrade_data['cost']
                self.weapon_switch_avalable = False   
                
            if self.magic_box_selected and self.magic_switch_avalable:
                if self.magic_index < len(self.magic_data) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0
            
                self.magic_kind = list(self.magic_data.keys())[self.magic_index]
                self.magic_cost = self.magic_upgrade_data[self.magic_kind]['cost']
                self.magic_switch_avalable = False 


        if keys[pygame.K_LEFT]:
            self.select_sound.stop()
            self.select_sound.play()
            self.weapon_box_selected = True
            self.magic_box_selected  = False
        if keys[pygame.K_RIGHT]:
            self.select_sound.stop()
            self.select_sound.play()
            self.weapon_box_selected = False
            self.magic_box_selected = True


        if keys[pygame.K_u] and self.upgrade_avalable:
            self.upgrade_mechanics()
            self.upgrade_avalable = False


    def weapon_magic_choice_box(self, type, center_pos, weapon_magic_index, has_switched=None):
        y_move = self.oscillate(SCR_HEIGHT // 5, 15)
        y_offset = pygame.math.Vector2(0,10)

        box_rect =  self.creat_box('selection', center_pos, BOX_SIZE['upgrade_choice'], has_switched)

        if type == 'weapon':
            image = self.weapon_images_list[weapon_magic_index]

            if self.weapon_box_selected:    y = y_move
            else:   y = SCR_HEIGHT // 5

            self.write('weapon', (box_rect.midtop[0], y))

            level = self.weapon_level_data[self.weapon_kind]
            self.write(f'{self.weapon_kind} lv.{level} exp.{self.weapon_cost}', box_rect.midbottom+y_offset)


        else:
            image = self.magic_images_list[weapon_magic_index]

            if self.magic_box_selected:    y = y_move
            else:   y = SCR_HEIGHT // 5

            self.write('magic', (box_rect.midtop[0], y))

            level = self.magic_level_data[self.magic_kind]
            self.write(f'{self.magic_kind} lv.{level} exp.{self.magic_cost}', box_rect.midbottom+y_offset)


        rect = image.get_rect(center = box_rect.center)
        self.display_surface.blit(image, rect)


    def upgrade_box(self):
        box_rect = self.creat_box('selection', (SCR_WIDTH//2,SCR_HEIGHT*5/6), BOX_SIZE['upgrade_button'], self.upgrade_avalable)
        self.write('upgrade--u--', box_rect.center-pygame.math.Vector2(0,10))


    def cooldowns(self):
        if not self.weapon_switch_avalable:
            self.weapon_SWITCH_COOLDOWN -= 1
            if self.weapon_SWITCH_COOLDOWN <= 0:
                self.weapon_switch_avalable = True
                self.weapon_SWITCH_COOLDOWN = SWITCH_COOLDOWN

        if not self.magic_switch_avalable:
            self.magic_SWITCH_COOLDOWN -= 1
            if self.magic_SWITCH_COOLDOWN <= 0:
                self.magic_switch_avalable = True
                self.magic_SWITCH_COOLDOWN = SWITCH_COOLDOWN

        if not self.upgrade_avalable:
            self.upgrade_cooldown -= 1
            if self.upgrade_cooldown <= 0:
                self.upgrade_avalable = True
                self.upgrade_cooldown = SWITCH_COOLDOWN

    def display(self):
        self.input()
        self.cooldowns()
        self.display_surface.fill(UPGRADE_BG_COLOR)

        self.player_exp_box((SCR_WIDTH//2, 100), self.player.current_exp)

        self.weapon_magic_choice_box('weapon', (SCR_WIDTH*1/4, SCR_HEIGHT//2), 
                                self.weapon_index, not self.weapon_box_selected)
        self.weapon_magic_choice_box('magic', (SCR_WIDTH*3/4, SCR_HEIGHT//2), 
                                self.magic_index, not self.magic_box_selected)

        self.upgrade_box()



class END(UI):
    def __init__(self):
        super().__init__()

        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE['header'])
        self.blink_speed = 5
        self.current_pos = SCR_HEIGHT*2/5
      
        # background
        self.bg_img = pygame.image.load("graphics/screen/bg_end_scr.png").convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (SCR_WIDTH,SCR_HEIGHT))
       
        # logo
        self.logo_surf = pygame.image.load("graphics/screen/end_logo.png").convert_alpha()
        self.logo_surf = pygame.transform.scale(self.logo_surf, (150,250))
 

    def logo(self, centerx, centery):
        self.pop_up(self.logo_surf)
        y_oscillate = self.oscillate(centery)

        self.logo_rect = self.logo_surf.get_rect(center=(centerx, y_oscillate))
        self.display_surface.blit(self.logo_surf, self.logo_rect)


    def display(self):
        self.pop_up(self.bg_img)
        self.bg_rect = self.bg_img.get_rect(topleft=(0,0))
        self.display_surface.blit(self.bg_img, self.bg_rect)
        
        if self.value >= 255:
            self.logo(SCR_WIDTH*2/5, SCR_HEIGHT*2/5)

            self.write('game over', (SCR_WIDTH//2+70, SCR_HEIGHT*2/5), pop_up=True)
            self.write('replay --r--', (SCR_WIDTH//2,SCR_HEIGHT*4/5), blink=True)
            self.write('quit --q--', (SCR_WIDTH//2,SCR_HEIGHT*4/5) + pygame.math.Vector2(0,50), blink=True)