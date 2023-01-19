SCR_WIDTH = 1280
SCR_HEIGHT = 720
TILESIZE = 64

# player
PLAYER_DATA = {'health':200, 'free_harm':0, 'mana':130, 'exp':0, 
			'mana_auto_recovery':0.1, 'hand_damage':4, 'magic_hand_damage':4, 'speed':6
		}
		
PLAYER_ATTACKABLE_COOLDOWN = 0.4 * 60
SWITCH_COOLDOWN = 0.3 * 60

HITBOX = {'player':(-6,-26),
			'enemy':{'bamboo':(-2,-10), 'squid':(-2,-10), 'spirit':(-10, -10), 'raccoon':(-100,-200)},
			'object':(0,-40),
			'grass':(0,-10),
			'boundary':(0,0)
			}

INVINCIBILITY_DURATION = {'player':0.3 * 60, 'enemy':0.3 * 60}

# UI
BAR_HEIGHT = {'player':20, 'enemy':30}
HEALTH_BAR_WIDTH = {'player':200, 'enemy':600}
MANA_BAR_WIDTH = 140
UI_FONT = 'graphics/font/joystix.ttf'
UI_FONT_SIZE = {'header':30, 'write':18}
BOX_SIZE = {'upgrade_choice':(300,300), 'choice':(80,80), 'exp':(30,35), 'upgrade_button':(300,50)}

# colors
HEALTH_COLOR = '#ff0000'
MANA_COLOR = '#0000ff'
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#1a1a1a'
UI_BORDER_COLOR = '#333333'
SWITCH_BOX_COLOR = '#ffff00'
UPGRADE_BG_COLOR = '#262626'


# weapons 
WEAPON_DATA = {
	'sword': {'cooldown':0.1*60, 'damage':17, 'heavy':0.5, 'path':'graphics/weapons/sword/full.png'},
	'lance': {'cooldown':0.5*60, 'damage':38, 'heavy':2, 'path':'graphics/weapons/lance/full.png'},
	'axe': {'cooldown':0.3*60, 'damage':23, 'heavy':1.3, 'path':'graphics/weapons/axe/full.png'},
	'rapier':{'cooldown':0.15*60, 'damage':27, 'heavy':0.75, 'path':'graphics/weapons/rapier/full.png'},
	'sai':{'cooldown':0.2*60, 'damage':12, 'heavy':1, 'path':'graphics/weapons/sai/full.png'}
	}


# magic
MAGIC_DATA = {
	'flame': {'cooldown':0.5*60, 'strength':50, 'mana_spend':50, 'path':'graphics/particles/flame/flame.png'},
	'heal': {'cooldown':0.2*60, 'strength':30, 'mana_spend':10, 'path':'graphics/particles/heal/heal.png'}
	}


# enemies
ENEMY_DATA = {	# raccoon notice_radius depend on player in territory
	'squid': {'health':350, 'exp':170, 'damage':40, 'attack_type':'slash', 'attack_sound':'audio/enemy/slash.wav', 'speed':4, 'resistance':4, 'attack_radius':80, 'notice_radius':360 ,'attackable_cooldown':2*60},
	'raccoon': {'health':2000, 'exp':500, 'damage':160, 'attack_type':'claw', 'attack_sound':'audio/enemy/claw.wav','speed':2, 'resistance':0, 'attack_radius':120, 'notice_radius':-1, 'attackable_cooldown':4*60},
	'spirit': {'health':150, 'exp':30, 'damage':60, 'attack_type':'thunder', 'attack_sound':'audio/enemy/fireball.wav', 'speed':5.5, 'resistance':3, 'attack_radius':30, 'notice_radius':400, 'attackable_cooldown':0.5*60},
	'bamboo': {'health':300, 'exp':120, 'damage':30, 'attack_type':'leaf_attack', 'attack_sound':'audio/enemy/slash.wav', 'speed':3, 'resistance':3, 'attack_radius':50, 'notice_radius':300, 'attackable_cooldown':1*60},
	}


# audio			
AUDIO_DATA = {
			# background
			'start': "audio/background/start.wav",
			'play': "audio/background/play.ogg",
			'end': "audio/background/end.wav",

			# switch
			'shop': "audio/switch/shop.wav",
			'change_magic': "audio/switch/change_magic.wav",
			'change_weapon': "audio/switch/change_weapon.wav",
			'upgrade': "audio/switch/upgrade.wav",
			'switch': "audio/switch/switch.wav",
			'select': "audio/switch/select.wav",
			'button': "audio/switch/button.wav",

			# player
			'heal': "audio/player/heal.wav",
			'fire': "audio/player/fire.wav",
			'weapon': "audio/player/weapon.wav",
			'attack': "audio/player/attack.wav",
			'attack_air': "audio/player/attack_air.wav",
			'attack_grass': "audio/player/attack_grass.wav",
			'player_die': "audio/player/die.wav",
			'out': "audio/player/out.wav",

			# enemy
			'enemy_die': "audio/enemy/die.wav",
			'boss_die': "audio/enemy/boss_die.wav",
		}


# upgrade
UPGRADE_DATA = {
			'weapon': {'cost':150, 'damage':3},
			'magic': {'heal': {'cost':200, 'strength':10, 'free_harm':3},
					'flame': {'cost':230, 'strength':50, 'hand_damage':5}
						}
	}