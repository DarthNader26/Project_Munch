import pygame, os, Loader, random, math
from pygame.locals import *
from pygame.compat import geterror
from pygame import surfarray
from fractions import Fraction

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
                self.health = 1
                self.direction = 0
                self.range = 256
                self.speed = 2
                self.alert = False
                self.attention = 30
                self.timer = 0

                toughness = random.randrange(0,100)
                self.original_image = self.original_image.convert()
                pixel_array = pygame.surfarray.array3d(self.original_image)
                if toughness <= 60:
                        pixel_array[:,:,0:1] = 200
                        ##the last position is the RGB//0:2 means "start at 0, stop at 2"
                        ##this means it will cover 0 and 1
                        self.type = "weak" #Red tinted
                elif toughness >60 and toughness <= 85:
                        pixel_array[:,:,1:2] = 200
                        self.type = "tough" #Green tinted
                        self.health += 1
                        self.speed -= 1
                        self.attention += 10
                elif toughness > 85:
                        pixel_array[:,:,2:3] = 200
                        self.type = "fast" #Blue tinted
                        self.speed += 1
                        self.attention -= 10
                self.original_image = pygame.surfarray.make_surface(pixel_array).convert()
                colorkey = self.original_image.get_at( (0,0) )
                self.original_image.set_colorkey( colorkey, RLEACCEL )
                
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
                
        def update(self, playerpos, mappos):
                self._hunt(playerpos)
                if self.alert:
                        angle = math.atan2(self.rect.center[0]-playerpos[0], self.rect.center[1]-playerpos[1])
                        self._turn(math.degrees(angle))
                        self.direction = angle
                        self._walk(playerpos[0], playerpos[1], mappos[0], mappos[1])
                else:
                        self._wander()
                        #comment out the next line to check for AI working
                        self._walk(playerpos[0], playerpos[1], mappos[0], mappos[1])
                
        def _walk(self, playerx, playery, mapx, mapy):
                newpos = self.rect.move((self.move))
                move = self.speed

                #Move the sprite for keydown values of walkx
                if playerx > self.rect.right:
                        self.move[0] = move
                elif playerx < self.rect.left:
                        self.move[0] = -move
                else:
                        self.move[0] = 0
                #Move the sprite for keydown values of walky
                if playery > self.rect.top:
                        self.move[1] = move
                elif playery < self.rect.bottom:
                        self.move[1] = -move
                else: 
                        self.move[1] = 0
                        
                if mapx > 0:
                        self.move[0] += -5
                elif mapx < 0:
                        self.move[0] += 5
                else:
                        self.move[0] += 0
                        
                if mapy > 0:
                        self.move[1] += -5
                elif mapy < 0:
                        self.move[1] += 5
                else:
                        self.move[1] += 0
                
                newpos = self.rect.move((self.move))
                self.rect = newpos

                
        def _turn(self, amount):
                "turn some amount"
                oldCenter = self.rect.center
                self.dir = amount
                self.image = pygame.transform.rotate(self.original_image, self.dir)
                self.rect.center = oldCenter

        def _wander(self):
                self.timer += 1
                if self.timer == self.attention:
                        self.timer = 0
                        delta = random.randrange(-90, 90)
                        angle = self.direction + delta
                        self._turn(math.degrees(angle))
                        self.direction = angle

                if self.direction > 0 and self.direction < 180:
                        deltaX = -1
                elif self.direction < 0 and self.direction > -180:
                        deltaX = 1
                else:
                        deltaX = 0
                if self.direction < 90 and self.direction > -90:
                        deltaY = -1
                elif self.direction > 90 and self.direction < -90:
                        deltaY = 1
                else:
                        deltaY = 0

                self.move[0] = deltaX 
                self.move[1] = deltaY
                
                newpos = self.rect.move((self.move))
                self.rect = newpos
                        
                
        def _hunt(self, playerpos):
                arm1 = [self.rect.center[0], self.rect.center[1]]
                arm2 = [self.rect.center[0], self.rect.center[1]]
                angle1 = self.direction - (math.pi * .25)
                angle2 = self.direction - (math.pi * .75)

                arm1[0] += self.range * math.cos(angle1)
                arm1[1] += self.range * math.sin(angle1)

                arm2[0] += self.range * math.cos(angle2)
                arm2[1] += self.range * math.sin(angle2)
                
                dist1 = math.sqrt( (playerpos[0] - arm1[0])**2 + (playerpos[1] - arm1[1])**2 )
                dist2 = math.sqrt( (playerpos[0] - arm2[0])**2 + (playerpos[1] - arm2[1])**2 )
                dist0 = math.sqrt( (playerpos[0] - self.rect.center[0])**2 + (playerpos[1] - self.rect.center[1])**2 )

                if dist1 <= self.range+128 and dist2 <= self.range+128 and dist0 <= (self.range + (self.range*.01)):
                        self.alert = True
                        self.timer = 0
                else:
                        self.alert = False

