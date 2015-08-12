import pygame, math
from pygame.sprite import Sprite
from Fizzle import Fizzle, Sparks


pygame.init()

class CTurret(Sprite):
    def __init__(self,screen, position, angles, image):
        Sprite.__init__(self)
        self.screen=screen
        (self.x,self.y)=(position)
        (self.upperAngle,self.lowerAngle)=(max(angles), min(angles))
        self.baseImage=image
        self.image=self.baseImage
        self.angleCount=self.lowerAngle
        (self.iwidth, self.iheight)=(self.image.get_width(),self.image.get_height())
        self.laserHit=False
        self.displayLaser=False
##        self.laserImg=data.laserImg
##        self.laserRect=self.laserImg.get_rect()
        

        
    """rot_centre code from: http://www.pygame.org/wiki/RotateCenter
       allows rotation around an image's centre, instead of corner"""
    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def draw(self,angle,data):
        self.image=self.rot_center(self.baseImage,angle)
       #self.image.set_colorkey((255,255,255))
        self.screen.blit(self.image, (self.x-self.iwidth/2,self.y-self.iheight/2))
        laser=Laser(data,(self.x,self.y),self.angleCount)
        if self.displayLaser==True:
            collide=None
            while self.laserHit==False:
                if (laser.x<0 or laser.x>data.swidth or laser.y<data.gameLowerBound
                    or laser.y>data.gameUpperBound):
                    if laser.x<2: (collide,self.laserHit)=("left",True)
                    if laser.x>data.swidth-2: (collide,self.laserHit)=("right",True)
                    if data.playerTurn==1:
                        if laser.y>data.gameLowerBound:
                            collide = "bottom"
                            self.laserHit=True
                    if data.playerTurn==0:
                        if laser.y<data.gameUpperBound:
                            collide = "top"
                            self.laserHit=True
                    
                for planet in data.planets:
                    if laser.collided(planet):
                        collide=planet
                        self.laserHit=True
                laser.update()
                if self.laserHit==True:
                    pass
                    Fizzle(laser.x,laser.y,laser.angle,collide,data)

                
            
            
        
    def keyPressed(self,event):
        if event.key == pygame.K_LEFT:
            if self.angleCount<self.upperAngle:
                self.angleCount+=1.0
        elif event.key == pygame.K_RIGHT:
            if self.angleCount>self.lowerAngle:
                self.angleCount-=1.0
        
    def update(self,data):
        if data.discActive==False:
            self.laserHit=False
        else: self.laserHit=True
        self.draw(self.angleCount,data) 

    def getinfo(self):
        return ((self.x,self.y),self.angleCount)
    
        
class Laser(Sprite):
    def __init__(self,data,position, angle):
        self.screen=data.screen
        self.image=data.laserImg
        self.rect=self.image.get_rect()
        (self.x,self.y)=(position)
        self.angle=math.radians(angle)
        self.y=self.y-(data.turretHeight/2.0)*math.sin(self.angle)
        self.x=self.x+(data.turretHeight/2.0)*math.cos(self.angle)
        self.rect.center=(self.x,self.y)
        self.radius=self.image.get_width()/2.0
        

    def draw(self):
        self.screen.blit(self.image,(self.x-self.radius,self.y-self.radius))

    def update(self):
        self.draw()
        self.x+=self.radius*math.cos(self.angle)
        self.y-=self.radius*math.sin(self.angle)

            
    def collided(self,planet):
        (x1,y1)=(self.x,self.y)
        (x2,y2)=(planet.x,planet.y)
        dx= x1-x2
        dy= y1-y2
        distance = math.hypot(dx, dy)
        if distance<=(self.radius+planet.radius):
            return True
        else: return False        
        
        
        
        
        

 
        
        
