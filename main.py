# import essential modules
# system modules:
import pygame
import random
import sys
from math import atan, degrees
# custom modules:
import unit_info, turret_info, projectile_info
from spritesheet import SpriteSheet

# initialize pygame module
pygame.init()

# main game class
class Game:
	def __init__(self):
		# constants:
		self.WINDOWTITLE = "AGE OF PIXEL"
		self.FLOOR_LEVEL = 460
		self.GRAVITY = 0.4


		# dev mode
		self.dev_mode = False
		
		# normal variables:
		self.running = True
		self.paused = False
		self.game_won = False
		self.game_over = False
		self.main_menu = False

		self.scaling_factor_x = 1
		self.scaling_factor_y = 1

		self.mouse_pos = (pygame.mouse.get_pos()[0] / self.scaling_factor_x, pygame.mouse.get_pos()[1] / self.scaling_factor_y)
		
		# clock object to keep constant framerate
		self.clock = pygame.time.Clock()


		# time variables to keep track of time
		self.frames_passed = 0
		self.seconds_passed = 0
		self.minutes_passed = 0
		# chooses if window should be fullscreen (work in progress: window scaling does not work propperly)
		self.SCREEN_SIZE = (960, 540)
		self.display = pygame.display.set_mode(self.SCREEN_SIZE, pygame.RESIZABLE)
		self.SCREEN_SIZE = (960, 540)

	
		pygame.display.set_caption(self.WINDOWTITLE)
		pygame.display.set_icon(pygame.image.load("assets/icon/aow_icon.png"))

		self.screen = pygame.Surface(self.SCREEN_SIZE, pygame.SRCALPHA)

		# changing menu variables
		self.unit_menu_open = False
		self.turret_menu_open = False
		self.clicked = False

		# rects to pan cam when mouse is at the edge of the screen
		self.screen_pan_rect_left = pygame.Rect(0, 128, 150, self.SCREEN_SIZE[1] - 128)
		self.screen_pan_rect_right = pygame.Rect(self.SCREEN_SIZE[0] - 150, 128, 150, self.SCREEN_SIZE[1] - 128)
		
		# camera setup
		self.camera_offset_x = 0
		self.camera_move_speed = 10
		self.scroll_speed = 20

		# key_pressed variables
		self.pan_right = False
		self.pan_left = False

		# list with all friendly units that are being trained
		self.friendly_units_queue = []

		# list containing only one unit, which is being trained
		self.training = []
		self.training_timer = 0
		self.training_timer_goal = 5 * 60

		# list containing units on hold
		self.friendly_unit_buffer = []
		self.enemy_unit_buffer = []

		# variables determening if unit is free to spawn
		self.friendly_spawn_allowed = True
		self.enemy_spawn_allowed = True

		# lists containing units on the battlefield in the correct order!!!
		self.friendly_units = []
		self.enemy_units = []

		# lists containing turrets on screen
		self.friendly_turrets = []
		self.enemy_turrets = []

		# variables determening if turret slot is taken
		# friendly:
		self.friendly_slots_free = {
			1: False,
			2: False,
			3: False
		}
		# enemy:
		self.enemy_slots_free = {
			1: False,
			2: False,
			3: False
		}

		self.turret_buy_mode = False
		self.turret_sell_mode = False

		self.turret_id_to_buy = 0

		# controlling enemy spawns
		self.enemy_spawn_timer = 0
		self.enemy_spawn_timer_goal = 5 * 60
		self.spawn_options = [1]


		# special attack cooldown
		self.special_timer = 0
		self.special_timer_goal = 50 * 60
		self.percent_value_special = 100 / self.special_timer_goal * self.special_timer
		self.special_available = False

		# current player age
		self.age = 1

		# current enemy age
		self.enemy_age = 1

		
		# player and enemy base upgrade state
		self.friendly_base_upgrade_state = 0
		self.enemy_base_upgrade_state = 0

		# base upgrade cost
		self.upgrade_cost = 200
	
		# declaring pos where base upgrade modules should be placed
		# tier 1 friendly
		self.friendly_module_pos1_t1 = (50 + self.camera_offset_x, 275)
		self.friendly_module_pos2_t1 = (50 + self.camera_offset_x, 275-64)
		self.friendly_module_pos3_t1 = (50 + self.camera_offset_x, 275-128)
		# tier 1 enemy
		self.enemy_module_pos1_t1 = (1870 + self.camera_offset_x, 0)
		self.enemy_module_pos2_t1 = (1870 + self.camera_offset_x, 0)
		self.enemy_module_pos3_t1 = (1870 + self.camera_offset_x, 0)
		# tier 2 friendly
		self.friendly_module_pos1_t2 = (129 + self.camera_offset_x, 235)
		self.friendly_module_pos2_t2 = (129 + self.camera_offset_x, 235-64)
		self.friendly_module_pos3_t2 = (129 + self.camera_offset_x, 235-128)
		# tier 2 enemy
		self.enemy_module_pos1_t2 = (1850 + self.camera_offset_x, 0)
		self.enemy_module_pos2_t2 = (1850 + self.camera_offset_x, 0)
		self.enemy_module_pos3_t2 = (1850 + self.camera_offset_x, 0)
		# tier 3 friendly
		self.friendly_module_pos1_t3 = (80 + self.camera_offset_x, 270)
		self.friendly_module_pos2_t3 = (80 + self.camera_offset_x, 270-64)
		self.friendly_module_pos3_t3 = (80 + self.camera_offset_x, 270-128)
		# tier 3 enemy
		self.enemy_module_pos1_t3 = (1850 + self.camera_offset_x, 0)
		self.enemy_module_pos2_t3 = (1850 + self.camera_offset_x, 0)
		self.enemy_module_pos3_t3 = (1850 + self.camera_offset_x, 0)

		# player and enemys money
		self.friendly_money = 300
		self.enemy_money = 10

		# player and enemy exp
		self.friendly_exp = 0
		self.enemy_exp = 0

		# treshholds for age upgrade
		self.age2_treshhold = 12000
		self.age3_treshhold = 50000

		# list containing all the blood particles on screen
		self.blood_particles = []
		# list containing all the meteors on screen
		self.meteors = []
		#list containing all the arrows on screen
		self.arrows = []
		#list containing all the planes on screen
		self.planes = []
		#list containing all the bullets shot by plane
		self.bullets = []
		#list containing all the dirt particles on screen
		self.dirt_particles = []
		#list containing particle objects
		self.particles = []

		# specifying button location and size

		self.unit_select_button_rect = pygame.Rect(648, 8, 48, 48)
		self.turret_select_button_rect = pygame.Rect(712, 8, 48, 48)
		self.turret_upgrade_button_rect = pygame.Rect(776, 8, 48, 48)
		self.special_attack_button_rect = pygame.Rect(840, 8, 48, 48)
		self.age_advance_button_rect = pygame.Rect(904, 8, 48, 48)

		self.unit_1_button_rect = pygame.Rect(648, 72, 48, 48)
		self.unit_2_button_rect = pygame.Rect(712, 72, 48, 48)
		self.unit_3_button_rect = pygame.Rect(776, 72, 48, 48)

		self.turret_1_button_rect = pygame.Rect(712, 72, 48, 48)
		self.turret_2_button_rect = pygame.Rect(776, 72, 48, 48)
		self.turret_3_button_rect = pygame.Rect(840, 72, 48, 48)
		self.turret_sell_button_rect = pygame.Rect(904, 72, 48, 48)

		self.pause_button_rect = pygame.Rect(0, 64, 32, 32)


		self.pause_button_continue_rect = pygame.Rect(352, 192, 256, 64)
		self.pause_button_restart_rect = pygame.Rect(352, 288, 256, 64)
		self.pause_button_quit_rect = pygame.Rect(352, 384, 256, 64)
	

		# importing game assets:

		#	sounds

		#	music
		self.aow_theme_music = pygame.mixer.Sound("assets/audio/music/aow_theme_music.mp3")
		#	playing music
		self.aow_theme_music.play(loops= 20)

		#	setting the volume for every sound
		self.aow_theme_music.set_volume(0.3)

		#	 font
		self.font_10 = pygame.font.Font("assets/font/pixel_font.otf", 10)
		self.font_12 = pygame.font.Font("assets/font/pixel_font.otf", 12)
		self.font_14 = pygame.font.Font("assets/font/pixel_font.otf", 14)
		self.font_16 = pygame.font.Font("assets/font/pixel_font.otf", 16)
		self.font_18 = pygame.font.Font("assets/font/pixel_font.otf", 18)
		self.font_20 = pygame.font.Font("assets/font/pixel_font.otf", 20)
		self.font_25 = pygame.font.Font("assets/font/pixel_font.otf", 25)
		self.font_30 = pygame.font.Font("assets/font/pixel_font.otf", 30)
		self.font_35 = pygame.font.Font("assets/font/pixel_font.otf", 35)
		self.font_40 = pygame.font.Font("assets/font/pixel_font.otf", 40)
		self.font_45 = pygame.font.Font("assets/font/pixel_font.otf", 45)
		self.font_50 = pygame.font.Font("assets/font/pixel_font.otf", 50)
		self.font_60 = pygame.font.Font("assets/font/pixel_font.otf", 60)
		self.font_70 = pygame.font.Font("assets/font/pixel_font.otf", 70)
		self.font_80 = pygame.font.Font("assets/font/pixel_font.otf", 80)
		self.font_90 = pygame.font.Font("assets/font/pixel_font.otf", 90)
		self.font_100 = pygame.font.Font("assets/font/pixel_font.otf", 100)
		self.font_150 = pygame.font.Font("assets/font/pixel_font.otf", 150)
		self.font_200 = pygame.font.Font("assets/font/pixel_font.otf", 200)
		#	 background
		self.background = pygame.image.load("assets/background/Age_Of_War_background.png").convert_alpha()
		self.background_pos = (0 + self.camera_offset_x, -540)
		# 	player base stone age
		self.friendly_base1_t1 = pygame.image.load("assets/bases/cave_base.png").convert_alpha()
		self.friendly_base2_t1 = pygame.image.load("assets/bases/cave_base2.png").convert_alpha()
		#	player base middle age
		self.friendly_base1_t2 = pygame.image.load("assets/bases/aow_2_base_1.png").convert_alpha()
		self.friendly_base2_t2 = pygame.image.load("assets/bases/aow_2_base_2.png").convert_alpha()
		#	player base modern age
		self.friendly_base1_t3 = pygame.image.load("assets/bases/aow_3_base_1.png").convert_alpha()
		self.friendly_base2_t3 = pygame.image.load("assets/bases/aow_3_base_2.png").convert_alpha()
		# 	create friendly base rect
		self.friendly_base_rect = self.friendly_base1_t1.get_rect()
		# 	set pos to const FLOOR LEVEL
		self.friendly_base_rect.bottomleft = (0 + self.camera_offset_x, self.FLOOR_LEVEL)
		# 	enemy base stone age (same as friendly base but flipped)
		self.enemy_base1_t1 = pygame.transform.flip(self.friendly_base1_t1, True, False)
		self.enemy_base2_t1 = pygame.transform.flip(self.friendly_base2_t1, True, False)
		#	enemy base middle age
		self.enemy_base1_t2 = pygame.transform.flip(self.friendly_base1_t2, True, False)
		self.enemy_base2_t2 = pygame.transform.flip(self.friendly_base2_t2, True, False)
		#	enemy base modern age
		self.enemy_base1_t3 = pygame.transform.flip(self.friendly_base1_t3, True, False)
		self.enemy_base2_t3 = pygame.transform.flip(self.friendly_base2_t3, True, False)
		# 	create enemy base rect
		self.enemy_base_rect = self.enemy_base1_t1.get_rect()
		self.enemy_base_rect.bottomright = (self.SCREEN_SIZE[0] + self.camera_offset_x, self.FLOOR_LEVEL)
		#	load base_upgrade_modules
		self.base_upgrade_1 = pygame.image.load("assets/upgrade_modules/aow_1_turretmount.png").convert_alpha()
		self.base_upgrade_2 = pygame.image.load("assets/upgrade_modules/aow_2_turretmount.png").convert_alpha()
		self.base_upgrade_3 = pygame.image.load("assets/upgrade_modules/aow_3_turretmount.png").convert_alpha()
		#	get base upgrade rects
		self.base_upgrade_1_rect = self.base_upgrade_3.get_rect()
		self.base_upgrade_2_rect = self.base_upgrade_3.get_rect()
		self.base_upgrade_3_rect = self.base_upgrade_3.get_rect()
		#	get enemy base upgrade rects
		self.enemy_base_upgrade_1_rect = self.base_upgrade_3.get_rect()
		self.enemy_base_upgrade_2_rect = self.base_upgrade_3.get_rect()
		self.enemy_base_upgrade_3_rect = self.base_upgrade_3.get_rect()
		# 	load the ui image
		self.ui_main = pygame.image.load("assets/ui/aow_ui1.png").convert_alpha()

		self.ui_units = pygame.image.load("assets/ui/aow_ui_units.png").convert_alpha()
		self.ui_turrets = pygame.image.load("assets/ui/aow_ui_turrets.png").convert_alpha()

		self.ui_pause_menu = pygame.image.load("assets/ui/aow_ui_pause_menu.png").convert_alpha()

		self.ui_pause_button = pygame.image.load("assets/ui/aow_ui_pause_button.png").convert_alpha()

		#   load special attack spritesheets
		#	tier 1
		self.tier1_special_sheet_img = pygame.image.load("assets/special_attack/tier1/aow_special_meteor.png").convert_alpha()
		self.tier1_special_sheet = SpriteSheet(self.tier1_special_sheet_img)
		#   tier 2
		self.tier2_special_sheet_img = pygame.image.load("assets/special_attack/tier2/aow_special_arrow.png").convert_alpha()
		self.tier2_special_sheet = SpriteSheet(self.tier2_special_sheet_img)
		#   tier 3
		self.tier3_special_sheet_img = pygame.image.load("assets/special_attack/tier3/aow_special_a10.png").convert_alpha()
		self.tier3_special_bullet = pygame.image.load("assets/special_attack/tier3/aow_special_a10_bullet.png").convert_alpha()
		self.tier3_special_sheet = SpriteSheet(self.tier3_special_sheet_img)
		# 	load unit spritesheets
		#	tier 1
		self.unit_1_sheet_img = pygame.image.load("assets/units/tier1/aow_1_caveman1.png").convert_alpha()
		self.unit_1_sheet = SpriteSheet(self.unit_1_sheet_img)
		self.unit_2_sheet_img = pygame.image.load("assets/units/tier1/aow_1_caveman2.png").convert_alpha()
		self.unit_2_sheet = SpriteSheet(self.unit_2_sheet_img)
		self.unit_3_sheet_img = pygame.image.load("assets/units/tier1/aow_1_caveman3.png").convert_alpha()
		self.unit_3_sheet = SpriteSheet(self.unit_3_sheet_img)
		#	tier 2
		self.unit_4_sheet_img = pygame.image.load("assets/units/tier2/aow_2_knight1.png").convert_alpha()
		self.unit_4_sheet = SpriteSheet(self.unit_4_sheet_img)
		self.unit_5_sheet_img = pygame.image.load("assets/units/tier2/aow_2_wizzard2.png").convert_alpha()
		self.unit_5_sheet = SpriteSheet(self.unit_5_sheet_img)
		self.unit_6_sheet_img = pygame.image.load("assets/units/tier2/aow_2_king3.png").convert_alpha()
		self.unit_6_sheet = SpriteSheet(self.unit_6_sheet_img)
		#	tier 3
		self.unit_7_sheet_img = pygame.image.load("assets/units/tier3/aow_3_soldiert1.png").convert_alpha()
		self.unit_7_sheet = SpriteSheet(self.unit_7_sheet_img)
		self.unit_8_sheet_img = pygame.image.load("assets/units/tier3/aow_3_rambo.png").convert_alpha()
		self.unit_8_sheet = SpriteSheet(self.unit_8_sheet_img)
		self.unit_9_sheet_img = pygame.image.load("assets/units/tier3/aow_3_tank.png").convert_alpha()
		self.unit_9_sheet = SpriteSheet(self.unit_9_sheet_img)
		#	loading unit weapons
		#	tier 1
		self.weapon_1_sheet_img = pygame.image.load("assets/weapons/tier1/aow_1_weapon_1.png").convert_alpha()
		self.weapon_1_sheet = SpriteSheet(self.weapon_1_sheet_img)
		self.weapon_2_sheet_img = pygame.image.load("assets/weapons/tier1/aow_1_weapon_2.png").convert_alpha()
		self.weapon_2_sheet = SpriteSheet(self.weapon_2_sheet_img)
		self.weapon_3_sheet_img = pygame.image.load("assets/weapons/tier1/aow_1_weapon_3.png").convert_alpha()
		self.weapon_3_sheet = SpriteSheet(self.weapon_3_sheet_img)
		#	tier 2
		self.weapon_4_sheet_img = pygame.image.load("assets/weapons/tier2/aow_2_weapon_1.png").convert_alpha()
		self.weapon_4_sheet = SpriteSheet(self.weapon_4_sheet_img)
		self.weapon_5_sheet_img = pygame.image.load("assets/weapons/tier2/aow_2_weapon_2.png").convert_alpha()
		self.weapon_5_sheet = SpriteSheet(self.weapon_5_sheet_img)
		self.weapon_6_sheet_img = pygame.image.load("assets/weapons/tier2/aow_2_weapon_3.png").convert_alpha()
		self.weapon_6_sheet = SpriteSheet(self.weapon_6_sheet_img)
		#	buffed crown
		self.buffed_crown_sheet_img = pygame.image.load("assets/weapons/tier2/aow_2_buffed_crown_3.png").convert_alpha()
		self.buffed_crown_sheet = SpriteSheet(self.buffed_crown_sheet_img)
		#	tier 3
		self.weapon_7_sheet_img = pygame.image.load("assets/weapons/tier3/aow_3_weapon_1.png").convert_alpha()
		self.weapon_7_sheet = SpriteSheet(self.weapon_7_sheet_img)
		self.weapon_8_sheet_img = pygame.image.load("assets/weapons/tier3/aow_3_weapon_2.png").convert_alpha()
		self.weapon_8_sheet = SpriteSheet(self.weapon_8_sheet_img)
		
	

		#	loading turret spritesheets
		#	tier 1
		self.turret_1_sheet_img = pygame.image.load("assets/turrets/tier1/aow_1_turret_1.png").convert_alpha()
		self.turret_1_sheet = SpriteSheet(self.turret_1_sheet_img)
		self.turret_2_sheet_img = pygame.image.load("assets/turrets/tier1/aow_1_turret_2.png").convert_alpha()
		self.turret_2_sheet = SpriteSheet(self.turret_2_sheet_img)
		self.turret_3_sheet_img = pygame.image.load("assets/turrets/tier1/aow_1_turret_3.png").convert_alpha()	
		self.turret_3_sheet = SpriteSheet(self.turret_3_sheet_img)
		#	tier 2
		self.turret_4_sheet_img = pygame.image.load("assets/turrets/tier2/aow_2_turret_1.png").convert_alpha()
		self.turret_4_sheet = SpriteSheet(self.turret_4_sheet_img)
		self.turret_5_sheet_img = pygame.image.load("assets/turrets/tier2/aow_2_turret_2.png").convert_alpha()
		self.turret_5_sheet = SpriteSheet(self.turret_5_sheet_img)
		self.turret_6_sheet_img = pygame.image.load("assets/turrets/tier2/aow_2_turret_3.png").convert_alpha()
		self.turret_6_sheet = SpriteSheet(self.turret_6_sheet_img)
		#	tier 3
		self.turret_7_sheet_img = pygame.image.load("assets/turrets/tier3/aow_3_turret_1.png").convert_alpha()
		self.turret_7_sheet = SpriteSheet(self.turret_7_sheet_img)
		self.turret_8_sheet_img = pygame.image.load("assets/turrets/tier3/aow_3_turret_2.png").convert_alpha()
		self.turret_8_sheet = SpriteSheet(self.turret_8_sheet_img)
		self.turret_9_sheet_img = pygame.image.load("assets/turrets/tier3/aow_3_turret_3.png").convert_alpha()
		self.turret_9_sheet = SpriteSheet(self.turret_9_sheet_img)
		# 	loading projectile spritesheets
		#	tier1
		self.projectile_1_sheet_img = pygame.image.load("assets/projectiles/aow_1_projectile_1.png").convert_alpha()
		self.projectile_1_sheet = SpriteSheet(self.projectile_1_sheet_img)
		self.projectile_2_sheet_img = pygame.image.load("assets/projectiles/aow_1_projectile_2.png").convert_alpha()
		self.projectile_2_sheet = SpriteSheet(self.projectile_2_sheet_img)
		self.projectile_3_sheet_img = pygame.image.load("assets/projectiles/aow_1_projectile_3.png").convert_alpha()
		self.projectile_3_sheet = SpriteSheet(self.projectile_3_sheet_img)
		#	tier2
		self.projectile_4_sheet_img = pygame.image.load("assets/projectiles/aow_2_projectile_1.png").convert_alpha()
		self.projectile_4_sheet = SpriteSheet(self.projectile_4_sheet_img)
		self.projectile_5_sheet_img = pygame.image.load("assets/projectiles/aow_2_projectile_2.png").convert_alpha()
		self.projectile_5_sheet = SpriteSheet(self.projectile_5_sheet_img)
		self.projectile_6_sheet_img = pygame.image.load("assets/projectiles/aow_2_projectile_3.png").convert_alpha()
		self.projectile_6_sheet = SpriteSheet(self.projectile_6_sheet_img)
		#	tier3
		self.projectile_7_sheet_img = pygame.image.load("assets/projectiles/aow_3_projectile_1.png").convert_alpha()
		self.projectile_7_sheet = SpriteSheet(self.projectile_7_sheet_img)
		self.projectile_8_sheet_img = pygame.image.load("assets/projectiles/aow_3_projectile_2.png").convert_alpha()
		self.projectile_8_sheet = SpriteSheet(self.projectile_8_sheet_img)
		self.projectile_9_sheet_img = pygame.image.load("assets/projectiles/aow_3_projectile_3.png").convert_alpha()
		self.projectile_9_sheet = SpriteSheet(self.projectile_9_sheet_img)
		#	unit projectiles
		#self.unit_projectile_2 = pygame.image.load("assets/weapons/tier1/aow_1_weapon_projectile_2.png").convert_alpha()
		self.unit_projectile_2_img = pygame.image.load("assets/weapons/tier1/aow_1_weapon_projectile_2.png").convert_alpha()
		self.unit_projectile_2 = SpriteSheet(self.unit_projectile_2_img)
		self.unit_projectile_5_img = pygame.image.load("assets/weapons/tier2/aow_2_weapon_projectile_2.png").convert_alpha()
		self.unit_projectile_5 = SpriteSheet(self.unit_projectile_5_img)
		self.unit_projectile_7_img = pygame.image.load("assets/weapons/tier3/aow_3_weapon_projectile_1.png").convert_alpha()		
		self.unit_projectile_7 = SpriteSheet(self.unit_projectile_7_img)
		self.unit_projectile_9_img = pygame.image.load("assets/weapons/tier3/aow_3_weapon_projectile_3.png").convert_alpha()		
		self.unit_projectile_9 = SpriteSheet(self.unit_projectile_9_img)



#>>>>>>>>>>>>>>>>>>>>>>>>>>INPUT>LOOP>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

	def get_input(self):
		self.mouse_pos = (pygame.mouse.get_pos()[0] / self.scaling_factor_x, pygame.mouse.get_pos()[1] / self.scaling_factor_y)
		if not self.pan_right and not self.pan_left:	
			if self.screen_pan_rect_left.collidepoint(self.mouse_pos):
				if self.camera_offset_x <= -8:
					self.camera_offset_x += self.camera_move_speed
	
	
			if self.screen_pan_rect_right.collidepoint(self.mouse_pos):
				if self.camera_offset_x >= -1912 + self.SCREEN_SIZE[0]:
					self.camera_offset_x -= self.camera_move_speed

		for event in pygame.event.get():
			# quits pygame if game window is closed
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.VIDEORESIZE:
				self.display = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)


			# sets key_pressed variables to True if key is pressed
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					if not self.paused:
						self.paused = True
					else:
						self.paused = False
				elif event.key == pygame.K_TAB:
					# avtivates dev mode
					if not self.dev_mode:
						self.dev_mode = True
					else:
						self.dev_mode = False

				elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					self.pan_right = True
				elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
					self.pan_left = True


			# sets key_pressed variables back to false if key is realeased
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
					self.pan_right = False
				elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
					self.pan_left = False

		
#>>>>>>>>>>>>>>>>>>>>>>>>>>GAME>LOGIC>LOOP>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

	def calc_game_state(self):
		#calculates unit positions and moves camera
		self.get_scaling_factors()
		self.move_camera()
		self.handle_menu_selection()
		self.handle_friendly_spawns()
		self.handle_menu_selection()
		self.unit_menu()
		self.turret_menu()
		self.place_turret_at_slot()
		self.sell_turret_friendly()
		turret.update()
		projectile.update()
		unit_projectile.update()
		unit.update()
		self.check_game_over_game_won()
		self.handle_buttons()
		self.handle_special_cooldown()
		blood_master.update()
		meteor.update()
		arrow.update()
		plane.update()
		bullet.update()
		dirt.update()
		particle.update()
		self.update_global_time()
		self.handle_enemy_progression()
		self.spawn_enemys()
		self.give_money_when_in_dev_mode()

#>>>>>>>>>>>>>>>>>>>>>>>>RENDERING>LOOP>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

	def render_new_frame(self):
		self.display.fill((000,000,000))
		# render game objects
		self.screen.blit(self.background, self.background_pos)
		# render bases
		self.draw_upgrade_modules()
		self.draw_bases_1()
		# render all units here:
		# >>>>>
		dirt.draw()
		unit.draw()
		self.draw_unit_healthbars()

		blood_master.draw()
		particle.draw()
		# >>>>>
		self.draw_bases_2()
		projectile.draw()
		unit_projectile.draw()
		turret.draw()


		# render_special attacks:
		meteor.draw()
		arrow.draw()
		bullet.draw()
		plane.draw()


		# render ui at last pos to keep it in foreground!!
		self.draw_ui()
		if self.dev_mode:
			self.render_text(f"FPS           : {round(self.clock.get_fps())}", self.font_16, "black", (0,64))
			self.render_text(f"MINUTES PASSED: {self.minutes_passed}", self.font_16, "black", (0,80))
			self.render_text(f"ENEMY AGE     : {self.enemy_age}", self.font_16, "black", (0,96))
			self.render_text(f"SPAWN OPTIONS : {self.spawn_options}", self.font_16, "black", (0,112))
			self.render_text(f"SPAWN FREQ    : {round(self.enemy_spawn_timer_goal / 60)}", self.font_16, "black", (0,128))
			self.draw_transparent_rect(friendly_base.base_rect.size, (0,200,0), 50, friendly_base.base_rect.topleft)
			self.draw_transparent_rect(enemy_base.base_rect.size, (200,0,0), 50, enemy_base.base_rect.topleft)
			self.draw_transparent_rect(friendly_base.base_spawn_rect.size, (200,0,0), 50, friendly_base.base_spawn_rect.topleft)
			self.draw_transparent_rect(enemy_base.base_spawn_rect.size, (0,200,0), 50, enemy_base.base_spawn_rect.topleft)
			self.draw_transparent_rect(self.screen_pan_rect_left.size, (255,255,255), 20, self.screen_pan_rect_left.topleft)
			self.draw_transparent_rect(self.screen_pan_rect_right.size, (255,255,255), 20, self.screen_pan_rect_right.topleft)

		self.display.blit(self.resize_screen(), (0,0))
		# update the frame
		pygame.display.flip()
		
		# wait for clock tick
		self.clock.tick(60)

	
# >>>>>>>>>>>>>>>>>>>>>>MAIN>LOOP>>>>>>>>>>>>>>>>>>>>>>>>>>>>

	def mainloop(self):
		# main game loop (doesnt stop until game.running is set to false)
		while self.running:
			if not self.paused and not self.game_over and not self.game_won:
				# get user input:
				self.get_input()
				# do all the game logic:
				self.calc_game_state()
				# render the current frame:
				self.render_new_frame() 
			

			# freeze game if player won/lost or if game is paused
			elif self.paused:
				self.pause_loop()
			elif self.game_won:
				self.game_won_loop()
			elif self.game_over:
				self.game_won_loop()
			elif self.main_menu:
				self.main_menu_loop()


#>>>>>>>>>>>>>>>>>>>>>>MAIN>LOOP>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>	


	def pause_loop(self):
		self.get_input()
		# pause logic:
		self.calc_game_state_pause()
		# draw pause menu:
		self.render_new_frame_pause()
		self.clock.tick(60)

	def game_won_loop(self):
		self.get_input()
		# game_won logic:
		self.calc_game_state_game_won()
		# draw game won screen:
		self.render_new_frame_game_won()
		self.clock.tick(60)

	def game_over_loop(self):
		self.get_input()
		# game_over logic:
		self.calc_game_state_game_over()
		# draw game over screen:
		self.render_new_frame_game_over()
		self.clock.tick(60)

	def main_menu_loop(self):
		self.get_input()
		# main menu logic:
		self.calc_game_state_main_menu()
		# draw main menu:
		self.render_new_frame_main_menu()
		self.clock.tick(60)
	

	def calc_game_state_pause(self):
		self.get_scaling_factors()
		if not self.clicked:
			if self.pause_button_continue_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0]:
				self.clicked = True
				self.paused = False

			elif self.pause_button_restart_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0]:
				self.clicked = True
				self.reset_everything(False)


			elif self.pause_button_quit_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0]:
				pygame.quit()
				sys.exit(0)

	def render_new_frame_pause(self):
		self.screen.blit(self.background, self.background_pos)
		self.draw_upgrade_modules()
		self.draw_bases_1()
		unit.draw()
		self.draw_bases_2()
		projectile.draw()
		unit_projectile.draw()
		turret.draw()
		self.draw_transparent_rect(self.SCREEN_SIZE, (0,0,0), 40, (0,0))
		
		self.render_text("paused", self.font_80, (0,0,0), (self.SCREEN_SIZE[0] / 2 - 190, self.SCREEN_SIZE[1] / 2  - 200))
		self.screen.blit(self.ui_pause_menu, (0,0))
		if not self.pause_button_continue_rect.collidepoint(self.mouse_pos):
			self.render_text("continue", self.font_35, (0,0,0), (self.pause_button_continue_rect.x + 10, self.pause_button_continue_rect.y + 10))
		else:
			self.render_text("continue", self.font_35, (80,80,80), (self.pause_button_continue_rect.x + 10, self.pause_button_continue_rect.y + 10))

		if not self.pause_button_restart_rect.collidepoint(self.mouse_pos):
			self.render_text("restart", self.font_35, (0,0,0), (self.pause_button_restart_rect.x + 10, self.pause_button_restart_rect.y + 10))
		else:
			self.render_text("restart", self.font_35, (80,80,80), (self.pause_button_restart_rect.x + 10, self.pause_button_restart_rect.y + 10))

		if not self.pause_button_quit_rect.collidepoint(self.mouse_pos):
			self.render_text("quit", self.font_35, (0,0,0), (self.pause_button_quit_rect.x + 10, self.pause_button_quit_rect.y + 10))
		else:
			self.render_text("quit", self.font_35, (80,80,80), (self.pause_button_quit_rect.x + 10, self.pause_button_quit_rect.y + 10))

		self.display.blit(self.resize_screen(), (0,0))
		pygame.display.flip()

	def calc_game_state_game_won(self):
		self.get_scaling_factors()

	def render_new_frame_game_won(self):
		self.display.blit(self.resize_screen(), (0,0))
		pygame.display.flip()

	def calc_game_state_game_over(self):
		self.get_scaling_factors()

	def render_new_frame_game_over(self):
		self.display.blit(self.resize_screen(), (0,0))
		pygame.display.flip()

	def calc_game_state_main_menu(self):
		self.get_scaling_factors()

	def render_new_frame_main_menu(self):
		self.display.blit(self.resize_screen(), (0,0))
		pygame.display.flip()



	def reset_everything(self, menu:bool= True):
		pygame.mixer.stop()
		self.dev_mode = False
		self.running = True
		self.paused = False
		self.game_won = False
		self.game_over = False
		if menu:
			self.main_menu = True
		else:
			self.main_menu = False
			self.aow_theme_music.play(loops= 20)
		self.frames_passed = 0
		self.seconds_passed = 0
		self.minutes_passed = 0
		self.unit_menu_open = False
		self.turret_menu_open = False
		self.clicked = False
		self.camera_offset_x = 0
		self.pan_right = False
		self.pan_left = False
		self.friendly_units_queue = []
		self.training = []
		self.training_timer = 0
		self.friendly_unit_buffer = []
		self.enemy_unit_buffer = []
		self.friendly_spawn_allowed = True
		self.enemy_spawn_allowed = True
		self.friendly_units = []
		self.enemy_units = []
		self.friendly_turrets = []
		self.enemy_turrets = []
		self.friendly_slots_free = {
			1: False,
			2: False,
			3: False
		}
		self.enemy_slots_free = {
			1: False,
			2: False,
			3: False
		}
		self.turret_buy_mode = False
		self.turret_sell_mode = False
		self.turret_id_to_buy = 0
		self.enemy_spawn_timer = 0
		self.enemy_spawn_timer_goal = 5 * 60
		self.spawn_options = [1]
		self.special_timer = 0
		self.percent_value_special = 100 / self.special_timer_goal * self.special_timer
		self.special_available = False
		self.age = 1
		self.enemy_age = 1
		self.friendly_base_upgrade_state = 0
		self.enemy_base_upgrade_state = 0
		self.friendly_money = 300
		self.enemy_money = 10
		self.friendly_exp = 0
		self.enemy_exp = 0
		self.upgrade_cost = 200
		self.blood_particles = []
		self.meteors = []
		self.arrows = []
		self.planes = []
		self.bullets = []
		self.dirt_particles = []
		self.particles = []
		self.background_pos = (0 + self.camera_offset_x, -540)
		friendly_base.health = 500
		enemy_base.health = 500

	def update_global_time(self):
		self.frames_passed += 1
		if self.frames_passed == 60:
			self.frames_passed = 0
			self.seconds_passed += 1
			if self.seconds_passed == 60:
				self.seconds_passed = 0
				self.minutes_passed += 1
				


	def handle_enemy_progression(self):
		if self.minutes_passed == 1:
			self.enemy_age = 1
			self.spawn_options = [1,1,1,1,2]
			self.enemy_spawn_timer_goal = 6 * 60

		elif self.minutes_passed == 2:
			self.enemy_age = 1
			self.spawn_options = [1,2]
			self.enemy_spawn_timer_goal = 6 * 60
			self.enemy_base_upgrade_state = 1
			self.enemy_slots_free[1] = True

		elif self.minutes_passed == 3:
			self.enemy_age = 1
			self.spawn_options = [1,2,3]
			self.enemy_spawn_timer_goal = 6 * 60
			self.buy_turret_enemy()

		elif self.minutes_passed == 4:
			self.enemy_age = 1
			self.spawn_options = [1,2,2,3,3,3]
			self.enemy_spawn_timer_goal = 5 * 60

		elif self.minutes_passed == 5:
			self.enemy_age = 2
			self.spawn_options = [4,4,5]
			self.enemy_spawn_timer_goal = 6 * 60

		elif self.minutes_passed == 6:
			self.enemy_age = 2
			self.spawn_options = [4,4,5,6]
			self.enemy_spawn_timer_goal = 6 * 60

		elif self.minutes_passed == 7:
			self.enemy_age = 2
			self.spawn_options = [4,5,6]
			self.enemy_spawn_timer_goal = 5 * 60
			self.enemy_base_upgrade_state = 2
			self.enemy_slots_free[2] = True

		elif self.minutes_passed == 8:
			self.enemy_age = 2
			self.spawn_options = [4,5,5,6]
			self.enemy_spawn_timer_goal = 5 * 60
			self.buy_turret_enemy()
			self.remove_turrets_from_the_past()

		elif self.minutes_passed == 9:
			self.enemy_age = 2
			self.spawn_options = [4,4,4,4,5]
			self.enemy_spawn_timer_goal = 3 * 60

		elif self.minutes_passed == 10:
			self.enemy_age = 3
			self.spawn_options = [7,7,7,8]
			self.enemy_spawn_timer_goal = 5 * 60

		elif self.minutes_passed == 11:
			self.enemy_age = 3
			self.spawn_options = [7,7,8,9]
			self.enemy_spawn_timer_goal = 5 * 60

		elif self.minutes_passed == 12:
			self.enemy_age = 3
			self.spawn_options = [7,8,9]
			self.enemy_spawn_timer_goal = 5 * 60

		elif self.minutes_passed == 13:
			self.enemy_age = 3
			self.spawn_options = [7,8,8,8,9]
			self.enemy_spawn_timer_goal = 5 * 60

		elif self.minutes_passed == 14:
			self.enemy_age = 3
			self.spawn_options = [7,7,7,7,7,7,8]
			self.enemy_spawn_timer_goal = 3 * 60
			self.enemy_base_upgrade_state = 3
			self.enemy_slots_free[3] = True

		elif self.minutes_passed == 15:
			self.enemy_age = 3
			self.spawn_options = [7,7,8,8,8,9,9]
			self.enemy_spawn_timer_goal = 4 * 60
			self.buy_turret_enemy()

		elif self.minutes_passed == 16:
			self.enemy_age = 3
			self.spawn_options = [8,9,9,9,9,9]
			self.enemy_spawn_timer_goal = 5 * 60

		elif self.minutes_passed == 17:
			self.enemy_age = 3
			self.spawn_options = [7,8,9]
			self.enemy_spawn_timer_goal = 4 * 60

		elif self.minutes_passed == 18:
			self.enemy_age = 3
			self.enemy_spawn__options = [7,8,9]
			self.enemy_spawn_timer_goal = 4 * 60

		elif self.minutes_passed == 19:
			self.enemy_age = 3
			self.spawn_options = [7,8,9]
			self.enemy_spawn_timer_goal = 3 * 60
			self.remove_turrets_from_the_past()


		elif self.minutes_passed >= 20:
			self.enemy_age = 3
			self.spawn_options = [9,9,9]
			self.enemy_spawn_timer_goal = 3 * 60
			self.buy_turret_enemy()

	def resize_screen(self):
		screen = self.screen
		scaled_screen = pygame.transform.scale(screen, pygame.display.get_surface().get_size())
		return scaled_screen

	def get_scaling_factors(self):
		self.scaling_factor_x = pygame.display.get_surface().get_size()[0] / self.SCREEN_SIZE[0]
		self.scaling_factor_y = pygame.display.get_surface().get_size()[1] / self.SCREEN_SIZE[1]



	def spawn_enemys(self):
		self.enemy_spawn_timer += 1
		if self.enemy_spawn_timer >= self.enemy_spawn_timer_goal:
			unit.spawn_enemy(random.choice(self.spawn_options))
			self.enemy_spawn_timer = 0

	def buy_turret_enemy(self):
		for slot in self.enemy_slots_free:
			if self.enemy_slots_free[slot] == True:
				id = random.choice(self.spawn_options)
				turret.spawn_turret(False, id, slot)
				self.enemy_slots_free[slot] = False

	def remove_turrets_from_the_past(self):
		for turret in self.enemy_turrets:
			if self.age == 2:
				if turret.id == 1 or turret.id == 2 or turret.id == 3:
					self.enemy_slots_free[turret.slot] = True
					self.enemy_turrets.pop(self.enemy_turrets.index(turret))
			elif self.age == 3:
				if turret.id == 4 or turret.id == 5 or turret.id == 6:
					self.enemy_slots_free[turret.slot] = True
					self.enemy_turrets.pop(self.enemy_turrets.index(turret))


	def draw_transparent_rect(self, size:tuple, color:tuple, alpha:int, pos:tuple):
		surface = pygame.Surface(size, pygame.SRCALPHA)
		surface.fill((color[0],color[1],color[2],alpha))
		self.screen.blit(surface, pos)
	

	def handle_special_cooldown(self):
		if self.special_available == False:
			self.special_timer += 1
			if self.special_timer == self.special_timer_goal:
				self.special_timer = 0
				self.special_available = True

	def draw_special_cooldown(self):
		# draws a semi transparent rect over the specialbutton to visualize the cooldown
		if not self.special_available:
			self.percent_value_special = 100 / self.special_timer_goal * self.special_timer
			pixel_value = 48 / 100 * self.percent_value_special
			cooldown_rect = pygame.Rect(0,pixel_value,48,48)
			surface = pygame.Surface(cooldown_rect.size, pygame.SRCALPHA)
			pygame.draw.rect(surface, (0,0,0,130), cooldown_rect)
			self.screen.blit(surface, self.special_attack_button_rect)



	def handle_buttons(self):
		if not self.clicked:
			if self.turret_upgrade_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
				self.unit_menu_open = False
				self.turret_menu_open = False
				self.turret_buy_mode = False
				self.turret_sell_mode = False
				if not self.friendly_base_upgrade_state == 3:
					if self.friendly_money >= self.upgrade_cost:
						self.friendly_money -= self.upgrade_cost
						self.friendly_base_upgrade_state += 1
						self.friendly_slots_free[self.friendly_base_upgrade_state] = True
						self.upgrade_cost *= 4
				self.clicked = True
			elif self.special_attack_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
				self.turret_buy_mode = False
				self.turret_sell_mode = False
				if self.age == 1:
					if self.special_available:
						meteor.rain = True
						self.special_available = False
				elif self.age == 2:
					if self.special_available:
						arrow.rain = True
						self.special_available = False
				elif self.age == 3:
					if self.special_available:
						plane.spawn()
						self.special_available = False
				self.clicked = True
			elif self.age_advance_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
				self.turret_buy_mode = False
				self.turret_sell_mode = False
				self.unit_menu_open = False
				self.turret_menu_open = False
				self.age_advancment()
				self.clicked = True
			if self.pause_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
				self.paused = True
		
			if pygame.mouse.get_pressed()[0] == 0:
				self.clicked = False


	def handle_menu_selection(self):
		if not self.clicked:
			if self.unit_select_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
				self.turret_buy_mode = False
				self.turret_sell_mode = False
				if self.unit_menu_open == False:
					self.unit_menu_open = True
				elif self.unit_menu_open == True:
					self.unit_menu_open = False
				self.turret_menu_open = False
				self.clicked = True
			if self.turret_select_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
				self.turret_buy_mode = False
				self.turret_sell_mode = False
				if self.turret_menu_open == False:
					self.turret_menu_open = True
				elif self.turret_menu_open == True:
					self.turret_menu_open = False
				self.unit_menu_open = False
				self.clicked = True
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

	def unit_menu(self):
		if self.unit_menu_open:
			if self.age == 1:
				if not self.clicked:
					if self.unit_1_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
						self.buy_unit(1)
						self.clicked = True
					elif self.unit_2_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
						self.buy_unit(2)
						self.clicked = True
					elif self.unit_3_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
						self.buy_unit(3)
						self.clicked = True
				if pygame.mouse.get_pressed()[0] == 0:
					self.clicked = False
			if self.age == 2:
				if not self.clicked:
					if self.unit_1_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
						self.buy_unit(4)
						self.clicked = True
					elif self.unit_2_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
						self.buy_unit(5)
						self.clicked = True
					elif self.unit_3_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
						self.buy_unit(6)
						self.clicked = True
				if pygame.mouse.get_pressed()[0] == 0:
					self.clicked = False
			if self.age == 3:
				if not self.clicked:
					if self.unit_1_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
						self.buy_unit(7)
						self.clicked = True
					elif self.unit_2_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
						self.buy_unit(8)
						self.clicked = True
					elif self.unit_3_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
						self.buy_unit(9)
						self.clicked = True
				if pygame.mouse.get_pressed()[0] == 0:
					self.clicked = False

	def turret_menu(self):
		if self.turret_menu_open:
			if not self.clicked:
				if self.turret_sell_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
					self.clicked = True
					if not self.turret_sell_mode:
						self.turret_sell_mode = True
						self.turret_buy_mode = False
					else:
						self.turret_sell_mode = False
			if self.age == 1:
				if not self.clicked:
					if self.turret_1_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
						self.turret_buy_mode = True
						self.turret_sell_mode = False
						self.turret_id_to_buy = 1
						self.clicked = True
					elif self.turret_2_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
						self.turret_buy_mode = True
						self.turret_sell_mode = False
						self.turret_id_to_buy = 2
						self.clicked = True
					elif self.turret_3_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
						self.turret_buy_mode = True
						self.turret_sell_mode = False
						self.turret_id_to_buy = 3
						self.clicked = True
				if pygame.mouse.get_pressed()[0] == 0:
					self.clicked = False
			if self.age == 2:
				if not self.clicked:
					if self.turret_1_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
						self.turret_buy_mode = True
						self.turret_sell_mode = False
						self.turret_id_to_buy = 4
						self.clicked = True
					elif self.turret_2_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
						self.turret_buy_mode = True
						self.turret_sell_mode = False
						self.turret_id_to_buy = 5
						self.clicked = True
					elif self.turret_3_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
						self.turret_buy_mode = True
						self.turret_sell_mode = False
						self.turret_id_to_buy = 6
						self.clicked = True
				if pygame.mouse.get_pressed()[0] == 0:
					self.clicked = False
			if self.age == 3:
				if not self.clicked:
					if self.turret_1_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
						self.turret_buy_mode = True
						self.turret_sell_mode = False
						self.turret_id_to_buy = 7
						self.clicked = True
					elif self.turret_2_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
						self.turret_buy_mode = True
						self.turret_sell_mode = False
						self.turret_id_to_buy = 8
						self.clicked = True
					elif self.turret_3_button_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
						self.turret_buy_mode = True
						self.turret_sell_mode = False
						self.turret_id_to_buy = 9
						self.clicked = True
				if pygame.mouse.get_pressed()[0] == 0:
					self.clicked = False



	def place_turret_at_slot(self):
		if self.turret_buy_mode and self.turret_id_to_buy != 0:
			if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
				self.clicked = True
				if self.friendly_slots_free[1] and self.base_upgrade_1_rect.collidepoint(self.mouse_pos):
					self.buy_turret_friendly(self.turret_id_to_buy, 1)
					self.turret_id_to_buy = 0
					self.turret_buy_mode = False
				elif self.friendly_slots_free[2] and self.base_upgrade_2_rect.collidepoint(self.mouse_pos):
					self.buy_turret_friendly(self.turret_id_to_buy, 2)
					self.turret_id_to_buy = 0
					self.turret_buy_mode = False
				elif self.friendly_slots_free[3] and self.base_upgrade_3_rect.collidepoint(self.mouse_pos):
					self.buy_turret_friendly(self.turret_id_to_buy, 3)
					self.turret_id_to_buy = 0
					self.turret_buy_mode = False



	def draw_base_healthbar(self):
		healthbar_width = 7
		healthbar_height = 100

		friendly_health_rect = pygame.Rect(10 + self.camera_offset_x, game.FLOOR_LEVEL, healthbar_width, friendly_base.health /5)
		friendly_health_rect.bottom = game.FLOOR_LEVEL
		pygame.draw.rect(self.screen, (200,0,0), pygame.Rect(10 + self.camera_offset_x, game.FLOOR_LEVEL - 100, healthbar_width, healthbar_height))
		pygame.draw.rect(self.screen, (0,200,0), friendly_health_rect)

		enemy_health_rect = pygame.Rect(1900 + self.camera_offset_x, game.FLOOR_LEVEL, healthbar_width, enemy_base.health /5)
		enemy_health_rect.bottom = game.FLOOR_LEVEL
		pygame.draw.rect(self.screen, (200,0,0), pygame.Rect(1900 + self.camera_offset_x, game.FLOOR_LEVEL - 100, healthbar_width, healthbar_height))
		pygame.draw.rect(self.screen, (0,200,0), enemy_health_rect)

	def draw_unit_healthbars(self):
		# draws unit health bar on mouse hover
		for unit in self.friendly_units + self.enemy_units:
			if unit.unit_rect.collidepoint(self.mouse_pos):
				max_health = unit_info.unit_health[unit.id]
				health_percent = 100/max_health * unit.health
				health_pixel = unit.unit_rect.width/100 * health_percent
				red_rect = pygame.Surface((unit.unit_rect.width, 5))
				red_rect.fill((200,000,000))
				green_rect = pygame.Rect(0, 0, health_pixel, 5)
				pygame.draw.rect(red_rect, (000,200,000), green_rect)
				self.screen.blit(red_rect, (unit.unit_rect.x, unit.unit_rect.y - 10))

	def draw_unit_prices(self):
		# draws the price of the unit on mouse hover with color red when not affordable
		if self.unit_menu_open:
			if self.age == 1:
				if self.unit_1_button_rect.collidepoint(self.mouse_pos):
					if self.friendly_money >= unit_info.unit_cost[1]:
						color = (0,0,0)
					else:
						color = (200,0,0)
					text = self.render_text(str(unit_info.unit_cost[1]), self.font_20, color, (self.unit_1_button_rect.x, 130))
				if self.unit_2_button_rect.collidepoint(self.mouse_pos):
					if self.friendly_money >= unit_info.unit_cost[2]:
						color = (0,0,0)
					else:
						color = (200,0,0)
					text = self.render_text(str(unit_info.unit_cost[2]), self.font_20, color, (self.unit_2_button_rect.x, 130))
				if self.unit_3_button_rect.collidepoint(self.mouse_pos):
					if self.friendly_money >= unit_info.unit_cost[3]:
						color = (0,0,0)
					else:
						color = (200,0,0)
					text = self.render_text(str(unit_info.unit_cost[3]), self.font_20, color, (self.unit_3_button_rect.x, 130))
			elif self.age == 2:
				if self.unit_1_button_rect.collidepoint(self.mouse_pos):
					if self.friendly_money >= unit_info.unit_cost[4]:
						color = (0,0,0)
					else:
						color = (200,0,0)
					text = self.render_text(str(unit_info.unit_cost[4]), self.font_20, color, (self.unit_1_button_rect.x, 130))
				if self.unit_2_button_rect.collidepoint(self.mouse_pos):
					if self.friendly_money >= unit_info.unit_cost[5]:
						color = (0,0,0)
					else:
						color = (200,0,0)
					text = self.render_text(str(unit_info.unit_cost[5]), self.font_20, color, (self.unit_2_button_rect.x, 130))
				if self.unit_3_button_rect.collidepoint(self.mouse_pos):
					if self.friendly_money >= unit_info.unit_cost[6]:
						color = (0,0,0)
					else:
						color = (200,0,0)
					text = self.render_text(str(unit_info.unit_cost[6]), self.font_20, color, (self.unit_3_button_rect.x, 130))
			elif self.age == 3:
				if self.unit_1_button_rect.collidepoint(self.mouse_pos):
					if self.friendly_money >= unit_info.unit_cost[7]:
						color = (0,0,0)
					else:
						color = (200,0,0)
					text = self.render_text(str(unit_info.unit_cost[7]), self.font_20, color, (self.unit_1_button_rect.x, 130))
				if self.unit_2_button_rect.collidepoint(self.mouse_pos):
					if self.friendly_money >= unit_info.unit_cost[8]:
						color = (0,0,0)
					else:
						color = (200,0,0)
					text = self.render_text(str(unit_info.unit_cost[8]), self.font_20, color, (self.unit_2_button_rect.x, 130))
				if self.unit_3_button_rect.collidepoint(self.mouse_pos):
					if self.friendly_money >= unit_info.unit_cost[9]:
						color = (0,0,0)
					else:
						color = (200,0,0)
					text = self.render_text(str(unit_info.unit_cost[9]), self.font_20, color, (self.unit_3_button_rect.x, 130))
	

	def draw_turret_prices(self):
		# draws the price of the turret on mouse hover with color red when not affordable
		if self.turret_menu_open:
			if self.turret_sell_button_rect.collidepoint(self.mouse_pos):
				text = self.render_text("sell for 1/2 the buy price", self.font_12, (0,0,0), (self.turret_1_button_rect.x - 10, 130))
			if self.age == 1:
				if self.turret_1_button_rect.collidepoint(self.mouse_pos):
					if self.friendly_money >= turret_info.turret_cost[1]:
						color = (0,0,0)
					else:
						color = (200,0,0)
					text = self.render_text(str(turret_info.turret_cost[1]), self.font_20, color, (self.turret_1_button_rect.x, 130))
				elif self.turret_2_button_rect.collidepoint(self.mouse_pos):
					if self.friendly_money >= turret_info.turret_cost[2]:
						color = (0,0,0)
					else:
						color = (200,0,0)
					text = self.render_text(str(turret_info.turret_cost[2]), self.font_20, color, (self.turret_2_button_rect.x, 130))
				elif self.turret_3_button_rect.collidepoint(self.mouse_pos):
					if self.friendly_money >= turret_info.turret_cost[3]:
						color = (0,0,0)
					else:
						color = (200,0,0)
					text = self.render_text(str(turret_info.turret_cost[3]), self.font_20, color, (self.turret_3_button_rect.x, 130))
			elif self.age == 2:
				if self.turret_1_button_rect.collidepoint(self.mouse_pos):
					if self.friendly_money >= turret_info.turret_cost[4]:
						color = (0,0,0)
					else:
						color = (200,0,0)
					text = self.render_text(str(turret_info.turret_cost[4]), self.font_20, color, (self.turret_1_button_rect.x, 130))
				elif self.turret_2_button_rect.collidepoint(self.mouse_pos):
					if self.friendly_money >= turret_info.turret_cost[5]:
						color = (0,0,0)
					else:
						color = (200,0,0)
					text = self.render_text(str(turret_info.turret_cost[5]), self.font_20, color, (self.turret_2_button_rect.x, 130))
				elif self.turret_3_button_rect.collidepoint(self.mouse_pos):
					if self.friendly_money >= turret_info.turret_cost[6]:
						color = (0,0,0)
					else:
						color = (200,0,0)
					text = self.render_text(str(turret_info.turret_cost[6]), self.font_20, color, (self.turret_3_button_rect.x, 130))
			elif self.age == 3:
				if self.turret_1_button_rect.collidepoint(self.mouse_pos):
					if self.friendly_money >= turret_info.turret_cost[7]:
						color = (0,0,0)
					else:
						color = (200,0,0)
					text = self.render_text(str(turret_info.turret_cost[7]), self.font_20, color, (self.turret_1_button_rect.x, 130))
				elif self.turret_2_button_rect.collidepoint(self.mouse_pos):
					if self.friendly_money >= turret_info.turret_cost[8]:
						color = (0,0,0)
					else:
						color = (200,0,0)
					text = self.render_text(str(turret_info.turret_cost[8]), self.font_20, color, (self.turret_2_button_rect.x, 130))
				elif self.turret_3_button_rect.collidepoint(self.mouse_pos):
					if self.friendly_money >= turret_info.turret_cost[9]:
						color = (0,0,0)
					else:
						color = (200,0,0)
					text = self.render_text(str(turret_info.turret_cost[9]), self.font_20, color, (self.turret_3_button_rect.x, 130))
	
	def draw_base_upgrade_cost(self):
		if self.friendly_money >= self.upgrade_cost:
			color = (0,0,0)
		else:
			color = (200,0,0)
		if self.unit_menu_open == False and self.turret_menu_open == False and self.friendly_base_upgrade_state != 3 and self.turret_upgrade_button_rect.collidepoint(self.mouse_pos):
			self.render_text(str(self.upgrade_cost), self.font_20, color, (self.turret_upgrade_button_rect.x, 64))

	def draw_age_advancement_cost(self):
		if self.age == 1:
			if self.friendly_exp >= self.age2_treshhold:
				color = (0,0,0)
			else:
				color = (200,0,0)
			if self.unit_menu_open == False and self.turret_menu_open == False and self.age_advance_button_rect.collidepoint(self.mouse_pos):
				self.render_text(f"{round(self.age2_treshhold/1000)}k", self.font_20, color, (self.age_advance_button_rect.x, 64))
		elif self.age == 2:
			if self.friendly_exp >= self.age3_treshhold:
				color = (0,0,0)
			else:
				color = (200,0,0)
			if self.unit_menu_open == False and self.turret_menu_open == False and self.age_advance_button_rect.collidepoint(self.mouse_pos):
				self.render_text(f"{round(self.age3_treshhold/1000)}k", self.font_20, color, (self.age_advance_button_rect.x, 64))
				
	
	def check_game_over_game_won(self):
		if friendly_base.health <= 0:
			self.game_over = True
		elif enemy_base.health <= 0:
			self.game_won = True



	def draw_units_to_menu(self):
		if self.unit_menu_open:
			if self.age == 1:
				unit_1_ui = self.unit_1_sheet.get_image(0, (16, 16), (1,0,0), 1)
				unit_1_ui = pygame.transform.scale(unit_1_ui, (48, 48))
				unit_1_ui.set_colorkey((1,0,0))
				self.screen.blit(unit_1_ui, self.unit_1_button_rect)
	
				unit_2_ui = self.unit_2_sheet.get_image(0, (16, 16), (1,0,0), 1)
				unit_2_ui = pygame.transform.scale(unit_2_ui, (48, 48))
				unit_2_ui.set_colorkey((1,0,0))
				self.screen.blit(unit_2_ui, self.unit_2_button_rect)
	
				unit_3_ui = self.unit_3_sheet.get_image(0, (32, 32), (1,0,0), 1)
				unit_3_ui = pygame.transform.scale(unit_3_ui, (48, 48))
				unit_3_ui.set_colorkey((1,0,0))
				self.screen.blit(unit_3_ui, self.unit_3_button_rect)
			elif self.age == 2:
				unit_1_ui = self.unit_4_sheet.get_image(0, (16, 16), (1,0,0), 1)
				unit_1_ui = pygame.transform.scale(unit_1_ui, (48, 48))
				unit_1_ui.set_colorkey((1,0,0))
				self.screen.blit(unit_1_ui, self.unit_1_button_rect)

				unit_2_ui = self.unit_5_sheet.get_image(0, (16, 16), (1,0,0), 1)
				unit_2_ui = pygame.transform.scale(unit_2_ui, (48, 48))
				unit_2_ui.set_colorkey((1,0,0))
				self.screen.blit(unit_2_ui, self.unit_2_button_rect)

				unit_3_ui = self.unit_6_sheet.get_image(0, (32, 32), (1,0,0), 1)
				unit_3_ui = pygame.transform.scale(unit_3_ui, (48, 48))
				unit_3_ui.set_colorkey((1,0,0))
				self.screen.blit(unit_3_ui, self.unit_3_button_rect)

			elif self.age == 3:
				unit_1_ui = self.unit_7_sheet.get_image(0, (16, 16), (1,0,0), 1)
				unit_1_ui = pygame.transform.scale(unit_1_ui, (48, 48))
				unit_1_ui.set_colorkey((1,0,0))
				self.screen.blit(unit_1_ui, self.unit_1_button_rect)

				unit_2_ui = self.unit_8_sheet.get_image(0, (16, 16), (1,0,0), 1)
				unit_2_ui = pygame.transform.scale(unit_2_ui, (48, 48))
				unit_2_ui.set_colorkey((1,0,0))
				self.screen.blit(unit_2_ui, self.unit_2_button_rect)

				unit_3_ui = self.unit_9_sheet.get_image(0, (32, 32), (1,0,0), 1)
				unit_3_ui = pygame.transform.scale(unit_3_ui, (48, 48))
				unit_3_ui.set_colorkey((1,0,0))
				self.screen.blit(unit_3_ui, self.unit_3_button_rect)

	def draw_turrets_to_menu(self):
		if self.turret_menu_open:
			if self.age == 1:
				turret_1_ui = self.turret_1_sheet.get_image(0, (32, 32), (1,0,0), 1)
				turret_1_ui = pygame.transform.scale(turret_1_ui, (48, 48))
				turret_1_ui.set_colorkey((1,0,0))
				self.screen.blit(turret_1_ui, self.turret_1_button_rect)
	
				turret_2_ui = self.turret_2_sheet.get_image(0, (32, 32), (1,0,0), 1)
				turret_2_ui = pygame.transform.scale(turret_2_ui, (48, 48))
				turret_2_ui.set_colorkey((1,0,0))
				self.screen.blit(turret_2_ui, self.turret_2_button_rect)
	
				turret_3_ui = self.turret_3_sheet.get_image(0, (32, 64), (1,0,0), 1)
				turret_3_ui = pygame.transform.scale(turret_3_ui, (48, 48))
				turret_3_ui.set_colorkey((1,0,0))
				self.screen.blit(turret_3_ui, self.turret_3_button_rect)
			elif self.age == 2:
				turret_1_ui = self.turret_4_sheet.get_image(0, (48, 64), (1,0,0), 1)
				turret_1_ui = pygame.transform.scale(turret_1_ui, (48, 48))
				turret_1_ui.set_colorkey((1,0,0))
				self.screen.blit(turret_1_ui, self.turret_1_button_rect)

				turret_2_ui = self.turret_5_sheet.get_image(0, (48, 64), (1,0,0), 1)
				turret_2_ui = pygame.transform.scale(turret_2_ui, (48, 48))
				turret_2_ui.set_colorkey((1,0,0))
				self.screen.blit(turret_2_ui, self.turret_2_button_rect)

				turret_3_ui = self.turret_6_sheet.get_image(0, (64, 64), (1,0,0), 1)
				turret_3_ui = pygame.transform.scale(turret_3_ui, (64, 64))
				turret_3_ui.set_colorkey((1,0,0))
				self.screen.blit(turret_3_ui, (self.turret_3_button_rect.x - 16, self.turret_3_button_rect.y - 8))

			elif self.age == 3:
				turret_1_ui = self.turret_7_sheet.get_image(0, (64, 64), (1,0,0), 1)
				turret_1_ui = pygame.transform.scale(turret_1_ui, (48, 48))
				turret_1_ui.set_colorkey((1,0,0))
				self.screen.blit(turret_1_ui, self.turret_1_button_rect)

				turret_2_ui = self.turret_8_sheet.get_image(0, (64, 64), (1,0,0), 1)
				turret_2_ui = pygame.transform.scale(turret_2_ui, (48, 48))
				turret_2_ui.set_colorkey((1,0,0))
				self.screen.blit(turret_2_ui, self.turret_2_button_rect)

				turret_3_ui = self.turret_9_sheet.get_image(0, (64, 64), (1,0,0), 1)
				turret_3_ui = pygame.transform.scale(turret_3_ui, (48, 48))
				turret_3_ui.set_colorkey((1,0,0))
				self.screen.blit(turret_3_ui, self.turret_3_button_rect)
	
	def draw_turrets_to_cursor(self):
		if self.turret_buy_mode and self.turret_id_to_buy != 0:
			if self.turret_id_to_buy == 1:
				self.screen.blit(self.turret_1_sheet.get_image(0, (32, 32), (1,0,0), 2), self.mouse_pos)
			if self.turret_id_to_buy == 2:
				self.screen.blit(self.turret_2_sheet.get_image(0, (32, 32), (1,0,0), 2), self.mouse_pos)
			if self.turret_id_to_buy == 3:
				self.screen.blit(self.turret_3_sheet.get_image(0, (32, 64), (1,0,0), 1), self.mouse_pos)
			if self.turret_id_to_buy == 4:
				self.screen.blit(self.turret_4_sheet.get_image(0, (48, 64), (1,0,0), 1), self.mouse_pos)
			if self.turret_id_to_buy == 5:
				self.screen.blit(self.turret_5_sheet.get_image(0, (48, 64), (1,0,0), 1), self.mouse_pos)
			if self.turret_id_to_buy == 6:
				self.screen.blit(self.turret_6_sheet.get_image(0, (64, 64), (1,0,0), 1), self.mouse_pos)
			if self.turret_id_to_buy == 7:
				self.screen.blit(self.turret_7_sheet.get_image(0, (64, 64), (1,0,0), 1), self.mouse_pos)
			if self.turret_id_to_buy == 8:
				self.screen.blit(self.turret_8_sheet.get_image(0, (64, 64), (1,0,0), 1), self.mouse_pos)
			if self.turret_id_to_buy == 9:
				self.screen.blit(self.turret_9_sheet.get_image(0, (64, 64), (1,0,0), 1), self.mouse_pos)

	def age_advancment(self):
		if self.age == 1 and self.friendly_exp >= self.age2_treshhold:
			self.age = 2
		elif self.age == 2 and self.friendly_exp >= self.age3_treshhold:
			self.age = 3



	def buy_turret_friendly(self, id:int, slot:int):
		if self.friendly_money >= turret_info.turret_cost[id] and self.friendly_slots_free[slot] == True:
			turret.spawn_turret(True, id, slot)
			self.friendly_money -= turret_info.turret_cost[id]
			self.friendly_slots_free[slot] = False

	def sell_turret_friendly(self):
		if self.turret_sell_mode:
			for turret in self.friendly_turrets:
				if turret.sell_rect.collidepoint(self.mouse_pos) and pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
					self.clicked = True
					self.friendly_turrets.pop(self.friendly_turrets.index(turret))
					self.friendly_money += turret.sell_value
					self.friendly_slots_free[turret.slot] = True
					self.turret_sell_mode = False

	

	def buy_unit(self, id):
		if self.friendly_money >= unit_info.unit_cost[id]:
			self.friendly_money -= unit_info.unit_cost[id]
			unit.spawn_friendly(id)




	def handle_spawn_queue(self):
		if len(self.friendly_units_queue) != 0:
			if len(self.training) == 0:
				self.training.append(self.friendly_units_queue[0])
				self.friendly_units_queue.pop(0)
		
	def handle_unit_training(self):
		if len(self.training) != 0:
			self.training_timer += 1
			if self.training_timer == self.training_timer_goal:
				self.training_timer = 0
				self.friendly_unit_buffer.append(self.training[0])
				self.training.pop(0)

	def handle_friendly_spawns(self):
		self.handle_spawn_queue()
		self.handle_unit_training()


	def draw_units_in_training(self):
		for unit in self.training:
			self.screen.blit(pygame.transform.scale(unit.frame1_surf, (32, 32)), (16, 16))

	def draw_training_progress_bar(self):
		pygame.draw.rect(self.screen, (100, 200, 100), pygame.Rect(70, 27, self.training_timer * 0.943, 10))


	def render_text(self, text:str, font:pygame.font.Font, color:tuple, pos:tuple):
		text = font.render(text, False, color)
		self.screen.blit(text, pos)


	def draw_money_and_exp(self):
		self.render_text(f"coins: {round(self.friendly_money)}", self.font_20, (0,0,0), (70,1))
		self.render_text(f"e x p: {round(self.friendly_exp)}", self.font_20, (0,0,0), (70,38))

	def draw_free_turret_slots(self):
		if self.turret_buy_mode:
			if self.age == 1:
				if self.friendly_slots_free[1]:
					self.draw_transparent_rect(self.base_upgrade_1_rect.size, (0,255,0), 100, self.friendly_module_pos1_t1)
				if self.friendly_slots_free[2]:
					self.draw_transparent_rect(self.base_upgrade_1_rect.size, (0,255,0), 100, self.friendly_module_pos2_t1)
				if self.friendly_slots_free[3]:
					self.draw_transparent_rect(self.base_upgrade_1_rect.size, (0,255,0), 100, self.friendly_module_pos3_t1)
			if self.age == 2:
				if self.friendly_slots_free[1]:
					self.draw_transparent_rect(self.base_upgrade_1_rect.size, (0,255,0), 100, self.friendly_module_pos1_t2)
				if self.friendly_slots_free[2]:
					self.draw_transparent_rect(self.base_upgrade_1_rect.size, (0,255,0), 100, self.friendly_module_pos2_t2)
				if self.friendly_slots_free[3]:
					self.draw_transparent_rect(self.base_upgrade_1_rect.size, (0,255,0), 100, self.friendly_module_pos3_t2)
			if self.age == 3:
				if self.friendly_slots_free[1]:
					self.draw_transparent_rect(self.base_upgrade_1_rect.size, (0,255,0), 100, self.friendly_module_pos1_t3)
				if self.friendly_slots_free[2]:
					self.draw_transparent_rect(self.base_upgrade_1_rect.size, (0,255,0), 100, self.friendly_module_pos2_t3)
				if self.friendly_slots_free[3]:
					self.draw_transparent_rect(self.base_upgrade_1_rect.size, (0,255,0), 100, self.friendly_module_pos3_t3)

	def draw_sellable_turrets(self):
		if self.turret_sell_mode:
			for turret in self.friendly_turrets:
				self.draw_transparent_rect(turret.sell_rect.size, (255,0,0), 100, turret.sell_rect.topleft)


	def draw_ui(self):
		self.screen.blit(self.ui_main, (0, 0))
		self.screen.blit(self.ui_pause_button, self.pause_button_rect)
		if self.unit_menu_open:
			self.turret_menu_open = False
			self.screen.blit(self.ui_units, (0, 0))
		elif self.turret_menu_open:
			self.unit_menu_open = False
			self.screen.blit(self.ui_turrets, (0, 0))
		self.draw_units_in_training()
		self.draw_training_progress_bar()
		self.draw_units_to_menu()
		self.draw_turrets_to_menu()
		self.draw_money_and_exp()
		self.draw_base_healthbar()
		self.draw_special_cooldown()
		self.draw_unit_prices()
		self.draw_turret_prices()
		self.draw_base_upgrade_cost()
		self.draw_age_advancement_cost()
		self.draw_free_turret_slots()
		self.draw_sellable_turrets()
		self.draw_turrets_to_cursor()

	def move_camera(self):
		if self.pan_left:
			if self.camera_offset_x <= -8:
				self.camera_offset_x += self.camera_move_speed
		elif self.pan_right:
			if self.camera_offset_x >= -1912 + self.SCREEN_SIZE[0]:
				self.camera_offset_x -= self.camera_move_speed
		# moves every object on screen (every static object needs to be moved here)
		self.background_pos = (0 + self.camera_offset_x, -540)
		self.friendly_base_rect.bottomleft = (-50 + self.camera_offset_x, self.FLOOR_LEVEL)
		self.enemy_base_rect.bottomright = (1970 + self.camera_offset_x, self.FLOOR_LEVEL)
		# tier 1 friendly
		self.friendly_module_pos1_t1 = (70 + self.camera_offset_x, 278)
		self.friendly_module_pos2_t1 = (70 + self.camera_offset_x, 278-64)
		self.friendly_module_pos3_t1 = (70 + self.camera_offset_x, 278-128)
		# tier 1 enemy
		self.enemy_module_pos1_t1 = (1850 - 16 + self.camera_offset_x, 278)
		self.enemy_module_pos2_t1 = (1850 - 16 + self.camera_offset_x, 278-64)
		self.enemy_module_pos3_t1 = (1850 - 16 + self.camera_offset_x, 278-128)
		# tier 2 friendly
		self.friendly_module_pos1_t2 = (79 + self.camera_offset_x, 234)
		self.friendly_module_pos2_t2 = (79 + self.camera_offset_x, 234-64)
		self.friendly_module_pos3_t2 = (79 + self.camera_offset_x, 234-128)
		# tier 2 enemy
		self.enemy_module_pos1_t2 = (1841 - 32 + self.camera_offset_x, 234)
		self.enemy_module_pos2_t2 = (1841 - 32 + self.camera_offset_x, 234-64)
		self.enemy_module_pos3_t2 = (1841 - 32 + self.camera_offset_x, 234-128)
		# tier 3 friendly
		self.friendly_module_pos1_t3 = (30 + self.camera_offset_x, 270)
		self.friendly_module_pos2_t3 = (30 + self.camera_offset_x, 270-64)
		self.friendly_module_pos3_t3 = (30 + self.camera_offset_x, 270-128)
		# tier 3 enemy
		self.enemy_module_pos1_t3 = (1890 - 32 + self.camera_offset_x, 270)
		self.enemy_module_pos2_t3 = (1890 - 32 + self.camera_offset_x, 270-64)
		self.enemy_module_pos3_t3 = (1890 - 32 + self.camera_offset_x, 270-128)

		friendly_base.base_rect.x = 0 + self.camera_offset_x
		enemy_base.base_rect.x = 1920 - 150 + self.camera_offset_x

		friendly_base.base_spawn_rect.x = 0 + self.camera_offset_x
		enemy_base.base_spawn_rect.x = 1920 - 100 + self.camera_offset_x




	
	
	# two functions becouse units need to be rendered inbetween the two layers of bases
	def draw_bases_1(self):
		if self.age == 1:
			self.screen.blit(self.friendly_base1_t1, self.friendly_base_rect)
		elif self.age == 2:
			self.screen.blit(self.friendly_base1_t2, self.friendly_base_rect)
		elif self.age == 3:
			self.screen.blit(self.friendly_base1_t3, self.friendly_base_rect)

		if self.enemy_age == 1:
			self.screen.blit(self.enemy_base1_t1, self.enemy_base_rect)
		elif self.enemy_age == 2:
			self.screen.blit(self.enemy_base1_t2, self.enemy_base_rect)
		elif self.enemy_age == 3:
			self.screen.blit(self.enemy_base1_t3, self.enemy_base_rect)

	def draw_bases_2(self):
		if self.age == 1:
			self.screen.blit(self.friendly_base2_t1, self.friendly_base_rect)
		elif self.age == 2:
			self.screen.blit(self.friendly_base2_t2, self.friendly_base_rect)
		elif self.age == 3:
			self.screen.blit(self.friendly_base2_t3, self.friendly_base_rect)

		if self.enemy_age == 1:
			self.screen.blit(self.enemy_base2_t1, self.enemy_base_rect)
		elif self.enemy_age == 2:
			self.screen.blit(self.enemy_base2_t2, self.enemy_base_rect)
		elif self.enemy_age == 3:
			self.screen.blit(self.enemy_base2_t3, self.enemy_base_rect)

	def draw_upgrade_modules(self):

		if self.age == 1:
			self.base_upgrade_1_rect.topleft = self.friendly_module_pos1_t1
			self.base_upgrade_2_rect.topleft = self.friendly_module_pos2_t1
			self.base_upgrade_3_rect.topleft = self.friendly_module_pos3_t1
			module = self.base_upgrade_1
			if self.friendly_base_upgrade_state == 1:
				self.screen.blit(module, self.friendly_module_pos1_t1)
			elif self.friendly_base_upgrade_state == 2:
				self.screen.blit(module, self.friendly_module_pos1_t1)
				self.screen.blit(module, self.friendly_module_pos2_t1)
			elif self.friendly_base_upgrade_state == 3:
				self.screen.blit(module, self.friendly_module_pos1_t1)
				self.screen.blit(module, self.friendly_module_pos2_t1)
				self.screen.blit(module, self.friendly_module_pos3_t1)
		elif self.age == 2:
			self.base_upgrade_1_rect.topleft = self.friendly_module_pos1_t2
			self.base_upgrade_2_rect.topleft = self.friendly_module_pos2_t2
			self.base_upgrade_3_rect.topleft = self.friendly_module_pos3_t2
			module = self.base_upgrade_2
			if self.friendly_base_upgrade_state == 1:
				self.screen.blit(module, self.friendly_module_pos1_t2)
			elif self.friendly_base_upgrade_state == 2:
				self.screen.blit(module, self.friendly_module_pos1_t2)
				self.screen.blit(module, self.friendly_module_pos2_t2)
			elif self.friendly_base_upgrade_state == 3:
				self.screen.blit(module, self.friendly_module_pos1_t2)
				self.screen.blit(module, self.friendly_module_pos2_t2)
				self.screen.blit(module, self.friendly_module_pos3_t2)
		elif self.age == 3:
			self.base_upgrade_1_rect.topleft = self.friendly_module_pos1_t3
			self.base_upgrade_2_rect.topleft = self.friendly_module_pos2_t3
			self.base_upgrade_3_rect.topleft = self.friendly_module_pos3_t3
			module = self.base_upgrade_3
			if self.friendly_base_upgrade_state == 1:
				self.screen.blit(module, self.friendly_module_pos1_t3)
			elif self.friendly_base_upgrade_state == 2:
				self.screen.blit(module, self.friendly_module_pos1_t3)
				self.screen.blit(module, self.friendly_module_pos2_t3)
			elif self.friendly_base_upgrade_state == 3:
				self.screen.blit(module, self.friendly_module_pos1_t3)
				self.screen.blit(module, self.friendly_module_pos2_t3)
				self.screen.blit(module, self.friendly_module_pos3_t3)
		if self.enemy_age == 1:
			self.enemy_base_upgrade_1_rect.topleft = self.enemy_module_pos1_t1
			self.enemy_base_upgrade_2_rect.topleft = self.enemy_module_pos2_t1
			self.enemy_base_upgrade_3_rect.topleft = self.enemy_module_pos3_t1
			module = self.base_upgrade_1
			if self.enemy_base_upgrade_state == 1:
				self.screen.blit(module, self.enemy_module_pos1_t1)
			elif self.enemy_base_upgrade_state == 2:
				self.screen.blit(module, self.enemy_module_pos1_t1)
				self.screen.blit(module, self.enemy_module_pos2_t1)
			elif self.enemy_base_upgrade_state == 3:
				self.screen.blit(module, self.enemy_module_pos1_t1)
				self.screen.blit(module, self.enemy_module_pos2_t1)
				self.screen.blit(module, self.enemy_module_pos3_t1)
		elif self.enemy_age == 2:
			self.enemy_base_upgrade_1_rect.topleft = self.enemy_module_pos1_t2
			self.enemy_base_upgrade_2_rect.topleft = self.enemy_module_pos2_t2
			self.enemy_base_upgrade_3_rect.topleft = self.enemy_module_pos3_t2
			module = self.base_upgrade_2
			if self.enemy_base_upgrade_state == 1:
				self.screen.blit(module, self.enemy_module_pos1_t2)
			elif self.enemy_base_upgrade_state == 2:
				self.screen.blit(module, self.enemy_module_pos1_t2)
				self.screen.blit(module, self.enemy_module_pos2_t2)
			elif self.enemy_base_upgrade_state == 3:
				self.screen.blit(module, self.enemy_module_pos1_t2)
				self.screen.blit(module, self.enemy_module_pos2_t2)
				self.screen.blit(module, self.enemy_module_pos3_t2)
		elif self.enemy_age == 3:
			self.enemy_base_upgrade_1_rect.topleft = self.enemy_module_pos1_t3
			self.enemy_base_upgrade_2_rect.topleft = self.enemy_module_pos2_t3
			self.enemy_base_upgrade_3_rect.topleft = self.enemy_module_pos3_t3
			module = self.base_upgrade_3
			if self.enemy_base_upgrade_state == 1:
				self.screen.blit(module, self.enemy_module_pos1_t3)
			elif self.enemy_base_upgrade_state == 2:
				self.screen.blit(module, self.enemy_module_pos1_t3)
				self.screen.blit(module, self.enemy_module_pos2_t3)
			elif self.enemy_base_upgrade_state == 3:
				self.screen.blit(module, self.enemy_module_pos1_t3)
				self.screen.blit(module, self.enemy_module_pos2_t3)
				self.screen.blit(module, self.enemy_module_pos3_t3)


	def give_money_when_in_dev_mode(self):
		if self.dev_mode:
			self.friendly_money = 99999999
			self.friendly_exp = 99999999


class Base:
	def __init__(self, friendly):
		self.friendly = friendly
		if self.friendly:
			self.base_rect = pygame.Rect(0 + game.camera_offset_x, game.FLOOR_LEVEL - 100, 150, 100)
			self.base_spawn_rect = pygame.Rect(0 + game.camera_offset_x, game.FLOOR_LEVEL - 100, 100, 100)
			self.health = 500

		else:
			self.base_rect = pygame.Rect(1920 - 150 + game.camera_offset_x, game.FLOOR_LEVEL - 100, 150, 100)
			self.base_spawn_rect = pygame.Rect(1920 - 100 + game.camera_offset_x, game.FLOOR_LEVEL - 100, 100, 100)
			self.health = 500

	def get_hurt(self, amount):
		self.health -= amount
		for i in range(5):
			if self.friendly:
				if game.age == 1:
					particle = Particle((132,126,135), (3,3), (self.base_rect.bottomright[0] - 20 + random.randint(-15, 15), self.base_rect.bottomright[1] - 30 + random.randint(-10, 10)), 1, "gravity")
					particle2 = Particle((167,165,167), (3,3), (self.base_rect.bottomright[0] - 20 + random.randint(-15, 15), self.base_rect.bottomright[1] - 30 + random.randint(-10, 10)), 0.3, "friendly_muzzle", 50)
					particle3 = Particle((131,110,100), (5,5), (self.base_rect.bottomright[0] - 20 + random.randint(-15, 15), self.base_rect.bottomright[1] - 30 + random.randint(-10, 10)), 1, "gravity")
				elif game.age == 2:
					particle = Particle((102,57,49), (3,3), (self.base_rect.bottomright[0] - 20 + random.randint(-15, 15), self.base_rect.bottomright[1] - 30 + random.randint(-10, 10)), 1, "gravity")
					particle2 = Particle((115,111,118), (3,3), (self.base_rect.bottomright[0] - 20 + random.randint(-15, 15), self.base_rect.bottomright[1] - 30 + random.randint(-10, 10)), 0.3, "friendly_muzzle", 50)
					particle3 = Particle((126,124,128), (5,5), (self.base_rect.bottomright[0] - 20 + random.randint(-15, 15), self.base_rect.bottomright[1] - 30 + random.randint(-10, 10)), 1, "gravity")
				elif game.age == 3:
					particle = Particle((55,78,32), (3,3), (self.base_rect.bottomright[0] - 20 + random.randint(-15, 15), self.base_rect.bottomright[1] - 30 + random.randint(-10, 10)), 1, "gravity")
					particle2 = Particle((110,157,66), (3,3), (self.base_rect.bottomright[0] - 20 + random.randint(-15, 15), self.base_rect.bottomright[1] - 30 + random.randint(-10, 10)), 0.3, "friendly_muzzle", 50)
					particle3 = Particle((92,128,59), (5,5), (self.base_rect.bottomright[0] - 20 + random.randint(-15, 15), self.base_rect.bottomright[1] - 30 + random.randint(-10, 10)), 1, "gravity")
				
			else:
				if game.enemy_age == 1:
					particle = Particle((132,126,135), (3,3), (self.base_rect.bottomleft[0] + 20 + random.randint(-15, 15), self.base_rect.bottomleft[1] - 30 + random.randint(-10, 10)), 1, "gravity")
					particle2 = Particle((167,165,167), (3,3), (self.base_rect.bottomleft[0] + 20 + random.randint(-15, 15), self.base_rect.bottomleft[1] - 30 + random.randint(-10, 10)), 0.3, "enemy_muzzle", 50)
					particle3 = Particle((131,110,100), (5,5), (self.base_rect.bottomleft[0] + 20 + random.randint(-15, 15), self.base_rect.bottomleft[1] - 30 + random.randint(-10, 10)), 1, "gravity")
				elif game.enemy_age == 2:
					particle = Particle((102,57,49), (3,3), (self.base_rect.bottomleft[0] + 20 + random.randint(-15, 15), self.base_rect.bottomleft[1] - 30 + random.randint(-10, 10)), 1, "gravity")
					particle2 = Particle((115,111,118), (3,3), (self.base_rect.bottomleft[0] + 20 + random.randint(-15, 15), self.base_rect.bottomleft[1] - 30 + random.randint(-10, 10)), 0.3, "enemy_muzzle", 50)
					particle3 = Particle((126,124,128), (5,5), (self.base_rect.bottomleft[0] + 20 + random.randint(-15, 15), self.base_rect.bottomleft[1] - 30 + random.randint(-10, 10)), 1, "gravity")
				elif game.enemy_age == 3:
					particle = Particle((55,78,32), (3,3), (self.base_rect.bottomleft[0] + 20 + random.randint(-15, 15), self.base_rect.bottomleft[1] - 30 + random.randint(-10, 10)), 1, "gravity")
					particle2 = Particle((110,157,66), (3,3), (self.base_rect.bottomleft[0] + 20 + random.randint(-15, 15), self.base_rect.bottomleft[1] - 30 + random.randint(-10, 10)), 0.3, "enemy_muzzle", 50)
					particle3 = Particle((92,128,59), (5,5), (self.base_rect.bottomleft[0] + 20 + random.randint(-15, 15), self.base_rect.bottomleft[1] - 30 + random.randint(-10, 10)), 1, "gravity")
			game.particles.append(particle)
			game.particles.append(particle2)
			game.particles.append(particle3)
	




class Turret:
	def __init__(self, friendly:bool, id:int, slot:int):
		self.id = id
		self.friendly = friendly
		self.slot = slot
		self.damage = turret_info.turret_damage[id]
		self.min_distance = turret_info.turret_min_dist[id]
		self.fire_rate = turret_info.turret_fire_rate[id]
		self.shoottimer = 0
		self.shoottimer_goal = round(60 / self.fire_rate)
		self.units_in_range = []
		self.projectiles = []
		self.cost = turret_info.turret_cost[id]
		self.rotation = 0
		self.sell_value = self.cost/2
		self.range = turret_info.turret_range[id]
		self.frames = turret_info.turret_frames[id]
		self.is_catapult = turret_info.turret_is_catapult[id]
		self.is_static = turret_info.turret_is_static[id]
		self.drawing_line = False
		self.target_pos = (0,0)
		self.animation_state = 0
		self.has_shot = False
		if self.frames > 1:
			self.animation_timer = 0
			self.animation_timer_goal = 60/self.frames


		if self.id == 1:
			self.frame1_surf = game.turret_1_sheet.get_image(0, (32,32), (1,0,0), 2)
		elif self.id == 2:
			self.frame1_surf = game.turret_2_sheet.get_image(0, (32,32), (1,0,0), 2)
		elif self.id == 3:
			self.frame1_surf = game.turret_3_sheet.get_image(0, (64,64), (1,0,0), 2)
		elif self.id == 4:
			self.frame1_surf = game.turret_4_sheet.get_image(0, (64,64), (1,0,0), 2)
		elif self.id == 5:
			self.frame1_surf = game.turret_5_sheet.get_image(0, (64,64), (1,0,0), 1.1)
			self.frame2_surf = game.turret_5_sheet.get_image(1, (64,64), (1,0,0), 1.1)
			self.frame3_surf = game.turret_5_sheet.get_image(2, (64,64), (1,0,0), 1.1)
		elif self.id == 6:
			self.frame1_surf = game.turret_6_sheet.get_image(0, (64,64), (1,0,0), 1.5)
			self.frame2_surf = game.turret_6_sheet.get_image(1, (64,64), (1,0,0), 1.5)
			self.frame3_surf = game.turret_6_sheet.get_image(2, (64,64), (1,0,0), 1.5)
			self.frame4_surf = game.turret_6_sheet.get_image(3, (64,64), (1,0,0), 1.5)
		elif self.id == 7:
			self.frame1_surf = game.turret_7_sheet.get_image(0, (64,64), (1,0,0), 1)
			self.frame2_surf = game.turret_7_sheet.get_image(1, (64,64), (1,0,0), 1)
			self.frame3_surf = game.turret_7_sheet.get_image(2, (64,64), (1,0,0), 1)
			self.frame4_surf = game.turret_7_sheet.get_image(3, (64,64), (1,0,0), 1)
		elif self.id == 8:
			self.frame1_surf = game.turret_8_sheet.get_image(0, (64,64), (1,0,0), 1)
			self.frame2_surf = game.turret_8_sheet.get_image(1, (64,64), (1,0,0), 1)
			self.frame3_surf = game.turret_8_sheet.get_image(2, (64,64), (1,0,0), 1)
			self.frame4_surf = game.turret_8_sheet.get_image(3, (64,64), (1,0,0), 1)
			self.rockets = 2
		elif self.id == 9:
			self.frame1_surf = game.turret_9_sheet.get_image(0, (64,64), (1,0,0), 1)

		self.turret_rect = self.frame1_surf.get_rect()
		self.turret_rect_rotate = self.turret_rect
		self.sell_rect = pygame.Rect(0, 0, self.turret_rect.width/2, self.turret_rect.height/2)
		self.sell_rect.center = self.turret_rect.center

		if not self.friendly:
			self.frame1_surf = pygame.transform.flip(self.frame1_surf, True, False)
			self.frame1_surf.set_colorkey((1,000,000))
			if self.frames > 1:
				self.frame2_surf = pygame.transform.flip(self.frame2_surf, True, False)
				self.frame2_surf.set_colorkey((1,000,000))
				if self.frames > 2:
					self.frame3_surf = pygame.transform.flip(self.frame3_surf, True, False)
					self.frame3_surf.set_colorkey((1,000,000))
					if self.frames > 3:
						self.frame4_surf = pygame.transform.flip(self.frame4_surf, True, False)
						self.frame4_surf.set_colorkey((1,000,000))

		if self.friendly:
			self.turret_range_rect = pygame.Rect(self.turret_rect.right + self.min_distance, 0, self.range, game.FLOOR_LEVEL)
		else:
			self.turret_range_rect = pygame.Rect(self.turret_rect.left - (self.range + self.min_distance), 0, self.range, game.FLOOR_LEVEL)


	
	def update_animation_state(self):
		for turret in game.friendly_turrets + game.enemy_turrets:
			if turret.id == 5:
				if turret.shoottimer == 0:
					turret.animation_state = 0
				elif turret.shoottimer == round(turret.shoottimer_goal/2):
					turret.animation_state = 1
				elif turret.shoottimer == round(turret.shoottimer_goal/1.5):
					turret.animation_state = 2

			elif turret.id == 6:
				if turret.shoottimer == 0:
					turret.animation_state = 1
				elif turret.shoottimer == 5:
					turret.animation_state = 2
				elif turret.shoottimer == 10:
					turret.animation_state = 3
				elif turret.shoottimer == 15:
					turret.animation_state = 0

			elif turret.id == 7:
				if turret.shoottimer == 0:
					turret.animation_state = 1
				elif turret.shoottimer == 3:
					turret.animation_state = 2
				elif turret.shoottimer == 6:
					turret.animation_state = 3
				elif turret.shoottimer == 9:
					turret.animation_state = 0
			
			elif turret.id == 8:
				if turret.rockets == 2:
					turret.animation_state = 0
				elif turret.rockets == 1:
					turret.animation_state = 1
				elif turret.rockets == 0:
					turret.animation_state = 2



	def update_pos(self):
		for turret in game.friendly_turrets:
			if game.age == 1:
				if turret.slot == 1:
					turret.turret_rect.center = (game.friendly_module_pos1_t1[0] + game.base_upgrade_1_rect.width / 2,
												 game.friendly_module_pos1_t1[1] + game.base_upgrade_1_rect.height / 2)
				elif turret.slot == 2:
					turret.turret_rect.center = (game.friendly_module_pos2_t1[0] + game.base_upgrade_2_rect.width / 2,
												 game.friendly_module_pos2_t1[1] + game.base_upgrade_2_rect.height / 2)
				elif turret.slot == 3:
					turret.turret_rect.center = (game.friendly_module_pos3_t1[0] + game.base_upgrade_3_rect.width / 2,
												 game.friendly_module_pos3_t1[1] + game.base_upgrade_3_rect.height / 2)
			elif game.age == 2:
				if turret.slot == 1:
					turret.turret_rect.center = (game.friendly_module_pos1_t2[0] + game.base_upgrade_1_rect.width / 2,
												 game.friendly_module_pos1_t2[1] + game.base_upgrade_1_rect.height / 2)
				elif turret.slot == 2:
					turret.turret_rect.center = (game.friendly_module_pos2_t2[0] + game.base_upgrade_2_rect.width / 2,
												 game.friendly_module_pos2_t2[1] + game.base_upgrade_2_rect.height / 2)
				elif turret.slot == 3:
					turret.turret_rect.center = (game.friendly_module_pos3_t2[0] + game.base_upgrade_3_rect.width / 2,
												 game.friendly_module_pos3_t2[1] + game.base_upgrade_3_rect.height / 2)
			elif game.age == 3:
				if turret.slot == 1:
					turret.turret_rect.center = (game.friendly_module_pos1_t3[0] + game.base_upgrade_1_rect.width / 2,
												 game.friendly_module_pos1_t3[1] + game.base_upgrade_1_rect.height / 2)
				elif turret.slot == 2:
					turret.turret_rect.center = (game.friendly_module_pos2_t3[0] + game.base_upgrade_2_rect.width / 2,
												 game.friendly_module_pos2_t3[1] + game.base_upgrade_2_rect.height / 2)
				elif turret.slot == 3:
					turret.turret_rect.center = (game.friendly_module_pos3_t3[0] + game.base_upgrade_3_rect.width / 2,
												 game.friendly_module_pos3_t3[1] + game.base_upgrade_3_rect.height / 2)
			turret.sell_rect.center = turret.turret_rect.center

		for turret in game.enemy_turrets:
			if game.enemy_age == 1:
				if turret.slot == 1:
					turret.turret_rect.center = (game.enemy_module_pos1_t1[0] + game.base_upgrade_1_rect.width / 2,
												 game.enemy_module_pos1_t1[1] + game.base_upgrade_1_rect.height / 2)
				elif turret.slot == 2:
					turret.turret_rect.center = (game.enemy_module_pos2_t1[0] + game.base_upgrade_2_rect.width / 2,
												 game.enemy_module_pos2_t1[1] + game.base_upgrade_2_rect.height / 2)
				elif turret.slot == 3:
					turret.turret_rect.center = (game.enemy_module_pos3_t1[0] + game.base_upgrade_3_rect.width / 2,
												 game.enemy_module_pos3_t1[1] + game.base_upgrade_3_rect.height / 2)
			elif game.enemy_age == 2:
				if turret.slot == 1:
					turret.turret_rect.center = (game.enemy_module_pos1_t2[0] + game.base_upgrade_1_rect.width / 2,
												 game.enemy_module_pos1_t2[1] + game.base_upgrade_1_rect.height / 2)
				elif turret.slot == 2:
					turret.turret_rect.center = (game.enemy_module_pos2_t2[0] + game.base_upgrade_2_rect.width / 2,
												 game.enemy_module_pos2_t2[1] + game.base_upgrade_2_rect.height / 2)
				elif turret.slot == 3:
					turret.turret_rect.center = (game.enemy_module_pos3_t2[0] + game.base_upgrade_3_rect.width / 2,
												 game.enemy_module_pos3_t2[1] + game.base_upgrade_3_rect.height / 2)
			elif game.enemy_age == 3:
				if turret.slot == 1:
					turret.turret_rect.center = (game.enemy_module_pos1_t3[0] + game.base_upgrade_1_rect.width / 2,
												 game.enemy_module_pos1_t3[1] + game.base_upgrade_1_rect.height / 2)
				elif turret.slot == 2:
					turret.turret_rect.center = (game.enemy_module_pos2_t3[0] + game.base_upgrade_2_rect.width / 2,
												 game.enemy_module_pos2_t3[1] + game.base_upgrade_2_rect.height / 2)
				elif turret.slot == 3:
					turret.turret_rect.center = (game.enemy_module_pos3_t3[0] + game.base_upgrade_3_rect.width / 2,
												 game.enemy_module_pos3_t3[1] + game.base_upgrade_3_rect.height / 2)
		

	def update_range_rect(self):
		if self.friendly:
			self.turret_range_rect = pygame.Rect(self.turret_rect.right + self.min_distance, 0, self.range, game.FLOOR_LEVEL)
		else:
			self.turret_range_rect = pygame.Rect(self.turret_rect.left - (self.range + self.min_distance), 0, self.range, game.FLOOR_LEVEL)


	def update_rotation(self):
		#	for non catapult turrets
		for turret in game.friendly_turrets:
			if not turret.is_catapult and not turret.is_static:
				if  len(turret.units_in_range) > 0:
					# get x and y pos of first unit in turret range
					unit_y = game.FLOOR_LEVEL - turret.units_in_range[0].unit_rect.height / 2
					unit_x = turret.units_in_range[0].unit_rect.x - turret.units_in_range[0].unit_rect.width / 2
					# get x and y pos of turret
					turret_y = turret.turret_rect.center[1]
					turret_x = turret.turret_rect.center[0]
					# calculate differece beweet unit and turret
					delta_y = unit_y - turret_y
					delta_x = unit_x - turret_x
					# calculate rotation angle to point at unit
					if delta_x > 0:
						turret.rotation = round(degrees(atan(delta_y/delta_x))) * -1
				else:
					turret.rotation = 0
		for turret in game.enemy_turrets:
			if not turret.is_catapult and not turret.is_static:
				if len(turret.units_in_range) > 0:
					# get x and y pos of first unit in turret range
					unit_y = game.FLOOR_LEVEL - turret.units_in_range[0].unit_rect.height / 2
					unit_x = turret.units_in_range[0].unit_rect.x + turret.units_in_range[0].unit_rect.width / 2
					# get x and y pos of turret
					turret_y = turret.turret_rect.center[1]
					turret_x = turret.turret_rect.center[0]
					# calculate differece beweet unit and turret
					delta_y = unit_y - turret_y
					delta_x = turret_x - unit_x
					# calculate rotation angle to point at unit
					if delta_x > 0:
						turret.rotation = round(degrees(atan(delta_y/delta_x)))
				else:
					turret.rotation = 0


	
	def attack_static(self):
		for turret in game.friendly_turrets:
			if turret.is_static and len(turret.units_in_range) > 0:
				turret.target_pos = turret.units_in_range[0].unit_rect.center
				turret.shoottimer += 1
				if turret.shoottimer >= turret.shoottimer_goal / 2:
					turret.drawing_line = True

				if turret.shoottimer >= turret.shoottimer_goal + random.randint(1,30):
					turret.drawing_line = False
					turret.shoottimer = 0
					if turret.units_in_range[0].moving:
						projectile = Projectile((turret.units_in_range[0].unit_rect.center[0] - unit.movement_speed* 240 + random.randint(-20,20), -32 - random.randint(1,32)), (0,1), 0, turret.id, True)
					else:
						projectile = Projectile((turret.units_in_range[0].unit_rect.center[0] - 180 + random.randint(-20,20), -32 - random.randint(1,32)), (0,0), 0, turret.id, True)
					turret.projectiles.append(projectile)

		for turret in game.enemy_turrets:
			if turret.is_static and len(turret.units_in_range) > 0:
				turret.target_pos = turret.units_in_range[0].unit_rect.center
				turret.shoottimer += 1
				if turret.shoottimer >= turret.shoottimer_goal / 2:
					turret.drawing_line = True

				if turret.shoottimer >= turret.shoottimer_goal + random.randint(1,30):
					turret.drawing_line = False
					turret.shoottimer = 0
					if turret.units_in_range[0].moving:
						projectile = Projectile((turret.units_in_range[0].unit_rect.center[0] + unit.movement_speed* 240 + random.randint(-20,20), -32 - random.randint(1,32)), (0,1), 0, turret.id, False)
					else:
						projectile = Projectile((turret.units_in_range[0].unit_rect.center[0] + 180 + random.randint(-20,20), -32 - random.randint(1,32)), (0,0), 0, turret.id, False)
					turret.projectiles.append(projectile)


	def attack_catapult(self):
		for turret in game.friendly_turrets:
			if turret.is_catapult and len(turret.units_in_range) > 0:
				if not turret.has_shot:
					turret.shoottimer += 1
					if turret.shoottimer >= turret.shoottimer_goal:
						turret.rotation -= 10
						if turret.rotation <= -120:
							projectile = Projectile(turret.turret_rect.midtop, 
							(turret.units_in_range[0].unit_rect.center[0] - turret.turret_rect.midtop[0],
							turret.units_in_range[0].unit_rect.center[1] - turret.turret_rect.midtop[1]),
							10, turret.id, True)
							turret.projectiles.append(projectile)
							turret.has_shot = True
							turret.shoottimer = 0

				else:
					turret.rotation += 2
					if turret.rotation >= 0:
						turret.has_shot = False
			elif turret.is_catapult and len(turret.units_in_range) == 0 and turret.rotation < 0:
				turret.rotation += 2

		for turret in game.enemy_turrets:
			if turret.is_catapult and len(turret.units_in_range) > 0:
				if not turret.has_shot:
					turret.shoottimer += 1
					if turret.shoottimer >= turret.shoottimer_goal:
						turret.rotation += 10
						if turret.rotation >= 120:
							projectile = Projectile(turret.turret_rect.midtop, 
							(turret.turret_rect.midtop[0] - turret.units_in_range[0].unit_rect.center[0],
							turret.units_in_range[0].unit_rect.center[1] - turret.turret_rect.midtop[1]),
							10, turret.id, False)
							turret.projectiles.append(projectile)
							turret.has_shot = True
							turret.shoottimer = 0

				else:
					turret.rotation -= 2
					if turret.rotation <= 0:
						turret.has_shot = False
			elif turret.is_catapult and len(turret.units_in_range) == 0 and turret.rotation > 0:
				turret.rotation -= 2




	def rotate_turret(self):
		if self.animation_state == 0:
			rotated_surf = pygame.transform.rotate(self.frame1_surf, self.rotation)
			rotated_surf.set_colorkey((1,0,0))
			self.turret_rect_rotate = rotated_surf.get_rect(center= self.turret_rect.center)
		elif self.animation_state == 1:
			rotated_surf = pygame.transform.rotate(self.frame2_surf, self.rotation)
			rotated_surf.set_colorkey((1,0,0))
			self.turret_rect_rotate = rotated_surf.get_rect(center= self.turret_rect.center)
		elif self.animation_state == 2:
			rotated_surf = pygame.transform.rotate(self.frame3_surf, self.rotation)
			rotated_surf.set_colorkey((1,0,0))
			self.turret_rect_rotate = rotated_surf.get_rect(center= self.turret_rect.center)
		elif self.animation_state == 3:
			rotated_surf = pygame.transform.rotate(self.frame4_surf, self.rotation)
			rotated_surf.set_colorkey((1,0,0))
			self.turret_rect_rotate = rotated_surf.get_rect(center= self.turret_rect.center)
		return rotated_surf


	def find_first_enemy_in_range(self):
		for turret in game.friendly_turrets:
			turret.update_range_rect()
			for unit in game.enemy_units:
				if unit.unit_rect.colliderect(turret.turret_range_rect) and not unit in turret.units_in_range:
					turret.units_in_range.append(unit)
				if not unit.unit_rect.colliderect(turret.turret_range_rect) and unit in turret.units_in_range:
					turret.units_in_range.pop(turret.units_in_range.index(unit))
					turret.shoottimer = 0
		for turret in game.enemy_turrets:
			turret.update_range_rect()
			for unit in game.friendly_units:
				if unit.unit_rect.colliderect(turret.turret_range_rect) and not unit in turret.units_in_range:
					turret.units_in_range.append(unit)
				if not unit.unit_rect.colliderect(turret.turret_range_rect) and unit in turret.units_in_range:
					turret.units_in_range.pop(turret.units_in_range.index(unit))
					turret.shoottimer = 0

	def shoot_enemy(self):
		for turret in game.friendly_turrets:
			if not turret.is_catapult and not turret.is_static:
				if len(turret.units_in_range) > 0:
					turret.shoottimer += 1
					if turret.id == 8:
						if turret.rockets == 0 and turret.shoottimer == round(turret.shoottimer_goal/2):
							turret.rockets = 2
					if turret.shoottimer == turret.shoottimer_goal:
						turret.shoottimer = 0
						if turret.id != 8:
							projectile = Projectile(turret.turret_rect.center,
							 (turret.units_in_range[0].unit_rect.center[0] - turret.turret_rect.center[0],
							  turret.units_in_range[0].unit_rect.center[1] - turret.turret_rect.center[1]),
							  turret.rotation, turret.id, True)
						else:
							if turret.rockets == 2:
								projectile = Projectile((turret.turret_rect.center[0], turret.turret_rect.center[1] - 7),
							 (turret.units_in_range[0].unit_rect.center[0] - turret.turret_rect.center[0],
							  turret.units_in_range[0].unit_rect.center[1] - turret.turret_rect.center[1]),
							  turret.rotation, turret.id, True)
							elif turret.rockets == 1:
								projectile = Projectile((turret.turret_rect.center[0], turret.turret_rect.center[1] + 7),
							 (turret.units_in_range[0].unit_rect.center[0] - turret.turret_rect.center[0],
							  turret.units_in_range[0].unit_rect.center[1] - turret.turret_rect.center[1]),
							  turret.rotation, turret.id, True)

						turret.projectiles.append(projectile)
						if turret.id == 8:
							if turret.rockets > 0:
								turret.rockets -= 1
							
		
		for turret in game.enemy_turrets:
			if not turret.is_catapult and not turret.is_static:
				if len(turret.units_in_range) > 0:
					turret.shoottimer += 1
					if turret.shoottimer == turret.shoottimer_goal:
						turret.shoottimer = 0
						projectile = Projectile(turret.turret_rect.center,
						 (turret.turret_rect.center[0] - turret.units_in_range[0].unit_rect.center[0],
						  turret.units_in_range[0].unit_rect.center[1] - turret.turret_rect.center[1]),
						  turret.rotation , turret.id, False)
						turret.projectiles.append(projectile)




	def remove_unit_from_list_if_dead(self):
		for turret in game.friendly_turrets:
			turret_range_rect = pygame.Rect(turret.turret_rect.right, 0, turret.range, game.FLOOR_LEVEL)
			for unit in turret.units_in_range:
				if not unit in game.enemy_units or not unit.unit_rect.colliderect(turret_range_rect):
					turret.units_in_range.pop(turret.units_in_range.index(unit))

		for turret in game.enemy_turrets:
			turret_range_rect = pygame.Rect(turret.turret_rect.left - turret.range, 0, turret.range, game.FLOOR_LEVEL)
			for unit in turret.units_in_range:
				if not unit in game.friendly_units or not unit.unit_rect.colliderect(turret_range_rect):
					turret.units_in_range.pop(turret.units_in_range.index(unit))


	def spawn_turret(self, friendly:bool, id:int, slot:int):
		turret = Turret(friendly, id, slot)
		if friendly:
			game.friendly_turrets.append(turret)
		else:
			game.enemy_turrets.append(turret)

	def sell(self):
		if self.friendly:
			game.friendly_turrets.pop(game.friendly_turrets.index(self))
			game.friendly_slots_free[self.slot] = True

	def draw(self):
		for turret in game.friendly_turrets:
			game.screen.blit(turret.rotate_turret(), turret.turret_rect_rotate)
			if game.dev_mode:
				game.draw_transparent_rect(turret.turret_range_rect.size, (0,255,0), 50, turret.turret_range_rect.topleft)
			if turret.drawing_line:
				pygame.draw.line(game.screen, (200,0,0), (turret.turret_rect.midright[0] - 5, turret.turret_rect.midright[1] + 6), turret.target_pos)
		for turret in game.enemy_turrets:
			game.screen.blit(turret.rotate_turret(), turret.turret_rect_rotate)
			if game.dev_mode:
				game.draw_transparent_rect(turret.turret_range_rect.size, (255,0,0), 50, turret.turret_range_rect.topleft)
			if turret.drawing_line:
				pygame.draw.line(game.screen, (200,0,0), (turret.turret_rect.midleft[0] + 5, turret.turret_rect.midleft[1] + 6), turret.target_pos)

		

	def update(self):
		self.update_pos()
		self.update_rotation()
		self.find_first_enemy_in_range()
		self.remove_unit_from_list_if_dead()
		self.update_animation_state()
		self.shoot_enemy()
		self.attack_catapult()
		self.attack_static()




class Projectile:
	def __init__(self, starting_pos:tuple, direction:tuple, angle:int, id:int, friendly:bool):
		self.starting_pos = starting_pos
		self.x_pos = self.starting_pos[0]
		self.y_pos = self.starting_pos[1]
		self.camera_offset_x = game.camera_offset_x
		self.direction = direction
		self.friendly = friendly
		self.rotation = angle
		self.falling_vel = 0
		self.forward_vel = 3
		self.id = id
		self.vel = projectile_info.projectile_vel[self.id]
		self.animation_state = 0
		if self.id == 1:
			self.frame1_surf = game.projectile_1_sheet.get_image(0, (8,8), (1,0,0), 1)
		elif self.id == 2:
			self.frame1_surf = game.projectile_2_sheet.get_image(0, (8,8), (1,0,0), 1)
		elif self.id == 3:
			self.frame1_surf = game.projectile_3_sheet.get_image(0, (16,16), (1,0,0), 1)
		elif self.id == 4:
			self.frame1_surf = game.projectile_4_sheet.get_image(0, (16,16), (1,0,0), 1)
		elif self.id == 5:
			self.frame1_surf = game.projectile_5_sheet.get_image(0, (32, 9), (1,0,0), 1)
		elif self.id == 6:
			self.frame1_surf = game.projectile_6_sheet.get_image(0, (16,16), (1,0,0), 0.7)
		elif self.id == 7:
			self.frame1_surf = game.projectile_7_sheet.get_image(0, (16, 3), (1,0,0), 1)
		elif self.id == 8:
			self.frame1_surf = game.projectile_8_sheet.get_image(0, (32, 7), (1,0,0), 1)
			self.frame2_surf = game.projectile_8_sheet.get_image(1, (32, 7), (1,0,0), 1)
		elif self.id == 9:
			self.frame1_surf = game.projectile_9_sheet.get_image(0, (32,16), (1,0,0), 1)

		self.rect = self.frame1_surf.get_rect(center= self.starting_pos)
		self.rect_rotate = self.rect
		if not self.friendly:
			if self.id != 8:
				self.frame1_surf = pygame.transform.flip(self.frame1_surf, True, False)
				self.frame1_surf.set_colorkey((1,0,0))
			elif self.id == 8:
				self.frame1_surf = pygame.transform.flip(self.frame1_surf, True, False)
				self.frame1_surf.set_colorkey((1,0,0))
				self.frame2_surf = pygame.transform.flip(self.frame2_surf, True, False)
				self.frame2_surf.set_colorkey((1,0,0))



	def rotate_image(self):
		if self.animation_state == 0:
			rotated_surf = pygame.transform.rotate(self.frame1_surf, self.rotation)
			rotated_surf.set_colorkey((1,0,0))
			self.rect_rotate = rotated_surf.get_rect(center= self.rect.center)
		elif self.animation_state == 1:
			rotated_surf = pygame.transform.rotate(self.frame2_surf, self.rotation)
			rotated_surf.set_colorkey((1,0,0))
			self.rect_rotate = rotated_surf.get_rect(center= self.rect.center)
		return rotated_surf

	def move(self):
		for turret in game.friendly_turrets:
			for projectile in turret.projectiles:
				x_camera_offset_dif = projectile.camera_offset_x - game.camera_offset_x
				if projectile.id != 9:
					projectile.x_pos += projectile.direction[0] * projectile.vel
					projectile.y_pos += projectile.direction[1] * projectile.vel
				else:
					projectile.falling_vel += 0.2
					if projectile.forward_vel > 0:
						projectile.forward_vel -= 0.01

					projectile.x_pos += projectile.forward_vel
					projectile.y_pos += projectile.falling_vel
					projectile.get_rotation_angle()
					
				projectile.rect.center = (projectile.x_pos - x_camera_offset_dif, projectile.y_pos)
				if projectile.rect.y >= 600:
					turret.projectiles.pop(turret.projectiles.index(projectile))


		for turret in game.enemy_turrets:
			for projectile in turret.projectiles:
				x_camera_offset_dif = projectile.camera_offset_x - game.camera_offset_x
				if projectile.id != 9:
					projectile.x_pos += projectile.direction[0] * projectile.vel * -1
					projectile.y_pos += projectile.direction[1] * projectile.vel
				else:
					projectile.falling_vel += 0.2
					if projectile.forward_vel < 0:
						projectile.forward_vel += 0.01

					projectile.x_pos -= projectile.forward_vel
					projectile.y_pos += projectile.falling_vel
					projectile.get_rotation_angle()
	
				projectile.rect.center = (projectile.x_pos - x_camera_offset_dif, projectile.y_pos)
				if projectile.rect.y >= 600:
					turret.projectiles.pop(turret.projectiles.index(projectile))
	

	def get_rotation_angle(self):
		if self.id == 9:
			if self.friendly:
				max_rotation = 90 / game.FLOOR_LEVEL
				current_rotation = max_rotation * self.y_pos
				self.rotation = current_rotation * -1
			else:
				max_rotation = 90 / game.FLOOR_LEVEL
				current_rotation = max_rotation * self.y_pos
				self.rotation = current_rotation



	def check_for_collision(self):
		for turret in game.friendly_turrets:
			for projectile in turret.projectiles:
				for unit in turret.units_in_range:
					if unit.unit_rect.colliderect(projectile.rect):
						try:
							unit.get_hurt(turret_info.turret_damage[projectile.id])
							turret.projectiles.pop(turret.projectiles.index(projectile))
							if projectile.id == 1:
								blood_master.spawn_cluster(projectile.rect.center, True, (100,255,100), (2,2), False, 4)
							elif projectile.id == 2:
								blood_master.spawn_cluster(projectile.rect.center, True, "yellow", (2,2), False, 1)
								blood_master.spawn_cluster(projectile.rect.center, True, "white", (2,2), False, 1)
							elif projectile.id == 5:
								blood_master.spawn_cluster(projectile.rect.center, True, (139,69,19), (5,5), False, 4)
							elif projectile.id == 6:
								blood_master.spawn_cluster(projectile.rect.center, True, (40,40,40), (6,6), False, 4)
							elif projectile.id == 7:
								blood_master.spawn_cluster(projectile.rect.center, True, "yellow", (1,1), False, 3)
							elif projectile.id == 8:
								particle.spawn_explosion(projectile.rect.center, (30,30,30), 1, (255,100,0), 0.3, (255,165,0), 0.7, (4,4), 5)
							elif projectile.id == 9:
								particle.spawn_explosion(projectile.rect.center, (30,30,30), 1, (255,100,0), 0.3, (255,165,0), 0.7, (4,4), 10)

						except ValueError:
							print("ValueError in turret projectile check collision friendly")

		for turret in game.enemy_turrets:
			for projectile in turret.projectiles:
				for unit in turret.units_in_range:
					if unit.unit_rect.colliderect(projectile.rect):
						try:
							unit.get_hurt(turret_info.turret_damage[projectile.id])
							turret.projectiles.pop(turret.projectiles.index(projectile))
							if projectile.id == 1:
								blood_master.spawn_cluster(projectile.rect.center, True, (100,255,100), (2,2), False, 4)
							elif projectile.id == 2:
								blood_master.spawn_cluster(projectile.rect.center, True, "yellow", (2,2), False, 1)
								blood_master.spawn_cluster(projectile.rect.center, True, "white", (2,2), False, 1)
							elif projectile.id == 5:
								blood_master.spawn_cluster(projectile.rect.center, True, (139,69,19), (5,5), False, 4)
							elif projectile.id == 6:
								blood_master.spawn_cluster(projectile.rect.center, True, (40,40,40), (6,6), False, 4)
							elif projectile.id == 7:
								blood_master.spawn_cluster(projectile.rect.center, True, "yellow", (1,1), False, 3)
							elif projectile.id == 8:
								particle.spawn_explosion(projectile.rect.center, (30,30,30), 1, (255,100,0), 0.3, (255,165,0), 0.7, (4,4), 5)
							elif projectile.id == 9:
								particle.spawn_explosion(projectile.rect.center, (30,30,30), 1, (255,100,0), 0.3, (255,165,0), 0.7, (4,4), 10)

						except ValueError:
							print("ValueError in turret projectile check collision enemy")

	def update(self):
		projectile.move()
		projectile.check_for_collision()

		
	
				
	

	def draw(self):
		for turret in game.friendly_turrets:
			for bullet in turret.projectiles:
				game.screen.blit(bullet.rotate_image(), bullet.rect_rotate)

		for turret in game.enemy_turrets:
			for bullet in turret.projectiles:
				game.screen.blit(bullet.rotate_image(), bullet.rect_rotate)
	






class Unit:
	# universal unit class for both enemy and friendly units
	def __init__(self, friendly:bool, id:int):
		self.friendly = friendly
		self.id = id
		self.moving = True
		self.has_weapon = unit_info.has_weapon[id]
		self.rotation = 0
		self.scale = 1
		if self.has_weapon:
			self.weapon_rotation = 0
			self.idle_swinging_direction = 0
		self.movement_speed = 1
		self.fall_speed = 0
		self.ranged = unit_info.is_unit_ranged[self.id]
		self.cost = unit_info.unit_cost[self.id]
		self.exp_value = unit_info.unit_cost[self.id]
		self.kill_value = unit_info.unit_cost[self.id]
		self.health = unit_info.unit_health[self.id]
		self.damage = unit_info.unit_damage[self.id]
		self.animation_frames = unit_info.animation_frames[self.id]
		self.animation_state = 0
		self.animation_timer = 0
		self.animation_timer_goal = 60 / unit_info.animation_frames[self.id]
		self.attack_timer = 0
		self.attack_timer_goal = 2 * 60
		if self.ranged:
			self.unit_in_range = False
			self.projectiles = []

		# extracts the animation frames from spritesheet using the get_image method
		if self.id == 1:
			self.frame1_surf = game.unit_1_sheet.get_image(0, (16, 16), (1, 0, 0), 2)
			self.frame2_surf = game.unit_1_sheet.get_image(1, (16, 16), (1, 0, 0), 2)
			self.frame3_surf = game.unit_1_sheet.get_image(2, (16, 16), (1, 0, 0), 2)
			self.frame4_surf = game.unit_1_sheet.get_image(3, (16, 16), (1, 0, 0), 2)
			self.unit_rect = self.frame1_surf.get_rect()
			self.unit_rect_rotate = self.unit_rect

			self.weapon_surf = game.weapon_1_sheet.get_image(0, (128,128), (1,0,0), 0.6)
			self.weapon_rect = self.weapon_surf.get_rect()
			self.weapon_rect_rotate = self.weapon_rect
			self.weapon_offset_x = 4
			self.weapon_offset_y = 4
			self.idle_swinging_distance = 30
			self.idle_swinging_speed = 0.7

		elif self.id == 2:
			self.frame1_surf = game.unit_2_sheet.get_image(0, (16, 16), (1, 0, 0), 2)
			self.frame2_surf = game.unit_2_sheet.get_image(1, (16, 16), (1, 0, 0), 2)
			self.frame3_surf = game.unit_2_sheet.get_image(2, (16, 16), (1, 0, 0), 2)
			self.frame4_surf = game.unit_2_sheet.get_image(3, (16, 16), (1, 0, 0), 2)
			self.unit_rect = self.frame1_surf.get_rect()
			self.unit_rect_rotate = self.unit_rect

			self.weapon_surf = game.weapon_2_sheet.get_image(0, (128,128), (1,0,0), 0.6)
			self.weapon_surf2 = game.weapon_2_sheet.get_image(1, (128,128), (1,0,0), 0.6)
			self.weapon_rect = self.weapon_surf.get_rect()
			self.weapon_rect_rotate = self.weapon_rect
			self.weapon_offset_x = 6
			self.weapon_offset_y = 3
			self.idle_swinging_distance = 30
			self.idle_swinging_speed = 0.7
			self.weapon_animation_state = 0

		elif self.id == 3:
			self.frame1_surf = game.unit_3_sheet.get_image(0, (32, 32), (1, 0, 0), 2)
			self.frame2_surf = game.unit_3_sheet.get_image(1, (32, 32), (1, 0, 0), 2)
			self.frame3_surf = game.unit_3_sheet.get_image(0, (32, 32), (1, 0, 0), 2)
			self.frame4_surf = game.unit_3_sheet.get_image(1, (32, 32), (1, 0, 0), 2)
			self.unit_rect = self.frame1_surf.get_rect()
			self.unit_rect_rotate = self.unit_rect

			self.weapon_surf = game.weapon_3_sheet.get_image(0, (128,128), (1,0,0), 0.6)
			self.weapon_rect = self.weapon_surf.get_rect()
			self.weapon_rect_rotate = self.weapon_rect
			self.weapon_offset_x = 4
			self.weapon_offset_y = 4
			self.idle_swinging_distance = 15
			self.idle_swinging_speed = 0.3

		elif self.id == 4:
			self.frame1_surf = game.unit_4_sheet.get_image(0, (16, 16), (1, 0, 0), 2)
			self.frame2_surf = game.unit_4_sheet.get_image(1, (16, 16), (1, 0, 0), 2)
			self.frame3_surf = game.unit_4_sheet.get_image(2, (16, 16), (1, 0, 0), 2)
			self.frame4_surf = game.unit_4_sheet.get_image(3, (16, 16), (1, 0, 0), 2)
			self.unit_rect = self.frame1_surf.get_rect()
			self.unit_rect_rotate = self.unit_rect

			self.weapon_surf = game.weapon_4_sheet.get_image(0, (128,128), (1,0,0), 0.7)
			self.weapon_rect = self.weapon_surf.get_rect()
			self.weapon_rect_rotate = self.weapon_rect
			self.weapon_offset_x = 4
			self.weapon_offset_y = 4
			self.idle_swinging_distance = 25
			self.idle_swinging_speed = 0.7

		elif self.id == 5:
			self.frame1_surf = game.unit_5_sheet.get_image(0, (16, 16), (1, 0, 0), 2)
			self.frame2_surf = game.unit_5_sheet.get_image(1, (16, 16), (1, 0, 0), 2)
			self.frame3_surf = game.unit_5_sheet.get_image(2, (16, 16), (1, 0, 0), 2)
			self.frame4_surf = game.unit_5_sheet.get_image(3, (16, 16), (1, 0, 0), 2)
			self.unit_rect = self.frame1_surf.get_rect()
			self.unit_rect_rotate = self.unit_rect

			self.weapon_surf = game.weapon_5_sheet.get_image(0, (128,128), (1,0,0), 0.6)
			self.weapon_surf2 = game.weapon_5_sheet.get_image(1, (128,128), (1,0,0), 0.6)
			self.weapon_rect = self.weapon_surf.get_rect()
			self.weapon_rect_rotate = self.weapon_rect
			self.weapon_offset_x = 7
			self.weapon_offset_y = 4
			self.idle_swinging_distance = 30
			self.idle_swinging_speed = 0.7
			self.weapon_animation_state = 0

		elif self.id == 6:
			self.frame1_surf = game.unit_6_sheet.get_image(0, (32, 32), (1, 0, 0), 2)
			self.frame2_surf = game.unit_6_sheet.get_image(1, (32, 32), (1, 0, 0), 2)
			self.frame3_surf = game.unit_6_sheet.get_image(2, (32, 32), (1, 0, 0), 2)
			self.frame4_surf = game.unit_6_sheet.get_image(3, (32, 32), (1, 0, 0), 2)
			self.unit_rect = self.frame1_surf.get_rect()
			self.unit_rect_rotate = self.unit_rect

			self.weapon_surf = game.weapon_6_sheet.get_image(0, (128,128), (1,0,0), 0.6)
			self.weapon_rect = self.weapon_surf.get_rect()
			self.weapon_rect_rotate = self.weapon_rect
			self.weapon_offset_x = 3
			self.weapon_offset_y = 0
			self.idle_swinging_distance = 10
			self.idle_swinging_speed = 0.2
			self.units_in_range = []

		elif self.id == 7:
			self.frame1_surf = game.unit_7_sheet.get_image(0, (16, 16), (1, 0, 0), 2)
			self.frame2_surf = game.unit_7_sheet.get_image(1, (16, 16), (1, 0, 0), 2)
			self.frame3_surf = game.unit_7_sheet.get_image(2, (16, 16), (1, 0, 0), 2)
			self.frame4_surf = game.unit_7_sheet.get_image(3, (16, 16), (1, 0, 0), 2)
			self.unit_rect = self.frame1_surf.get_rect()
			self.unit_rect_rotate = self.unit_rect

			self.weapon_surf = game.weapon_7_sheet.get_image(0, (128,128), (1,0,0), 0.6)
			self.weapon_surf2 = game.weapon_7_sheet.get_image(1, (128,128), (1,0,0), 0.6)
			self.weapon_rect = self.weapon_surf.get_rect()
			self.weapon_rect_rotate = self.weapon_rect
			self.weapon_offset_x = 7
			self.weapon_offset_y = 2
			self.idle_swinging_distance = 14
			self.idle_swinging_speed = 0.4
			self.weapon_animation_state = 0
			self.shooting_timer = 0
			self.shooting_timer_goal = 10
			self.shooting = False

		elif self.id == 8:
			self.frame1_surf = game.unit_8_sheet.get_image(0, (16, 16), (1, 0, 0), 2)
			self.frame2_surf = game.unit_8_sheet.get_image(1, (16, 16), (1, 0, 0), 2)
			self.frame3_surf = game.unit_8_sheet.get_image(2, (16, 16), (1, 0, 0), 2)
			self.frame4_surf = game.unit_8_sheet.get_image(3, (16, 16), (1, 0, 0), 2)
			self.unit_rect = self.frame1_surf.get_rect()
			self.unit_rect_rotate = self.unit_rect

			self.weapon_surf = game.weapon_8_sheet.get_image(0, (128,128), (1,0,0), 0.7)
			self.weapon_rect = self.weapon_surf.get_rect()
			self.weapon_rect_rotate = self.weapon_rect
			self.weapon_offset_x = 7
			self.weapon_offset_y = 2
			self.idle_swinging_distance = 30
			self.idle_swinging_speed = 0.7

		elif self.id == 9:
			self.frame1_surf = game.unit_9_sheet.get_image(0, (32, 32), (1, 0, 0), 3)
			self.frame2_surf = game.unit_9_sheet.get_image(1, (32, 32), (1, 0, 0), 3)
			self.frame3_surf = game.unit_9_sheet.get_image(2, (32, 32), (1, 0, 0), 3)
			self.frame4_surf = game.unit_9_sheet.get_image(3, (32, 32), (1, 0, 0), 3)
			self.unit_rect = self.frame1_surf.get_rect()
			self.unit_rect_rotate = self.unit_rect

		self.height = self.unit_rect.height
		self.width = self.unit_rect.width

		if not self.id == 6:
			self.crown_frame1 = game.buffed_crown_sheet.get_image(0, (13,6), (1,0,0), 2)
			self.crown_frame2 = game.buffed_crown_sheet.get_image(1, (13,6), (1,0,0), 2)
			self.crown_frame3 = game.buffed_crown_sheet.get_image(2, (13,6), (1,0,0), 2)
			self.crown_frame4 = game.buffed_crown_sheet.get_image(3, (13,6), (1,0,0), 2)
			self.crown_rect = self.crown_frame1.get_rect()
			self.crown_animation_state = 0
			self.crown_animation_timer = 0
			self.crown_animation_timer_goal = 60
			self.buffed = False
			self.buff_timer = 0
			self.buff_timer_goal = 3 * 60
			self.crown_floating_direction = 0
			self.crown_y_offset = 0

		
			# flip the unit if its from the enemy
		if not self.friendly:
			self.x_pos = 1920 - 32
			self.frame1_surf = pygame.transform.flip(self.frame1_surf, True, False)
			self.frame1_surf.set_colorkey((1,000,000))
			self.frame2_surf = pygame.transform.flip(self.frame2_surf, True, False)
			self.frame2_surf.set_colorkey((1,000,000))
			self.frame3_surf = pygame.transform.flip(self.frame3_surf, True, False)
			self.frame3_surf.set_colorkey((1,000,000))
			self.frame4_surf = pygame.transform.flip(self.frame4_surf, True, False)
			self.frame4_surf.set_colorkey((1,000,000))

			if self.has_weapon:
				self.weapon_surf = pygame.transform.flip(self.weapon_surf, True, False)
				self.weapon_surf.set_colorkey((1,0,0))

			if self.id == 2 or self.id == 5 or self.id == 7:
				self.weapon_surf2 = pygame.transform.flip(self.weapon_surf2, True, False)
				self.weapon_surf2.set_colorkey((1,0,0))

		else:
			self.x_pos = 32

		self.unit_rect.bottomleft = (self.x_pos, game.FLOOR_LEVEL)
		
		# create smaller rect infront of the unit to make it stop when in combat
		if self.friendly:
			self.front_rect = pygame.Rect(self.x_pos + self.unit_rect.width, game.FLOOR_LEVEL, 6, self.unit_rect.height)
			self.front_rect.bottom = game.FLOOR_LEVEL

		else:
			self.front_rect = pygame.Rect(self.x_pos - self.unit_rect.width, game.FLOOR_LEVEL, 6, self.unit_rect.height)
			self.front_rect.bottom = game.FLOOR_LEVEL


		if self.ranged and self.friendly:
			self.range_rect = pygame.Rect(self.unit_rect.topright[0], self.unit_rect.topright[1], 96, self.unit_rect.height)
		if self.ranged and not self.friendly:
			self.range_rect = pygame.Rect(self.unit_rect.topleft[0], self.unit_rect.topleft[1], 96, self.unit_rect.height)
		elif not self.ranged:
			self.melee_combat = False


	def rotate_and_scale(self):
		if self.animation_state == 0:
			scaled_surf = pygame.transform.scale(self.frame1_surf, (self.width * self.scale, self.height * self.scale))
			rotated_surf = pygame.transform.rotate(scaled_surf, self.rotation)
		if self.animation_state == 1:
			scaled_surf = pygame.transform.scale(self.frame2_surf, (self.width * self.scale, self.height * self.scale))
			rotated_surf = pygame.transform.rotate(scaled_surf, self.rotation)
		if self.animation_state == 2:
			scaled_surf = pygame.transform.scale(self.frame3_surf, (self.width * self.scale, self.height * self.scale))
			rotated_surf = pygame.transform.rotate(scaled_surf, self.rotation)
		if self.animation_state == 3:
			scaled_surf = pygame.transform.scale(self.frame4_surf, (self.width * self.scale, self.height * self.scale))
			rotated_surf = pygame.transform.rotate(scaled_surf, self.rotation)
		rotated_surf.set_colorkey((1,0,0))
		self.unit_rect_rotate = rotated_surf.get_rect(center= self.unit_rect.center)

		return rotated_surf

	def handle_buff(self):
		for unit in game.friendly_units:
			if unit.id != 6:
				if unit.buffed:
					unit.buff_timer += 1
					
					if unit.buff_timer == unit.buff_timer_goal:
						unit.buff_timer = 0
						unit.buffed = False

	def draw_buff_crown(self):
		if self.id != 6:
			if self.buffed and self.health > 0:
				if self.crown_animation_timer == 0:
					self.crown_animation_state = 0
				elif self.crown_animation_timer == 15:
					self.crown_animation_state = 1
				elif self.crown_animation_timer == 30:
					self.crown_animation_state = 2
				elif self.crown_animation_timer == 45:
					self.crown_animation_state = 3
				self.crown_animation_timer += 1
				if self.crown_animation_timer == self.crown_animation_timer_goal:
					self.crown_animation_timer = 0


				if self.crown_y_offset < 2 and self.crown_floating_direction == 0:
					self.crown_y_offset += 0.1
				elif self.crown_y_offset >= 2 and self.crown_floating_direction == 0:
					self.crown_floating_direction = 1
				elif self.crown_y_offset > -2 and self.crown_floating_direction == 1:
					self.crown_y_offset -= 0.1
				elif self.crown_y_offset <= -2 and self.crown_floating_direction == 1:
					self.crown_floating_direction = 0


				if not self.id == 9 and not self.id == 3:
					self.crown_rect.center = (self.unit_rect.center[0], self.unit_rect.topleft[1] - 15 + self.crown_y_offset)
				elif self.id == 9:
					self.crown_rect.center = (self.unit_rect.center[0], self.unit_rect.topleft[1] + 30 + self.crown_y_offset)
				elif self.id == 3:
					self.crown_rect.center = (self.unit_rect.center[0], self.unit_rect.topleft[1] + self.crown_y_offset)
				

				game.draw_transparent_rect((self.crown_rect.width, game.FLOOR_LEVEL - round(self.crown_rect.bottomleft[1])), (255,215,0), 60 - round(self.buff_timer/3), self.crown_rect.bottomleft)


				if self.crown_animation_state == 0:
					game.screen.blit(self.crown_frame1, self.crown_rect)
				elif self.crown_animation_state == 1:
					game.screen.blit(self.crown_frame2, self.crown_rect)
				elif self.crown_animation_state == 2:
					game.screen.blit(self.crown_frame3, self.crown_rect)
				elif self.crown_animation_state == 3:
					game.screen.blit(self.crown_frame4, self.crown_rect)


	def buff_units(self):
		for unit in game.friendly_units:
			if unit.id == 6:
				unit.attack_timer += 1
				if unit.attack_timer >= round(unit.attack_timer_goal / 2):
						particle = Particle((255,215,0), (3,3), (unit.unit_rect.topright[0] - 15 - unit.weapon_rotation/2, unit.unit_rect.topright[1] +24 -unit.weapon_rotation/3), 0.03, "no_gravity")
						game.particles.append(particle)
						if not unit.weapon_rotation >= 40 and unit.idle_swinging_direction == 0:
							unit.weapon_rotation += 4
						elif unit.weapon_rotation >= 40 and unit.idle_swinging_direction == 0:
							unit.idle_swinging_direction = 1
						elif not unit.weapon_rotation <= 10 and unit.idle_swinging_direction == 1:
							unit.weapon_rotation -= 4
						elif unit.weapon_rotation <= 10 and unit.idle_swinging_direction == 1:
							unit.idle_swinging_direction = 0

				if unit.attack_timer == unit.attack_timer_goal:
					unit.attack_timer = 0
					for friendly in game.friendly_units:
						if not friendly.id == 6:
							friendly.buffed = True
							friendly.buff_timer = 0
		
		for unit in game.enemy_units:
			if unit.id == 6:
				unit.attack_timer += 1
				if unit.attack_timer >= round(unit.attack_timer_goal / 2):
						if unit.attack_timer >= round(unit.attack_timer_goal / 2):
							particle = Particle((255,215,0), (3,3), (unit.unit_rect.topleft[0] + 15 - unit.weapon_rotation/2, unit.unit_rect.topright[1] +10 -unit.weapon_rotation/3), 0.03, "no_gravity")
							game.particles.append(particle)
							if unit.weapon_rotation > -40 and unit.idle_swinging_direction == 0:
								unit.weapon_rotation -= 4
							elif unit.weapon_rotation <= -40 and unit.idle_swinging_direction == 0:
								unit.idle_swinging_direction = 1
							elif unit.weapon_rotation <= -10 and unit.idle_swinging_direction == 1:
								unit.weapon_rotation += 4
							elif unit.weapon_rotation >= -10 and unit.idle_swinging_direction == 1:
								unit.idle_swinging_direction = 0
	
				if unit.attack_timer == unit.attack_timer_goal:
					unit.attack_timer = 0
					for enemy in game.enemy_units:
						if not enemy.id == 6:
							enemy.buffed = True
							enemy.buff_timer = 0

	
	def spawn_friendly(self, id):
		unit = Unit(True, id)
		game.friendly_units_queue.append(unit)
		game.friendly_exp += unit_info.unit_exp_value[id]/2

	def spawn_enemy(self, id):
		unit = Unit(False, id)
		game.enemy_unit_buffer.append(unit)

	def spawn_friendly_from_buffer(self):
		if not len(game.friendly_units) == 0:
				if not game.friendly_units[-1].unit_rect.colliderect(friendly_base.base_spawn_rect) and not len(game.friendly_unit_buffer) == 0:
					game.friendly_units.append(game.friendly_unit_buffer[0])
					game.friendly_exp += unit_info.unit_exp_value[game.friendly_unit_buffer[0].id]/2
					game.friendly_unit_buffer.pop(0)
		elif not len(game.friendly_unit_buffer) == 0 and len(game.friendly_units) == 0:
			game.friendly_units.append(game.friendly_unit_buffer[0])
			game.friendly_exp += unit_info.unit_exp_value[game.friendly_unit_buffer[0].id]/2
			game.friendly_unit_buffer.pop(0)
		
		

	def spawn_enemy_from_buffer(self):
		if not len(game.enemy_units) == 0:
				if not game.enemy_units[-1].unit_rect.colliderect(enemy_base.base_spawn_rect) and not len(game.enemy_unit_buffer) == 0:
					game.enemy_units.append(game.enemy_unit_buffer[0])
					game.enemy_exp += unit_info.unit_exp_value[game.enemy_unit_buffer[0].id]/2
					game.enemy_unit_buffer.pop(0)
		elif not len(game.enemy_unit_buffer) == 0 and len(game.enemy_units) == 0:
			game.enemy_units.append(game.enemy_unit_buffer[0])
			game.enemy_exp += unit_info.unit_exp_value[game.enemy_unit_buffer[0].id]/2
			game.enemy_unit_buffer.pop(0)





	def check_if_in_enemy_base(self):
		for unit in game.friendly_units:
			if unit.unit_rect.bottomright[0] >= 1900 + game.camera_offset_x:
				game.friendly_units.pop(game.friendly_units.index(unit))
				enemy_base.health -= unit.damage
		for enemy in game.enemy_units:
			if enemy.unit_rect.bottomleft[0] <= 20 + game.camera_offset_x:
				game.enemy_units.pop(game.enemy_units.index(enemy))
				friendly_base.health -= enemy.damage


	def move(self):
		for unit in game.friendly_units:
			if unit.moving:
				unit.x_pos += unit.movement_speed
				unit.unit_rect.x = unit.x_pos + game.camera_offset_x
				unit.front_rect.x = unit.x_pos + unit.unit_rect.width + game.camera_offset_x
			else:
				unit.unit_rect.x = unit.x_pos + game.camera_offset_x
				unit.front_rect.x = unit.x_pos + unit.unit_rect.width + game.camera_offset_x
			unit.unit_rect.y += unit.fall_speed
			#	triggers the idle walking animation
			if unit.has_weapon:
				unit.weapon_rect.center = (unit.unit_rect.center[0] - unit.weapon_offset_x, unit.unit_rect.center[1] + unit.weapon_offset_y) 
				unit.weapon_walking_animation()

		for unit in game.enemy_units:
			if unit.moving:
				unit.x_pos -= unit.movement_speed
				unit.unit_rect.x = unit.x_pos + game.camera_offset_x
				unit.front_rect.bottomright = (unit.x_pos + game.camera_offset_x, game.FLOOR_LEVEL)
			else:
				unit.unit_rect.x = unit.x_pos + game.camera_offset_x
				unit.front_rect.bottomright = (unit.x_pos + game.camera_offset_x, game.FLOOR_LEVEL)
			unit.unit_rect.y += unit.fall_speed
			#	triggers the idle walking animation
			if unit.has_weapon:
				unit.weapon_rect.center = (unit.unit_rect.center[0] + unit.weapon_offset_x, unit.unit_rect.center[1] + unit.weapon_offset_y) 
				unit.weapon_walking_animation()
	
	def rotate_weapon(self):
		if self.id != 2 and self.id != 7 and self.id != 5:
			rotated_surf = pygame.transform.rotate(self.weapon_surf, self.weapon_rotation)
			rotated_surf.set_colorkey((1,0,0))
			self.weapon_rect_rotate = rotated_surf.get_rect(center= self.weapon_rect.center)
			return rotated_surf
		else:
			if self.weapon_animation_state == 0:
				rotated_surf = pygame.transform.rotate(self.weapon_surf, self.weapon_rotation)
				rotated_surf.set_colorkey((1,0,0))
				self.weapon_rect_rotate = rotated_surf.get_rect(center= self.weapon_rect.center)
				return rotated_surf
			elif self.weapon_animation_state == 1:
				rotated_surf = pygame.transform.rotate(self.weapon_surf2, self.weapon_rotation)
				rotated_surf.set_colorkey((1,0,0))
				self.weapon_rect_rotate = rotated_surf.get_rect(center= self.weapon_rect.center)
				return rotated_surf
	

	def weapon_walking_animation(self):
		if self.moving:
			if self.friendly and not self.id == 6:
				if not self.weapon_rotation <= -self.idle_swinging_distance and self.idle_swinging_direction == 0:
					self.weapon_rotation -= self.idle_swinging_speed
				elif self.weapon_rotation <= -self.idle_swinging_distance and self.idle_swinging_direction == 0:
					self.idle_swinging_direction = 1
				elif not self.weapon_rotation >= 0 and self.idle_swinging_direction == 1:
					self.weapon_rotation += self.idle_swinging_speed
				elif self.weapon_rotation >= 0 and self.idle_swinging_direction == 1:
					self.idle_swinging_direction = 0
			elif not self.friendly and not self.id == 6:
				if not self.weapon_rotation >= +self.idle_swinging_distance and self.idle_swinging_direction == 0:
					self.weapon_rotation += self.idle_swinging_speed
				elif self.weapon_rotation >= +self.idle_swinging_distance and self.idle_swinging_direction == 0:
					self.idle_swinging_direction = 1
				elif not self.weapon_rotation <= 0 and self.idle_swinging_direction == 1:
					self.weapon_rotation -= self.idle_swinging_speed
				elif self.weapon_rotation <= 0 and self.idle_swinging_direction == 1:
					self.idle_swinging_direction = 0


	def update_animation_state(self):
		for unit in game.friendly_units + game.enemy_units:
			if unit.moving:
				unit.animation_timer += 1
				if unit.animation_timer == unit.animation_timer_goal:
					unit.animation_timer = 0
					if unit.animation_state < unit.animation_frames - 1:
						unit.animation_state += 1
					else:
						unit.animation_state = 0
			else:
				unit.animation_state = 0


	def check_health(self):
		for unit in game.friendly_units:
			if unit.health <= 0:
				unit.fall_speed += game.GRAVITY
				unit.moving = False
				unit.unit_rect.x -= unit.fall_speed
				unit.rotation += 6
				unit.scale -= 0.02
				if unit.has_weapon:
					unit.weapon_rotation = unit.rotation

				if unit.unit_rect.y >= 500:
					game.friendly_units.pop(game.friendly_units.index(unit))
					game.enemy_money += unit.kill_value * 1.5
					game.enemy_exp += unit_info.unit_exp_value[unit.id]

		for unit in game.enemy_units:
			if unit.health <= 0:
				unit.fall_speed += game.GRAVITY
				unit.moving = False
				unit.unit_rect.x += unit.fall_speed
				unit.rotation -= 6
				unit.scale -= 0.02
				if unit.has_weapon:
					unit.weapon_rotation = unit.rotation

				if unit.unit_rect.y >= 500:
					game.enemy_units.pop(game.enemy_units.index(unit))
					game.friendly_money += unit.kill_value
					game.friendly_exp += unit_info.unit_exp_value[unit.id]

	
	def make_units_stop_on_collision(self):
		if len(game.friendly_units) > 0 and len(game.enemy_units) > 0:
			if game.friendly_units[0].unit_rect.colliderect(game.enemy_units[0].unit_rect):
				game.friendly_units[0].moving = False
				if not game.friendly_units[0].ranged:
					game.friendly_units[0].melee_combat = True

				game.enemy_units[0].moving = False
				if not game.enemy_units[0].ranged:
					game.enemy_units[0].melee_combat = True

			else:
				#	if not coliding with enemy unit make units move again
				game.friendly_units[0].moving = True
				game.enemy_units[0].moving = True
				#	if not colliding and not ranged make units stop fighting
				if not game.friendly_units[0].ranged:
					game.friendly_units[0].melee_combat = False
				if not game.enemy_units[0].ranged:
					game.enemy_units[0].melee_combat = False
				#	if unit collides with other unit spop moving
		for unit in game.friendly_units:
			if game.friendly_units.index(unit) != 0:
				if unit.front_rect.colliderect(game.friendly_units[game.friendly_units.index(unit) - 1].unit_rect):
					unit.moving = False
				#	if not colliding make unit move again
				else:
					unit.moving = True
				#	if enemy collides with other enemy stop moving
		for unit in game.enemy_units:
			if game.enemy_units.index(unit) != 0:
				if unit.front_rect.colliderect(game.enemy_units[game.enemy_units.index(unit) - 1].unit_rect):
					unit.moving = False
				#	if not colling make enemy move again
				else:
					unit.moving = True

	def handle_melee_combat(self):
		#	if melee combat state is active: call the attack melee methon
		if len(game.friendly_units) != 0 and len(game.enemy_units) != 0:
			if not game.friendly_units[0].ranged:
				if game.friendly_units[0].melee_combat:
					game.friendly_units[0].attack_melee(game.enemy_units[0])
	
			if not game.enemy_units[0].ranged:
				if game.enemy_units[0].melee_combat:
					game.enemy_units[0].attack_melee(game.friendly_units[0])

	def attack_base(self):
		if len(game.friendly_units) != 0:
			if game.friendly_units[0].unit_rect.colliderect(enemy_base.base_rect):
				game.friendly_units[0].moving = False
				if not game.friendly_units[0].ranged:
					if not game.friendly_units[0].melee_combat:	
						game.friendly_units[0].attack_melee(enemy_base)
		if len(game.enemy_units) != 0:
			if game.enemy_units[0].unit_rect.colliderect(friendly_base.base_rect):
				game.enemy_units[0].moving = False
				if not game.enemy_units[0].ranged:
					if not game.enemy_units[0].melee_combat:
						game.enemy_units[0].attack_melee(friendly_base)




	def attack_melee(self, target):
		#	determains the correckt weapon rotaition while attacking and calls the get_hurt method
		if self.friendly:
			if self.id == 1 or self.id == 4:
				self.attack_timer += 1
				if self.attack_timer >= round(self.attack_timer_goal / 2):
					self.weapon_rotation += 2
				if self.attack_timer >= self.attack_timer_goal - 15 and self.weapon_rotation >= 0:
					self.weapon_rotation -= 15
				if self.attack_timer >= self.attack_timer_goal:
					self.attack_timer = 0
					self.weapon_rotation = 0
					if not self.buffed:
						target.get_hurt(self.damage)
					else:
						target.get_hurt(round(self.damage * 1.25))
			
			elif self.id == 3:
				self.attack_timer += 1
				if self.attack_timer >= round(self.attack_timer_goal / 2):
					self.weapon_rotation -= 1
				if self.attack_timer >= self.attack_timer_goal - 15 and self.weapon_rotation <= 0:
					self.weapon_rotation += 10
				if self.attack_timer >= self.attack_timer_goal:
					self.attack_timer = 0
					self.weapon_rotation = 0
					if not self.buffed:
						target.get_hurt(self.damage)
					else:
						target.get_hurt(round(self.damage * 1.25))

			elif self.id == 8:
				self.attack_timer += 1
				if self.attack_timer >= round(self.attack_timer_goal / 2):
					self.weapon_rotation -= 1
				if self.attack_timer >= self.attack_timer_goal - 10 and self.weapon_rotation <= 10:
					self.weapon_rotation += 10
				if self.attack_timer >= self.attack_timer_goal:
					self.attack_timer = 0
					self.weapon_rotation = 0
					if not self.buffed:
						target.get_hurt(self.damage)
					else:
						target.get_hurt(round(self.damage * 1.25))

		else:
			if self.id == 1 or self.id == 4:
				self.attack_timer += 1
				if self.attack_timer >= round(self.attack_timer_goal / 2):
					self.weapon_rotation -= 2
				if self.attack_timer >= self.attack_timer_goal - 15 and self.weapon_rotation <= 0:
					self.weapon_rotation += 15
				if self.attack_timer >= self.attack_timer_goal:
					self.attack_timer = 0
					self.weapon_rotation = 0
					if not self.buffed:
						target.get_hurt(self.damage)
					else:
						target.get_hurt(round(self.damage * 1.25))
			
			elif self.id == 3:
				self.attack_timer += 1
				if self.attack_timer >= round(self.attack_timer_goal / 2):
					self.weapon_rotation += 1
				if self.attack_timer >= self.attack_timer_goal - 15 and self.weapon_rotation >= 0:
					self.weapon_rotation -= 10
				if self.attack_timer >= self.attack_timer_goal:
					self.attack_timer = 0
					self.weapon_rotation = 0
					if not self.buffed:
						target.get_hurt(self.damage)
					else:
						target.get_hurt(round(self.damage * 1.25))

			elif self.id == 8:
				self.attack_timer += 1
				if self.attack_timer >= round(self.attack_timer_goal / 2):
					self.weapon_rotation += 1
				if self.attack_timer >= self.attack_timer_goal - 10 and self.weapon_rotation >= 10:
					self.weapon_rotation -= 10
				if self.attack_timer >= self.attack_timer_goal:
					self.attack_timer = 0
					self.weapon_rotation = 0
					if not self.buffed:
						target.get_hurt(self.damage)
					else:
						target.get_hurt(round(self.damage * 1.25))



	def update_range_rect(self):
		if self.ranged and self.friendly:
			self.range_rect = pygame.Rect(self.unit_rect.topright[0], self.unit_rect.topright[1], 96, self.unit_rect.height)
		if self.ranged and not self.friendly:
			self.range_rect = pygame.Rect(self.unit_rect.topleft[0] - 96, self.unit_rect.topleft[1], 96, self.unit_rect.height)



	def find_unit_in_range(self):
		for unit in game.friendly_units:
			unit.update_range_rect()
			if unit.ranged and len(game.enemy_units) > 0:
				if unit.range_rect.colliderect(game.enemy_units[0].unit_rect) or unit.range_rect.colliderect(enemy_base.base_rect):
					unit.unit_in_range = True
				if not unit.range_rect.colliderect(game.enemy_units[0].unit_rect) and not unit.range_rect.colliderect(enemy_base.base_rect):
					unit.unit_in_range = False

		for enemy in game.enemy_units:
			enemy.update_range_rect()
			if enemy.ranged and len(game.friendly_units) > 0:
				if enemy.range_rect.colliderect(game.friendly_units[0].unit_rect) or enemy.range_rect.colliderect(friendly_base.base_rect):
					enemy.unit_in_range = True
				if not enemy.range_rect.colliderect(game.friendly_units[0].unit_rect) and not enemy.range_rect.colliderect(friendly_base.base_rect):
					enemy.unit_in_range = False
				

	def attack_ranged(self):
		for unit in game.friendly_units:
			if unit.id == 2:
				if unit.unit_in_range:
					unit.attack_timer += 1
					if unit.attack_timer >= round(unit.attack_timer_goal / 4):
						unit.weapon_animation_state = 0
						unit.weapon_rotation += 3
					if unit.attack_timer >= unit.attack_timer_goal - 20:
						unit.weapon_rotation -= 15
					if unit.attack_timer == unit.attack_timer_goal:
						unit.attack_timer = 0
						unit.weapon_rotation = 0
						unit.weapon_animation_state = 1
						projectile = UnitProjectile((unit.unit_rect.topright[0] - 4, unit.unit_rect.topright[1] + 10), True, 2)
						unit.projectiles.append(projectile)

			elif unit.id == 5:
				if unit.unit_in_range:
					unit.attack_timer += 1
					if unit.attack_timer >= round(unit.attack_timer_goal / 2):
						unit.weapon_animation_state = 1
						particle = Particle((50,50,240), (2,2), (unit.unit_rect.topright[0] - unit.weapon_rotation/2, unit.unit_rect.topright[1] +10 -unit.weapon_rotation/3), 0.03, "no_gravity")
						game.particles.append(particle)
						if not unit.weapon_rotation >= random.randint(35, 45) and unit.idle_swinging_direction == 0:
							unit.weapon_rotation += 4
						elif unit.weapon_rotation >= random.randint(35, 45) and unit.idle_swinging_direction == 0:
							unit.idle_swinging_direction = 1
						elif not unit.weapon_rotation <= 10 and unit.idle_swinging_direction == 1:
							unit.weapon_rotation -= 4
						elif unit.weapon_rotation <= 10 and unit.idle_swinging_direction == 1:
							unit.idle_swinging_direction = 0
					if unit.attack_timer == unit.attack_timer_goal:
						unit.attack_timer = 0
						unit.weapon_rotation = 0
						unit.weapon_animation_state = 0
						projectile = UnitProjectile((unit.unit_rect.topright[0] - 4, unit.unit_rect.topright[1] + 10), True, 5)
						unit.projectiles.append(projectile)

			elif unit.id == 7:
				if unit.unit_in_range:
					unit.weapon_rotation = 0
					unit.weapon_animation_state = 0
					unit.attack_timer += 1
					if unit.attack_timer >= round(unit.attack_timer_goal/4):
						unit.shooting = False
					if unit.attack_timer == unit.attack_timer_goal:
						unit.shooting = True
						unit.attack_timer = 0
					if unit.shooting:
						unit.shooting_timer += 1
						if unit.shooting_timer == round(unit.shooting_timer_goal/1.5):
							unit.weapon_animation_state = 0
						if unit.shooting_timer == unit.shooting_timer_goal:
							unit.shooting_timer = 0
							projectile = UnitProjectile((unit.unit_rect.topright[0] + 2, unit.unit_rect.topright[1] + 20), True, 7)
							unit.projectiles.append(projectile)
							unit.weapon_animation_state = 1
							for i in range(5):
								particle1 = Particle((255,206,0), (2,2), (unit.unit_rect.topright[0], unit.unit_rect.topright[1] + 20), 0.1, "friendly_muzzle")
								particle2 = Particle((255,154,0), (2,2), (unit.unit_rect.topright[0], unit.unit_rect.topright[1] + 20), 0.1, "friendly_muzzle")
								particle3 = Particle((255,90,0), (2,2), (unit.unit_rect.topright[0], unit.unit_rect.topright[1] + 20), 0.1, "friendly_muzzle")
								game.particles.append(particle1)
								game.particles.append(particle2)
								game.particles.append(particle3)

			elif unit.id == 9:
				if unit.unit_in_range:
					unit.attack_timer += 1
					if unit.attack_timer == unit.attack_timer_goal:
						unit.attack_timer = 0
						projectile = UnitProjectile((unit.unit_rect.topright[0] + 2, unit.unit_rect.topright[1] + 58), True, 9)
						unit.projectiles.append(projectile)
						for i in range(30):
							particle1 = Particle((255,206,0), (3,3), (unit.unit_rect.topright[0] - 5, unit.unit_rect.topright[1] + 58), 0.1, "friendly_muzzle")
							particle2 = Particle((255,154,0), (3,3), (unit.unit_rect.topright[0] - 5, unit.unit_rect.topright[1] + 58), 0.1, "friendly_muzzle")
							particle3 = Particle((255,90,0) , (3,3), (unit.unit_rect.topright[0] - 5, unit.unit_rect.topright[1] + 58), 0.1, "friendly_muzzle")
							game.particles.append(particle1)
							game.particles.append(particle2)
							game.particles.append(particle3)

		for unit in game.enemy_units:
			if unit.id == 2:
				if unit.unit_in_range:
					unit.attack_timer += 1
					if unit.attack_timer >= round(unit.attack_timer_goal / 4):
						unit.weapon_animation_state = 0
						unit.weapon_rotation -= 3
					if unit.attack_timer >= unit.attack_timer_goal - 20:
						unit.weapon_rotation += 15
					if unit.attack_timer == unit.attack_timer_goal:
						unit.attack_timer = 0
						unit.weapon_rotation = 0
						unit.weapon_animation_state = 1
						projectile = UnitProjectile((unit.unit_rect.topleft[0] + 4, unit.unit_rect.topright[1] + 10), False, 2)
						unit.projectiles.append(projectile)

			elif unit.id == 5:
				if unit.unit_in_range:
					unit.attack_timer += 1
					if unit.attack_timer >= round(unit.attack_timer_goal / 2):
						unit.weapon_animation_state = 1
						particle = Particle((50,50,240), (2,2), (unit.unit_rect.topleft[0] - unit.weapon_rotation/2, unit.unit_rect.topright[1] +10 -unit.weapon_rotation/3), 0.03, "no_gravity")
						game.particles.append(particle)
						if unit.weapon_rotation > random.randint(-45, -35) and unit.idle_swinging_direction == 0:
							unit.weapon_rotation -= 4
						elif unit.weapon_rotation <= random.randint(-45, -35) and unit.idle_swinging_direction == 0:
							unit.idle_swinging_direction = 1
						elif unit.weapon_rotation <= -10 and unit.idle_swinging_direction == 1:
							unit.weapon_rotation += 4
						elif unit.weapon_rotation >= -10 and unit.idle_swinging_direction == 1:
							unit.idle_swinging_direction = 0
					if unit.attack_timer >= unit.attack_timer_goal:
						unit.attack_timer = 0
						unit.weapon_rotation = 0
						unit.weapon_animation_state = 0
						projectile = UnitProjectile((unit.unit_rect.topleft[0] + 4, unit.unit_rect.topleft[1] + 10), False, 5)
						unit.projectiles.append(projectile)

			elif unit.id == 7:
				if unit.unit_in_range:
					unit.weapon_rotation = 0
					unit.weapon_animation_state = 0
					unit.attack_timer += 1
					if unit.attack_timer >= round(unit.attack_timer_goal/4):
						unit.shooting = False
					if unit.attack_timer == unit.attack_timer_goal:
						unit.shooting = True
						unit.attack_timer = 0
					if unit.shooting:
						unit.shooting_timer += 1
						if unit.shooting_timer == round(unit.shooting_timer_goal/1.5):
							unit.weapon_animation_state = 0
						if unit.shooting_timer == unit.shooting_timer_goal:
							unit.shooting_timer = 0
							projectile = UnitProjectile((unit.unit_rect.topleft[0] - 2, unit.unit_rect.topleft[1] + 20), False, 7)
							unit.projectiles.append(projectile)
							unit.weapon_animation_state = 1
							for i in range(5):
								particle1 = Particle((255,206,0), (2,2), (unit.unit_rect.topleft[0], unit.unit_rect.topleft[1] + 20), 0.1, "enemy_muzzle")
								particle2 = Particle((255,154,0), (2,2), (unit.unit_rect.topleft[0], unit.unit_rect.topleft[1] + 20), 0.1, "enemy_muzzle")
								particle3 = Particle((255,90,0), (2,2), (unit.unit_rect.topleft[0], unit.unit_rect.topleft[1] + 20), 0.1, "enemy_muzzle")
								game.particles.append(particle1)
								game.particles.append(particle2)
								game.particles.append(particle3)

			elif unit.id == 9:
				if unit.unit_in_range:
					unit.attack_timer += 1
					if unit.attack_timer == unit.attack_timer_goal:
						unit.attack_timer = 0
						projectile = UnitProjectile((unit.unit_rect.topleft[0] - 2, unit.unit_rect.topleft[1] + 58), False, 9)
						unit.projectiles.append(projectile)
						for i in range(30):
							particle1 = Particle((255,206,0), (3,3), (unit.unit_rect.topleft[0] + 5, unit.unit_rect.topleft[1] + 58), 0.1, "enemy_muzzle")
							particle2 = Particle((255,154,0), (3,3), (unit.unit_rect.topleft[0] + 5, unit.unit_rect.topleft[1] + 58), 0.1, "enemy_muzzle")
							particle3 = Particle((255,90,0) , (3,3), (unit.unit_rect.topleft[0] + 5, unit.unit_rect.topleft[1] + 58), 0.1, "enemy_muzzle")
							game.particles.append(particle1)
							game.particles.append(particle2)
							game.particles.append(particle3)



	
	def get_hurt(self, amount):
		if not self.id == 6:
			if not self.buffed:
				self.health -= amount
			else:
				self.health -= round(amount * 0.75)
		else:
			self.health -= amount
		if not self.id == 9:
			blood_master.spawn_cluster(self.unit_rect.center, self.friendly, (200,0,0), (8,8), True, 20)
		else:
			blood_master.spawn_cluster(self.unit_rect.center, self.friendly, (249,233,9), (4,4), False, 10)
			blood_master.spawn_cluster(self.unit_rect.center, self.friendly, (20,20,20), (4,4), False, 10)


			
	def draw(self):
		for unit in game.friendly_units:
			game.screen.blit(unit.rotate_and_scale(), unit.unit_rect_rotate)
			unit.draw_buff_crown()
			if unit.has_weapon:
				game.screen.blit(unit.rotate_weapon(), unit.weapon_rect_rotate)
			if unit.ranged and game.dev_mode:
				pygame.draw.rect(game.screen, "red", unit.range_rect)
			


		for unit in game.enemy_units:
			game.screen.blit(unit.rotate_and_scale(), unit.unit_rect_rotate)
			unit.draw_buff_crown()
			if unit.has_weapon:
				game.screen.blit(unit.rotate_weapon(), unit.weapon_rect_rotate)
			if unit.ranged and game.dev_mode:
				pygame.draw.rect(game.screen, "red", unit.range_rect)
			

	def update(self):
		self.spawn_friendly_from_buffer()
		self.spawn_enemy_from_buffer()
		self.move()
		self.update_animation_state()
		self.handle_melee_combat()
		self.make_units_stop_on_collision()
		self.attack_base()
		self.check_health()
		self.find_unit_in_range()
		self.attack_ranged()
		self.handle_buff()
		self.buff_units()



class UnitProjectile:
	def __init__(self, starting_pos, friendly, id):
		self.starting_pos = starting_pos
		self.x_pos = self.starting_pos[0]
		self.y_pos = self.starting_pos[1]
		self.starting_camera_offset = game.camera_offset_x
		self.friendly = friendly
		self.id = id
		self.speed = projectile_info.unit_projectile_vel[self.id]
		self.damage = unit_info.unit_damage[self.id]
		self.rotation = 0

		if self.id == 2:
			self.surf = game.unit_projectile_2.get_image(0, (10,24), (1,0,0), 0.7)
		elif self.id == 5:
			self.surf = game.unit_projectile_5.get_image(0, (8,8), (1,0,0), 1)
		elif self.id == 7:
			self.surf = game.unit_projectile_7.get_image(0, (8,8), (1,0,0), 0.5)
		elif self.id == 9:
			self.surf = game.unit_projectile_9.get_image(0, (16,8), (1,0,0), 1)
		
		self.rect = self.surf.get_rect(center= self.starting_pos)
		self.rect_rotate = self.rect

		if not self.friendly:
			self.surf = pygame.transform.flip(self.surf, True, False)
			self.surf.set_colorkey((1,0,0))


	def move(self):
		for unit in game.friendly_units + game.enemy_units:
			if unit.ranged:
				for projectile in unit.projectiles:
					x_camera_offset_dif = projectile.starting_camera_offset - game.camera_offset_x
					if projectile.friendly:
						projectile.x_pos += projectile.speed
						if projectile.id == 2 or projectile.id == 5:
							projectile.rotation -= 10
						if projectile.id == 5:
							particle = Particle((50,50,255), (3,3), projectile.rect.center, 0.05, "no_gravity")
							game.particles.append(particle)
							particle = Particle((200,200,200), (1,1), projectile.rect.center, 0.05, "no_gravity")
							game.particles.append(particle)
						elif projectile.id == 9:
							projectile.y_pos += 0.5
					else:
						projectile.x_pos -= projectile.speed
						if projectile.id == 2 or projectile.id == 5:
							projectile.rotation += 10
						if projectile.id == 5:
							particle = Particle((50,50,255), (3,3), projectile.rect.center, 0.05, "no_gravity")
							game.particles.append(particle)
							particle = Particle((200,200,200), (1,1), projectile.rect.center, 0.05, "no_gravity")
							game.particles.append(particle)
						elif projectile.id == 9:
							projectile.y_pos += 0.5

					projectile.rect.center = (projectile.x_pos - x_camera_offset_dif, projectile.y_pos)

	def check_for_collision(self):
		for unit in game.friendly_units:
			if unit.ranged:
				for projectile in unit.projectiles:
						for enemy in game.enemy_units:
							if enemy.unit_rect.colliderect(projectile.rect):
								if not unit.buffed:
									enemy.get_hurt(projectile.damage)
								else:
									enemy.get_hurt(round(projectile.damage * 1.25))

								if projectile.id == 9:
									for i in range(20):
										particle1 = Particle((255,206,0), (2,2), projectile.rect.midright, 0.2, "no_gravity")
										particle2 = Particle((255,154,0), (3,3), projectile.rect.midright, 0.2, "no_gravity")
										particle3 = Particle((255,90,0) , (2,2), projectile.rect.midright, 0.2, "no_gravity")
										game.particles.append(particle1)
										game.particles.append(particle2)
										game.particles.append(particle3)
								try:
									unit.projectiles.pop(unit.projectiles.index(projectile))
								except ValueError:
									print("ValueError in unit projectile 'check for collision friendly'")
						
		for unit in game.enemy_units:
			if unit.ranged:
				for projectile in unit.projectiles:
						for friendly in game.friendly_units:
							if friendly.unit_rect.colliderect(projectile.rect):
								if not unit.buffed:
									friendly.get_hurt(projectile.damage)
								else:
									friendly.get_hurt(round(projectile.damage * 1.25))
								if projectile.id == 9:
									for i in range(20):
										particle1 = Particle((255,206,0), (2,2), projectile.rect.midright, 0.2, "no_gravity")
										particle2 = Particle((255,154,0), (3,3), projectile.rect.midright, 0.2, "no_gravity")
										particle3 = Particle((255,90,0) , (2,2), projectile.rect.midright, 0.2, "no_gravity")
										game.particles.append(particle1)
										game.particles.append(particle2)
										game.particles.append(particle3)
								try:
									unit.projectiles.pop(unit.projectiles.index(projectile))
								except ValueError:
									print("ValueError in unit projectile 'check for collision enemy'")


	def check_for_base_collision(self):
		for unit in game.friendly_units:
			if unit.ranged:
				for projectile in unit.projectiles:
					if enemy_base.base_spawn_rect.colliderect(projectile.rect):
						enemy_base.get_hurt(projectile.damage)

						if projectile.id == 9:
							for i in range(20):
								particle1 = Particle((255,206,0), (2,2), projectile.rect.midright, 0.2, "no_gravity")
								particle2 = Particle((255,154,0), (3,3), projectile.rect.midright, 0.2, "no_gravity")
								particle3 = Particle((255,90,0) , (2,2), projectile.rect.midright, 0.2, "no_gravity")
								game.particles.append(particle1)
								game.particles.append(particle2)
								game.particles.append(particle3)

						try:
							unit.projectiles.pop(unit.projectiles.index(projectile))
						except ValueError:
							print("ValueError in unit projectile 'check for collision friendly' (targeting base)")

		for unit in game.enemy_units:
			if unit.ranged:
				for projectile in unit.projectiles:
					if friendly_base.base_spawn_rect.colliderect(projectile.rect):
						friendly_base.get_hurt(projectile.damage)

						if projectile.id == 9:
							for i in range(20):
								particle1 = Particle((255,206,0), (2,2), projectile.rect.midright, 0.2, "no_gravity")
								particle2 = Particle((255,154,0), (3,3), projectile.rect.midright, 0.2, "no_gravity")
								particle3 = Particle((255,90,0) , (2,2), projectile.rect.midright, 0.2, "no_gravity")
								game.particles.append(particle1)
								game.particles.append(particle2)
								game.particles.append(particle3)

						try:
							unit.projectiles.pop(unit.projectiles.index(projectile))
						except ValueError:
							print("ValueError in unit projectile 'check for collision enemy' (targeting base)")


	def rotate(self):
		rotated_surf = pygame.transform.rotate(self.surf, self.rotation)
		rotated_surf.set_colorkey((1,0,0))
		self.rect_rotate = rotated_surf.get_rect(center= self.rect.center)
		return rotated_surf


	def draw(self):
		for unit in game.friendly_units + game.enemy_units:
			if unit.ranged:
				for projectile in unit.projectiles:
					game.screen.blit(projectile.rotate(), projectile.rect)
	

	def update(self):
		self.move()
		self.check_for_collision()
		self.check_for_base_collision()



class Dirt:
	def __init__(self, pos):
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.color = (64,41,5)
		self.width = 2
		self.height = 2
		self.fall_vel = 0
		self.death_timer = 0
		self.death_timer_goal = 10
		self.x_direction = random.randint(-1, 1)
		self.y_direction = random.randint(-4, 1)


	def spawn_cluster(self, pos):
		dirt1 = Dirt(pos)
		dirt2 = Dirt(pos)
		dirt3 = Dirt(pos)
		dirt4 = Dirt(pos)
		dirt5 = Dirt(pos)
		dirt6 = Dirt(pos)
		dirt7 = Dirt(pos)
		dirt8 = Dirt(pos)
		dirt9 = Dirt(pos)
		dirt10 = Dirt(pos)
		dirt11 = Dirt(pos)
		dirt12 = Dirt(pos)
		game.dirt_particles.append(dirt1)
		game.dirt_particles.append(dirt2)
		game.dirt_particles.append(dirt3)
		game.dirt_particles.append(dirt4)
		game.dirt_particles.append(dirt5)
		game.dirt_particles.append(dirt6)
		game.dirt_particles.append(dirt7)
		game.dirt_particles.append(dirt8)
		game.dirt_particles.append(dirt9)
		game.dirt_particles.append(dirt10)
		game.dirt_particles.append(dirt11)
		game.dirt_particles.append(dirt12)
	def move(self):
		for dirt in game.dirt_particles:
			dirt.x_pos += dirt.x_direction
			dirt.y_pos += dirt.y_direction
			dirt.fall_vel += game.GRAVITY
			dirt.y_pos += dirt.fall_vel
	def check_if_dead(self):
		for dirt in game.dirt_particles:
			dirt.death_timer += 1
			if dirt.death_timer == dirt.death_timer_goal:
				game.dirt_particles.pop(game.dirt_particles.index(dirt))

	def update(self):
		self.move()
		self.check_if_dead()

	def draw(self):
		for dirt in game.dirt_particles:
			pygame.draw.rect(game.screen, dirt.color, pygame.Rect(dirt.x_pos, dirt.y_pos, dirt.width, dirt.height))

class Blood:
	def __init__(self, pos:tuple, friendly:bool, color:tuple, size:tuple, stays_on_screen:bool = True):
		self.friendly = friendly
		self.camera_offset_x = game.camera_offset_x
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.color = color
		self.width = size[0]
		self.height = size[1]
		self.stays_on_screen = stays_on_screen
		self.fall_vel = 0
		if self.friendly:
			self.x_direction = random.randint(-4, 1)
			self.y_direction = random.randint(-6, 1)
		elif not self.friendly:
			self.x_direction = random.randint(-1, 4)
			self.y_direction = random.randint(-6, 1)

		self.rect = pygame.Rect(self.x_pos, self.y_pos, self.height, self.width)


	def spawn_cluster(self, pos, friendly, color, size, stays_on_screen, number:int):
		for i in range(number):
			blood_part = Blood(pos, friendly, color, size, stays_on_screen)
			game.blood_particles.append(blood_part)
		
		


	def move(self):
		for blood in game.blood_particles:
			x_camera_offset_dif = blood.camera_offset_x - game.camera_offset_x
			blood.x_pos += blood.x_direction
			blood.y_pos += blood.y_direction
			blood.fall_vel += game.GRAVITY
			blood.y_pos += blood.fall_vel
			if blood.y_pos >= game.SCREEN_SIZE[1] - blood.height and blood.stays_on_screen:
				blood.fall_vel = 0
				blood.x_direction = 0
				blood.y_direction = 0
				blood.fall_vel -= game.GRAVITY
				blood.y_direction += 0.02
			if blood.y_pos >= game.SCREEN_SIZE[1]:
				game.blood_particles.pop(game.blood_particles.index(blood))
			blood.rect.topleft = (blood.x_pos - x_camera_offset_dif, blood.y_pos)

	def draw(self):
		for blood in game.blood_particles:
			pygame.draw.rect(game.screen, blood.color, blood.rect)

	def update(self):
		self.move()


class Particle:
	def __init__(self, color:tuple, size:tuple, starting_pos:tuple, lifetime:int, type:str, alpha:int = 255):
		self.color = (color[0], color[1], color[2], alpha)
		self.width = size[0]
		self.height = size[1]
		self.x_pos = starting_pos[0]
		self.y_pos = starting_pos[1]
		self.starting_pos_x = self.x_pos
		self.starting_pos_y = self.y_pos
		self.x_vel = 0
		self.y_vel = 0
		self.lifetime = round(lifetime * 60)
		self.lifetimer = 0
		self.type = type
		self.starting_camera_offset = game.camera_offset_x
		self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

		if self.type == "no_gravity":
			self.x_direction = random.randint(-1, 1)
			self.y_direction = random.randint(-1, 1)
			self.x_vel = random.randint(0, 7)
			self.y_vel = random.randint(0, 4)

		elif self.type == "gravity":
			self.x_direction = random.randint(-1, 1)
			self.x_vel = random.choice([-0.6,-0.4,-0.2,0,0.2,0.4,0.6])
			self.y_vel = random.randint(-4, 0)

		elif self.type == "smoke":
			self.x_direction = random.randint(-1, 1)
			self.y_direction = -1
			self.x_vel = random.randint(-4, 4)
			self.y_vel = 3

		elif self.type == "friendly_muzzle":
			self.x_direction = 1
			self.y_direction = random.choice([-0.6,-0.4,-0.2,0,0.2,0.4,0.6])
			self.x_vel = random.randint(1, 4)
			self.y_vel = random.randint(1, 4)

		elif self.type == "enemy_muzzle":
			self.x_direction = -1
			self.y_direction = random.choice([-0.6,-0.4,-0.2,0,0.2,0.4,0.6])
			self.x_vel = random.randint(1, 4)
			self.y_vel = random.randint(1, 4)

		elif self.type == "none":
			self.x_direction = random.randint(-1, 1)
			self.y_direction = random.randint(-1, 1)
			self.x_vel = random.randint(0, 4)
			self.y_vel = random.randint(0, 4)


	def move(self):
		# method to determine how every particle should move
		x_camera_offset_dif = self.starting_camera_offset - game.camera_offset_x

		if self.type == "gravity":
			# particle moves in random direction and gets pulled down by gravity
			self.y_vel += game.GRAVITY
			self.x_pos += self.x_direction * self.x_vel
			self.y_pos += self.y_vel

		elif self.type == "no_gravity":
			# particle moves in random direction
			self.x_pos += self.x_direction * self.x_vel
			self.y_pos += self.y_direction * self.y_vel

		elif self.type == "friendly_muzzle" or self.type == "enemy_muzzle":
			self.x_pos += self.x_direction * self.x_vel
			self.y_pos += self.y_direction * self.y_vel

		elif self.type == "smoke":
			# particle moves in random dircetion an x axis and up
			self.x_pos += self.x_direction * self.x_vel
			self.y_pos += self.y_direction * self.y_vel

		# assign pos variables to rect atribute
		self.rect.topleft = (self.x_pos - x_camera_offset_dif, self.y_pos)


	def check_lifetime(self):
		# if max lifetime is reached remove particle
		self.lifetimer += 1
		if self.lifetimer == self.lifetime:
			game.particles.pop(game.particles.index(self))


	def create_transparent_surf(self):
		# create surface object to allow for transparent particles
		surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		surf.fill(self.color)
		return surf


	def draw(self):
		for particle in game.particles:
			if not particle.type == "none":
				game.screen.blit(particle.create_transparent_surf(), particle.rect)

	def update(self):
		for particle in game.particles:
			particle.check_lifetime()
			particle.move()

	def spawn_explosion(self, pos:tuple, smoke_color:tuple, 
						smoke_lifetime:int, color_1:tuple, 
						color_1_lifetime:int, color_2:tuple, 
						color_2_lifetime:int, part_size:tuple, 
						part_count:int):
		
		for i in range(part_count):
			smoke_particle = Particle(smoke_color, part_size, pos, smoke_lifetime, "smoke", 40)
			game.particles.append(smoke_particle)

			particle_gravity = Particle(color_1, part_size, pos, color_1_lifetime, "gravity")
			game.particles.append(particle_gravity)
			particle_gravity = Particle(color_1, part_size, pos, color_1_lifetime, "no_gravity")
			game.particles.append(particle_gravity)

			particle_no_gravity = Particle(color_2, part_size, pos, color_2_lifetime, "gravity")
			game.particles.append(particle_no_gravity)
			particle_no_gravity = Particle(color_2, part_size, pos, color_2_lifetime, "no_gravity")
			game.particles.append(particle_no_gravity)

	def muzzle_flash(self, pos:tuple, color1:tuple, color2:tuple, color3:tuple, size:tuple, 
								part_count:int, lifetime:float, friendly:bool):
		for i in range(part_count):
			if friendly == True:
				color1 = Particle(color1, size, pos, lifetime, "friendly_muzzle")
				color2 = Particle(color2, size, pos, lifetime, "friendly_muzzle")
				color3 = Particle(color3, size, pos, lifetime, "friendly_muzzle")
				game.particles.append(color1)
				game.particles.append(color2)
				game.particles.append(color3)
			else:
				color1 = Particle(color1, size, pos, lifetime, "enemy_muzzle")
				color2 = Particle(color2, size, pos, lifetime, "enemy_muzzle")
				color3 = Particle(color3, size, pos, lifetime, "enemy_muzzle")
				game.particles.append(color1)
				game.particles.append(color2)
				game.particles.append(color3)


class Meteor():
	def __init__(self, pos):
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.fall_speed = 4
		self.spawntimer = 0
		self.spawntimer_goal = 5
		self.duration_timer = 0
		self.duration_timer_goal = 7*60
		self.rain = False
		self.animation_state = 0
		self.animation_timer = 0
		self.animation_timer_goal = 5
		self.frame1_surf = game.tier1_special_sheet.get_image(0, (32, 64), (1,0,0), 1)
		self.frame2_surf = game.tier1_special_sheet.get_image(1, (32, 64), (1,0,0), 1)
		self.frame3_surf = game.tier1_special_sheet.get_image(2, (32, 64), (1,0,0), 1)
		self.frame4_surf = game.tier1_special_sheet.get_image(3, (32, 64), (1,0,0), 1)
		self.rect = self.frame1_surf.get_rect()
		self.rect.topleft = (self.x_pos + game.camera_offset_x, self.y_pos)

	def spawn_meteor(self):
		meteor = Meteor((random.randint(0, 1920), -128))
		game.meteors.append(meteor)

	def spawn_meteor_rain(self):
		if self.rain:
			if self.duration_timer <= self.duration_timer_goal:
				self.duration_timer += 1
				self.spawntimer += 1
				if self.spawntimer >= self.spawntimer_goal:
					self.spawn_meteor()
					self.spawntimer = 0
	
			else:
				self.duration_timer = 0
				self.rain = False

	def move(self):
		for meteor in game.meteors:
			meteor.rect.x = meteor.x_pos + game.camera_offset_x
			
			meteor.y_pos += meteor.fall_speed
			meteor.rect.y = meteor.y_pos

			if meteor.y_pos > 600:
				game.meteors.pop(game.meteors.index(meteor))

	def update_animation_state(self):
		for meteor in game.meteors:
			meteor.animation_timer += 1
			if meteor.animation_timer == meteor.animation_timer_goal:
				if meteor.animation_state == 0:
					meteor.animation_state = 1
				elif meteor.animation_state == 1:
					meteor.animation_state = 2
				elif meteor.animation_state == 2:
					meteor.animation_state = 3
				elif meteor.animation_state == 3:
					meteor.animation_state = 0
				meteor.animation_timer = 0

	def draw(self):
		for meteor in game.meteors:
			if meteor.animation_state == 0:
				game.screen.blit(self.frame1_surf, meteor.rect)
			if meteor.animation_state == 1:
				game.screen.blit(self.frame2_surf, meteor.rect)
			if meteor.animation_state == 2:
				game.screen.blit(self.frame3_surf, meteor.rect)
			if meteor.animation_state == 3:
				game.screen.blit(self.frame4_surf, meteor.rect)

	def check_if_unit_hit(self):
		for unit in game.enemy_units:
			for meteor in game.meteors:
				if meteor.rect.colliderect(unit.unit_rect):
					unit.get_hurt(unit.health + 20)
			

	def update(self):
		self.spawn_meteor_rain()
		self.move()
		self.update_animation_state()
		self.check_if_unit_hit()





class Arrow():
	def __init__(self, pos):
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.fall_speed = 6
		self.spawntimer = 0
		self.spawntimer_goal = 3
		self.duration_timer = 0
		self.duration_timer_goal = 7*60
		self.rain = False
		self.frame1_surf = game.tier2_special_sheet.get_image(0, (8, 16), (1,0,0), 2)
		self.rect = self.frame1_surf.get_rect()
		self.rect.topleft = (self.x_pos + game.camera_offset_x, self.y_pos)

	def spawn_arrow(self):
		arrow = Arrow((random.randint(0, 1920), -128))
		game.arrows.append(arrow)

	def spawn_arrow_rain(self):
		if self.rain:
			if self.duration_timer <= self.duration_timer_goal:
				self.duration_timer += 1
				self.spawntimer += 1
				if self.spawntimer >= self.spawntimer_goal:
					self.spawn_arrow()
					self.spawntimer = 0
	
			else:
				self.duration_timer = 0
				self.rain = False

	def move(self):
		for arrow in game.arrows:
			arrow.rect.x = arrow.x_pos + game.camera_offset_x
			
			arrow.y_pos += arrow.fall_speed
			arrow.rect.y = arrow.y_pos

			if arrow.y_pos > 600:
				game.arrows.pop(game.arrows.index(arrow))


	def draw(self):
		for arrow in game.arrows:
			game.screen.blit(self.frame1_surf, arrow.rect)
			

	def check_if_unit_hit(self):
		for unit in game.enemy_units:
			for arrow in game.arrows:
				if arrow.rect.colliderect(unit.unit_rect):
					unit.get_hurt(unit.health + 20)
					game.arrows.pop(game.arrows.index(arrow))
			

	def update(self):
		self.spawn_arrow_rain()
		self.move()
		self.check_if_unit_hit()



class A10:
	def __init__(self):
		self.altitude = 200
		self.x_pos = -500
		self.movement_speed = 8
		self.shoottimer = 0
		self.shoottimer_goal = 3
		self.animation_state = 0
		self.animation_timer = 0
		self.animation_timer_goal = 15
		self.frame1_surf = game.tier3_special_sheet.get_image(0, (64, 32), (1,0,0), 2)
		self.frame2_surf = game.tier3_special_sheet.get_image(1, (64, 32), (1,0,0), 2)
		self.rect = self.frame1_surf.get_rect()

	def spawn(self):
		a10 = A10()
		game.planes.append(a10)
	
	
	def shoot(self):
		for plane in game.planes:
			plane.shoottimer += 1
			if plane.shoottimer == plane.shoottimer_goal:
				plane.shoottimer = 0
				bullet.spawn(plane.rect.center)

	def move(self):
		for plane in game.planes:
			plane.x_pos += plane.movement_speed
			plane.rect.topleft = (plane.x_pos + game.camera_offset_x, plane.altitude)
			if plane.x_pos >= 1920:
				game.planes.pop(game.planes.index(plane))

	def update_animation_state(self):
		for plane in game.planes:
			plane.animation_timer += 1
			if plane.animation_timer == plane.animation_timer_goal:
				plane.animation_timer = 0
				if plane.animation_state == 0:
					plane.animation_state = 1
				elif plane.animation_state == 1:
					plane.animation_state = 0

	def draw(self):
		for plane in game.planes:
			if plane.animation_state == 0:
				game.screen.blit(plane.frame1_surf, plane.rect)
			elif plane.animation_state == 1:
				game.screen.blit(plane.frame2_surf, plane.rect)

	
	def update(self):
		self.move()
		self.shoot()
		self.update_animation_state()


class Bullet:
	def __init__(self, pos):
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.vel_x = random.randint(24, 26)
		self.vel_y = random.randint(9, 10)
		self.surf = game.tier3_special_bullet
		self.rect = self.surf.get_rect()

	def spawn(self, pos):
		bullet = Bullet(pos)
		game.bullets.append(bullet)

	def move(self):
		for bullet in game.bullets:
			bullet.x_pos += bullet.vel_x
			bullet.y_pos += bullet.vel_y
			bullet.rect.topleft = (bullet.x_pos, bullet.y_pos)
			if bullet.y_pos >= game.FLOOR_LEVEL:
				dirt.spawn_cluster(bullet.rect.center)
				game.bullets.pop(game.bullets.index(bullet))

	def check_if_collide_with_unit(self):
		for bullet in game.bullets:
			for unit in game.enemy_units:
				try:
					if bullet.rect.colliderect(unit.unit_rect):
						game.bullets.pop(game.bullets.index(bullet))
						unit.get_hurt(90)
				except ValueError:
					print("ValueError in A10 special check collision")

	def draw(self):
		for bullet in game.bullets:
			game.screen.blit(bullet.surf, bullet.rect)

	def update(self):
		self.move()
		self.check_if_collide_with_unit()






# creates "game"-object and master instances of other classes
game = Game()
meteor = Meteor((0,0))
arrow = Arrow((0,0))
plane = A10()
bullet = Bullet((0,0))
dirt = Dirt((0,0))
blood_master = Blood((100,100), False, (0,0,0), (1,1))
particle = Particle((0,0,0), (1,1), (0,0), 1, "none")
turret = Turret(False, 1, 1)
projectile = Projectile((0,0), (1,1), 1, 1, True)
unit_projectile = UnitProjectile((0,0), False, 2)
friendly_base = Base(True)
enemy_base = Base(False)
# master class to controll units
unit = Unit(False, 3)

# starts the main game loop
game.mainloop()

