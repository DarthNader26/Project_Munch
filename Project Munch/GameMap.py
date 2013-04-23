import pygame, os, Loader


class GameMap():
	def __init__(self, screenDimensions):
		main_dir = os.path.split(os.path.abspath(__file__))[0]
		data_dir = os.path.join(main_dir, 'data')
		self.image, self.view_rect = Loader.load_image('map.png', -1)
		print ("Map Initialized!")
		self.screenwidth = screenDimensions[0]
		self.screenheight = screenDimensions[1]
		self.mapwidth = 4000
		self.mapheight = 4000
		self.scrollx = 5		#how many pixels to adjust map when moving in x direction
		self.scrolly = 5		#how many pixels to adjust map when moving in y direction
		self.mapcorner = [0,0]	#x,y coordinates for currently viewed map image (upper-left pixel)
		
	def update(self, mapx, mapy):
		self._scroll(mapx, mapy)
		
	def _scroll(self, mapx, mapy):
		newpos = self.mapcorner
		if mapx > 0:
			newpos[0] += 5
		elif mapx < 0:
			newpos[0] += -5
		else:
			newpos[0] += 0
			
		if mapy > 0:
			newpos[1] += 5
		elif mapy < 0:
			newpos[1] += -5
		else:
			newpos[1] += 0
		
		#update visible subsurface of large map
		#mapobj.mapcorner[0] += move_mapx
		#mapobj.mapcorner[1] += move_mapy
		
		#keep map in bounds of image
		if newpos[0] < 0:
			self.mapcorner[0] = 0
			move_mapx = 0
		elif newpos[0] > self.mapwidth - self.screenwidth:
			self.mapcorner[0] = self.mapwidth - self.screenwidth
			move_mapx = 0
		if newpos[1] < 0:
			self.mapcorner[1] = 0
			move_mapy = 0
		elif newpos[1] > self.mapheight - self.screenheight:
			self.mapcorner[1] = self.mapheight - self.screenheight
			move_mapy = 0
			
		self.mapcorner = newpos