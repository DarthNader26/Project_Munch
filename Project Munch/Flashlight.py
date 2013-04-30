import pygame, os, math
from pygame.locals import *
from pygame.compat import geterror

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

def updateLight(playerpos, angle):
	range = 64
	arm1 = [playerpos[0], playerpos[0]]
	arm2 = [playerpos[0], playerpos[0]]
	angle1 = angle - (math.pi * .25)
	angle2 = angle - (math.pi * .75)

	arm1[0] += range * math.cos(angle1)
	arm1[1] += range * math.sin(angle1)

	arm2[0] += range * math.cos(angle2)
	arm2[1] += range * math.sin(angle2)

	dist1 = math.sqrt( (playerpos[0] - arm1[0])**2 + (playerpos[1] - arm1[1])**2 )
	dist2 = math.sqrt( (playerpos[0] - arm2[0])**2 + (playerpos[1] - arm2[1])**2 )
	#dist0 = math.sqrt( (playerpos[0] - self.rect.center[0])**2 + (playerpos[1] - self.rect.center[1])**2 )
	
	return dist1, dist2