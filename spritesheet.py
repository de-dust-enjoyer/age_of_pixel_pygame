import pygame

class SpriteSheet:
	def __init__(self, image):
		self.sprite_sheet = image

	def get_image(self, frame:int, size:tuple, color:tuple, scale:float):
		img = pygame.Surface(size).convert_alpha()
		img.fill(color)
		img.blit(self.sprite_sheet, (0, 0), (size[0] * frame, 0, size[0], size[1]))
		img = pygame.transform.scale(img, (size[0] * scale, size[1] * scale))
		img.set_colorkey(color)
		
		return img