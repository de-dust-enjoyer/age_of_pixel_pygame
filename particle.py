import pygame, random


class Particle:
	def __init__(self, color:tuple, size:tuple, starting_pos:tuple, lifetime:int, type:str, camera_offset_x:int = 0, alpha:int = 255):
		self.color = (color[0], color[1], color[2], alpha)
		self.width = size[0]
		self.height = size[1]
		self.starting_pos_x = starting_pos[0]
		self.starting_pos_y = starting_pos[1]
		self.lifetime = lifetime * 60
		self.type = type
		self.starting_camera_offset = camera_offset_x
		self.rect = pygame.Rect(self.starting_pos_x, self.starting_pos_y, self.width, self.height)
		self.display_surf = game.screen
		print(self.display_surf)











