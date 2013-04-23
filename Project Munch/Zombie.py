import pygame, os, Loader, random, math
from pygame.locals import *
from pygame.compat import geterror

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')
	
class Zombie(pygame.sprite.Sprite):
	#Creates the zombie object
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.original_image, self.rect = Loader.load_image('Zombie.png', -1)
		self.rect = self.rect.inflate(-10, -10)
		self.image = self.original_image
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		while True:
			selfx = random.randrange(-100, 1124)
			if selfx > 1024 or selfx < 0:
				break
		while True:
			selfy = random.randrange(-100, 868)
			if selfy > 868 or selfy > -100:
				break
		self.rect.topleft = selfx, selfy
		self.move = [0, 0]
		print ("Zombie loaded!")
		
	def update(self, playerpos):
		self._walk(playerpos[0], playerpos[1])
		angle = math.atan2(self.rect.center[0]-playerpos[0], self.rect.center[1]-playerpos[1])
		self._turn(math.degrees(angle))
		#self._turn()
	
		
	def _walk(self, playerx, playery):
		newpos = self.rect.move((self.move))
		#Move the sprite for keydown values of walkx
		if playerx > self.rect.right:
			self.move[0] = 1
		elif playerx < self.rect.left:
			self.move[0] = -1
		else:
			self.move[0] = 0
		#Move the sprite for keydown values of walky
		if playery > self.rect.top:
			self.move[1] = 1
		elif playery < self.rect.bottom:
			self.move[1] = -1
		else: 
			self.move[1] = 0
		
		newpos = self.rect.move((self.move))
		self.rect = newpos
		
	def _turn(self, amount):
		"turn some amount"
		oldCenter = self.rect.center
		self.dir = amount
		self.image = pygame.transform.rotate(self.original_image, self.dir)
		self.rect.center = oldCenter