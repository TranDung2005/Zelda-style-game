import pygame
from support import import_imgs_list
from random import choice

class PARTICLE_EFFECT(pygame.sprite.Sprite):
	def __init__(self, pos, animation_frames, groups):
		super().__init__(groups)

		self.sprite_type = 'particle_effect'
		self.frame_index = 0
		self.animation_speed = 0.15
        
		self.frames = animation_frames
		self.image = self.frames[self.frame_index] 
		self.rect = self.image.get_rect(center=pos)

	def animate(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			self.kill()	

		else:
			self.image = self.frames[int(self.frame_index)]
		

	def update(self):
		self.animate()


class PARTICLE_ANIMATION:
    def __init__(self):
        self.frames = {
        # magic
        'flame': import_imgs_list('graphics/particles/flame/frames'),
        'aura': import_imgs_list('graphics/particles/aura'),
        'heal': import_imgs_list('graphics/particles/heal/frames'),

        # attacks 
        'claw': (import_imgs_list('graphics/particles/claw'), 
                self.reflect_img(import_imgs_list('graphics/particles/claw'))),

        'slash': (import_imgs_list('graphics/particles/slash'),
                self.reflect_img(import_imgs_list('graphics/particles/slash'))),

        'sparkle': (import_imgs_list('graphics/particles/sparkle'),
                self.reflect_img(import_imgs_list('graphics/particles/sparkle'))),

        'leaf_attack': (import_imgs_list('graphics/particles/leaf_attack'),
                self.reflect_img(import_imgs_list('graphics/particles/leaf_attack'))),

        'thunder': (import_imgs_list('graphics/particles/thunder'),
                self.reflect_img(import_imgs_list('graphics/particles/thunder'))),


        # enemy deaths
        'squid': import_imgs_list('graphics/particles/smoke_orange'),
        'raccoon': import_imgs_list('graphics/particles/raccoon'),
        'spirit': import_imgs_list('graphics/particles/nova'),
        'bamboo': import_imgs_list('graphics/particles/bamboo'),

        # leafs 
        'leaf': (
            import_imgs_list('graphics/particles/leaf1'),
            import_imgs_list('graphics/particles/leaf2'),
            import_imgs_list('graphics/particles/leaf3'),
            import_imgs_list('graphics/particles/leaf4'),
            import_imgs_list('graphics/particles/leaf5'),
            import_imgs_list('graphics/particles/leaf6'),
            self.reflect_img(import_imgs_list('graphics/particles/leaf1')),
            self.reflect_img(import_imgs_list('graphics/particles/leaf2')),
            self.reflect_img(import_imgs_list('graphics/particles/leaf3')),
            self.reflect_img(import_imgs_list('graphics/particles/leaf4')),
            self.reflect_img(import_imgs_list('graphics/particles/leaf5')),
            self.reflect_img(import_imgs_list('graphics/particles/leaf6'))
            )
        }


    def reflect_img(self, imgs_list):
        refect_imgs_list = []
        for img in imgs_list:
            flipped_img = pygame.transform.flip(img, True, False)
            refect_imgs_list.append(flipped_img)

        return(refect_imgs_list)
	

    def create_particles(self, type, pos, groups):
        if type in ['leaf', 'claw', 'slash', 'sparkle', 'leaf_attack', 'thunder']:
            animation_frames = choice(self.frames[type])
        else:
            animation_frames = list(self.frames[type])
            
        PARTICLE_EFFECT(pos, animation_frames, groups)

   