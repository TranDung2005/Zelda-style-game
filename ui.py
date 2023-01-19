import pygame
from settings import *

class UI():
    def __init__(self):
        
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE['write'])

    # text effect default
        self.movement_speed = 0.5
        self.blink_speed = 10
        # reset when replay
        self.current_value = 0
        self.value = 0

        # player, enemy
        self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH['player'],BAR_HEIGHT['player'])
        self.mana_bar_rect = pygame.Rect(10,35,MANA_BAR_WIDTH,BAR_HEIGHT['player'])

        self.enemy_bar_rect = pygame.Rect((2/4) * SCR_WIDTH,15,HEALTH_BAR_WIDTH['enemy'],BAR_HEIGHT['enemy'])
        
        # graphics
        self.weapon_images_list = self.import_all_graphics(WEAPON_DATA)
        self.magic_images_list = self.import_all_graphics(MAGIC_DATA)


    def import_all_graphics(self, data, scale=False):
        self.images_list = []
        for image in data.values():
            path = image['path']
            surf = pygame.image.load(path)

            if scale:   surf = pygame.transform.scale(surf, (250, 250))
            self.images_list.append(surf)

        return(self.images_list)


    # text effect
    def oscillate(self, pos, range=15):  # init current_pos when use oscillate
        self.current_pos += self.movement_speed
        if self.current_pos >= pos + range: self.movement_speed = - self.movement_speed
        if self.current_pos <= pos - range: self.movement_speed = - self.movement_speed

        self.pos_oscillate = self.current_pos
        return(self.pos_oscillate)

    def pop_up(self, surface, speed=1):
        if self.value  >= 255:   self.value = 255
        else:    self.value += speed
        return(surface.set_alpha(self.value))
    
    def blink(self, surface):
        self.current_value += self.blink_speed
        if self.current_value >= 255: self.blink_speed = - self.blink_speed
        if self.current_value <= 0: self.blink_speed = - self.blink_speed

        return(surface.set_alpha(self.current_value))

    def write(self, msg, midtop_pos, color='white', blink=False, pop_up=False):
        surf = self.font.render(str(msg), True, color)

        if blink:   self.blink(surf)
        elif pop_up:  self.pop_up(surf)

        rect = surf.get_rect(midtop=(midtop_pos[0],midtop_pos[1]))

        self.display_surface.blit(surf, rect)



    # create box, rect
    def create_bar(self, for_enemy_or_player, type, current_amount, max_amount, rect, color):
        if type == 'health':
            if for_enemy_or_player == 'player':     width = HEALTH_BAR_WIDTH['player']
            else:   width = HEALTH_BAR_WIDTH['enemy']
        else:
            width = MANA_BAR_WIDTH

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, rect)

        current_amount_display = (width * current_amount) / max_amount
        rect_display = rect.copy()
        rect_display.width = current_amount_display

        pygame.draw.rect(self.display_surface, color, rect_display)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, rect, 2)

    def creat_box(self, type, center_pos, size, has_switched=None): 
        rect = pygame.Rect((0,0), size)
        rect.center = center_pos

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, rect, 3) 
        if type == 'selection': 
            if not has_switched:
                pygame.draw.rect(self.display_surface, SWITCH_BOX_COLOR, rect, 3)  
            
        return(rect)


    def weapon_magic_choice_box(self, type, center_pos, index, has_switched):
        if type == 'weapon':
            box_rect = self.creat_box('selection', center_pos, BOX_SIZE['choice'], has_switched)
            image = self.weapon_images_list[index]
        else:
            box_rect = self.creat_box('selection', center_pos, BOX_SIZE['choice'], has_switched)
            image = self.magic_images_list[index]

        rect = image.get_rect(center = box_rect.center)
        self.display_surface.blit(image, rect)


    def player_health_bar(self, current_health, max_health):
        self.create_bar('player', 'health', current_health, max_health, self.health_bar_rect, HEALTH_COLOR)

    def player_mana_bar(self, current_health, max_health):
        self.create_bar('player', 'mana', current_health, max_health, self.mana_bar_rect, MANA_COLOR)

    def player_exp_box(self, center_pos, current_exp):
        resize_offset = (len(str(current_exp))) * 15

        EXP_BOX_RESIZE_AUTO = (BOX_SIZE['exp'][0] + resize_offset, BOX_SIZE['exp'][1])

        rect = self.creat_box('exp', center_pos, EXP_BOX_RESIZE_AUTO)
        

        msg_surf = self.font.render(str(current_exp), True, 'white')
        msg_rect = msg_surf.get_rect(center=rect.center)
        self.display_surface.blit(msg_surf, msg_rect)


    def enemy_health_bar(self, current_health, max_health):
        self.create_bar('enemy', 'health', current_health, max_health, self.enemy_bar_rect, HEALTH_COLOR)
        
    def enemy_icon(self, icon_img):
        x = self.enemy_bar_rect.midright[0]
        y = self.enemy_bar_rect.centery
        box_rect = self.creat_box('avatar', (x,y), BOX_SIZE['choice'])

        img = pygame.transform.rotozoom(icon_img, 0, 0.5)
        rect = img.get_rect(center=box_rect.center)
        
        self.display_surface.blit(img, rect)
   