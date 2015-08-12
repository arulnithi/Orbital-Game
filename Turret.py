import pygame
from pygame.sprite import Sprite

pygame.init()

class Turret(Sprite):
    def __init__(self,screen, position, angles, image):
        Sprite.__init__(self)
        self.screen=screen
        (self.x,self.y)=(position)
        (self.upperAngle,self.lowerAngle)=(max(angles), min(angles))
        #self.timer=timerPassed
        self.baseImage=image
        self.image=self.baseImage
        self.clockwise=False
        self.angleCount=self.lowerAngle
        (self.iwidth, self.iheight)=(self.image.get_width(),self.image.get_height())
        self.rotate=True
        
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

    def draw(self,data,angle):
        if data.discActive==False:
            self.image=self.rot_center(self.baseImage,angle)
        #self.image.set_colorkey((255,255,255))
        self.screen.blit(self.image, (self.x-self.iwidth/2,self.y-self.iheight/2))

    def update(self,data):
        if data.discActive==False and self.rotate==True:
            if self.clockwise==False: self.angleCount+=0.5
            else: self.angleCount-=0.5
        if self.angleCount<=self.lowerAngle: self.clockwise=False
        elif self.angleCount>=self.upperAngle: self.clockwise=True
        self.draw(data,self.angleCount) 

    def getinfo(self):
        return ((self.x,self.y),self.angleCount)
        

        
        
        
        
