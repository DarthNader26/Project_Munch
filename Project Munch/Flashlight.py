import pygame, os
from pygame.locals import *
from pygame.compat import geterror

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

flashlightCone = 30

def calculateSlope(playerx, playery, mousex, mousey):
	slope = (playerx - mousex) / (playery - mousey)
	return slope
	
def calculatePoints(playerx, playery, mousex, mousey):
	