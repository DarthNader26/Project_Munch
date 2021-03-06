#!/usr/bin/env python

#Import Modules
#Added random to the import list. That's the only change here.
import os, pygame, random, math, time, Player, Zombie, Weapons, Loader, Flashlight
from GameMap import GameMap
from pygame.locals import *
from pygame.compat import geterror

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

main_dir = os.path.split(os.path.abspath('Project Munch'))[0]
data_dir = os.path.join(main_dir, 'data')       
        
def main():

#Initialize Everything
		pygame.init()
		screen = pygame.display.set_mode((1024, 768))
		pygame.display.set_caption('Project Munch')
		pygame.mouse.set_visible(0)
		pygame.key.set_repeat(3, 3)

		#Load and display the splash screen while everything loads
		splash, splashRect = Loader.load_image('splashscreen.png', None)
		splash = splash.convert()
		screen.blit(splash, (0, 0))
		pygame.display.flip()

		time.sleep(1)

		#gamemap is the larger map image surface
		mapobj = GameMap([1024, 768])
		gamemap = pygame.Surface((mapobj.mapwidth, mapobj.mapheight))
		gamemap.blit( mapobj.image, ( mapobj.mapcorner[0], mapobj.mapcorner[1] ) )
		gamemap = gamemap.convert()



		#Initialize a few ints.
		print ("Everything initalized!")

		#Create The Backgound, a subsurface of the gamemap image surface
		background = pygame.Surface(screen.get_size())
		backgroundrect = background.get_rect()
		#get smaller map image for gameplay mode as a subsurface of the larger map
		background = gamemap.subsurface((mapobj.mapcorner[0], mapobj.mapcorner[1], 1024, 768))
		background = background.convert()
		print ("Background created!")


		#Display The Background
		screen.blit(background, (0, 0))
		pygame.display.flip()
		print ("Background printed!")

#Prepare Game Objects
		clock = pygame.time.Clock()
		#music = pygame.mixer.music.load('data/music.wav')
		player = Player.Player()
		weapons = Weapons.Weapons()
		playersprite = pygame.sprite.RenderPlain((player))
		zombies = pygame.sprite.Group()
		for x in range (0, 5):
				zombies.add(Zombie.Zombie())
		weaponsprite = pygame.sprite.RenderPlain((weapons))
		spawncounter = 0
		move_mapx = 0
		move_mapy = 0
		bullets = weapons.ammunition
		eat_sound = Loader.load_sound('eat.wav')
		dead_sound = Loader.load_sound('dead.wav')
		flashlightScreen = pygame.Surface(screen.get_size())
		flashlightScreen.set_colorkey((10, 10, 10))
		print ("Variables created!")
        
#Create the ammunition counter
		if pygame.font:
			font = pygame.font.Font(None, 36)
			text = font.render("Ammo " + str(bullets), 1, (200, 10, 10))
			textpos = text.get_rect(centerx = background.get_width()/2)
			background.blit(text, textpos)



#Main Loop
		going = True
		#music.play(-1, 0.0) 
		while going:
			clock.tick(60)
			   

                #Handle Input Events
			for event in pygame.event.get():
				if event.type == QUIT:
						going = False
				elif event.type == KEYDOWN and event.key == K_w:
						move_mapy = -1
				elif event.type == KEYDOWN and event.key == K_s:
						move_mapy = 1
				elif event.type == KEYDOWN and event.key == K_a:
						move_mapx = -1
				elif event.type == KEYDOWN and event.key == K_d:
						move_mapx = 1
				elif event.type == KEYDOWN and event.key == K_r:
						if weapons.reloading == False:
								weapons.reload()
								bullets = weapons.ammunition
								text = font.render("Ammo: " + str(bullets), 1, (200, 10, 10))
				elif event.type == KEYUP and event.key == K_w:
						move_mapy = 0
				elif event.type == KEYUP and event.key == K_s:
						move_mapy = 0
				elif event.type == KEYUP and event.key == K_a:
						move_mapx = 0
				elif event.type == KEYUP and event.key == K_d:
						move_mapx = 0
				elif event.type == MOUSEBUTTONDOWN:
						if (weapons.shoot() == True):
								#pygame.sprite.spritecollide(weapons, zombies, False)
								chump = pygame.sprite.spritecollideany(weapons, zombies)
								if chump != None:
										chump.health -= 1
										if chump.health <= 0:
												zombies.remove(chump)
								bullets = weapons.ammunition
								text = font.render("Ammo: " + str(bullets), 1, (200, 10, 10))
				elif event.type == MOUSEMOTION:
						mouseX, mouseY = pygame.mouse.get_pos()
						playerX, playerY = player.get_pos()
						angle = math.atan2(playerX-mouseX, playerY-mouseY)
						player.turn(math.degrees(angle))
			collidecheck = player.checkbounds(background)
			#move the map if the player didn't cross a boundary
			if(collidecheck == 0):
				mapobj.update(move_mapx, move_mapy)
				zombies.update(player.get_pos(), [move_mapx, move_mapy], background)
			elif(collidecheck == 1):
				mapobj.update(0, 1)
				zombies.update(player.get_pos(), [0, 1], background)
			elif(collidecheck == 2):
				mapobj.update(0, -1)
				zombies.update(player.get_pos(), [0, -1], background)
			elif(collidecheck == 3):
				mapobj.update(1, 0)
				zombies.update(player.get_pos(), [1, 0], background)
			elif(collidecheck == 4):
				mapobj.update(-1, 0)
				zombies.update(player.get_pos(), [-1, 0], background)

			weapons.update()
			
			#Check for a lose condition
			if pygame.sprite.spritecollideany(player, zombies) != None:
					eat_sound.play()
					time.sleep(2.5)
					dead_sound.play()
					time.sleep(3)
					pygame.quit()
			
			#Spawn a new zombie, if appropriate
			if spawncounter >= 30:
					zombies.add(Zombie.Zombie())
					spawncounter = 0
			else:
					spawncounter = spawncounter + 1
		#Draw Everything
			#background.fill((10,10,10))

			#subsurface of larger map image is copied to the background based upon previous player movement
			background = gamemap.subsurface((mapobj.mapcorner[0], mapobj.mapcorner[1], 1024, 768))
			

			mouseposition = pygame.mouse.get_pos()
			#pygame.draw.line(background, (255, 0, 0), player.rect.center, pygame.mouse.get_pos(), 1)
			screen.fill((0, 0, 0))
			screen.blit(background, (0, 0))
			playersprite.draw(screen)
			zombies.draw(screen)
			weaponsprite.draw(screen)
			flashlightScreen.fill((0, 0, 0))
			#flashlightArms = Flashlight.updateLight(player.get_pos(), angle)
			pygame.draw.circle(flashlightScreen, (10, 10, 10), player.get_pos(), 350, 0)
			flashlightScreen.blit(text, textpos)
			# pygame.draw.polygon(flashlightScreen, (30, 10, 10), (player.get_pos(), 200, 400), 0)
			screen.blit(flashlightScreen, (0, 0))
			pygame.display.flip()

                        
                
		pygame.quit()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
