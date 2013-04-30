import pygame, os, Loader
from pygame.locals import *
from pygame.compat import geterror

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')
	
class Player(pygame.sprite.Sprite):
	#Creates the player object
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.original_image, self.rect = Loader.load_image('Player.png', -1)
		self.image = self.original_image
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = 512, 384
		self.move = [0, 0]
		self.dir = 0.0
		print ("Player loaded!")
		
	def get_pos(self):
		position = self.rect.center
		return position
		
	def turn(self, amount):
		"turn some amount"
		oldCenter = self.rect.center
		self.dir = amount
		self.image = pygame.transform.rotate(self.original_image, self.dir)
		self.rect = self.image.get_rect()
		self.rect.center = oldCenter
		print self.image.get_rect()