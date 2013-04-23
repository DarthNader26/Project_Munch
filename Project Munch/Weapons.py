import pygame, os, Loader, time
from pygame.locals import *
from pygame.compat import geterror

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')
	
class Weapons(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = Loader.load_image('crosshair.png', -1)
		self.rateOfFire = 60
		self.ammunition = 10
		self.weapons_sound = Loader.load_sound('pow.wav')
		self.weapons_empty = Loader.load_sound('nomorebullets.wav')
		self.weapons_reloading = Loader.load_sound('reloading.wav')
		self.reloading = False
		self.cooldown = False
		self.reloadframes = 0
		
	def update(self):
		pos = pygame.mouse.get_pos()
		self.rect.midtop = (pos[0], pos[1]-16)
		if (self.reloadframes > 0):
			self.reloadframes = self.reloadframes - 1
		else:
			self.reloading = False
			self.cooldown = False
			
	def shoot(self):
		if (self.cooldown == False):
			if (self.ammunition > 0 and self.reloading == False):
				self.weapons_sound.play()
				self.ammunition = self.ammunition - 1
				self.reloadframes = self.rateOfFire
				self.cooldown = True
				return True
			else:
				self.weapons_empty.play()
				return False

	def reload(self):
		self.reloading = True
		self.ammunition = 10
		self.reloadframes = 180
		pygame.mixer.stop()
		self.weapons_reloading.play()
			