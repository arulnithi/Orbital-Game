import pygame, math, random
from pygame.sprite import Sprite


def Fizzle(xcoord, ycoord, laserAngle, collision,data):
    red=(255,0,0)
    if collision == "top":
        angle=-math.pi
        color=(255,255,255)
    elif collision == "bottom":
        angle=0
        color=(255,255,255)
    elif collision == "left":
        angle= -math.pi/2
        color=(255,255,255)
    elif collision == "right":
        angle= -math.pi*3/2
        color=(255,255,255)
    else:
        (px,py)=(collision.x,collision.y)
        (sx,sy)=(xcoord, ycoord)
        (dx,dy)=(sx-px,-(sy-py))
        angle = math.atan2(dy, dx)-math.pi/2
        color=collision.color
        
    direction= random.randint(1,180)
    newAngle= angle + (direction/180.0)*math.pi
    data.sparks.add(Sparks(newAngle,(xcoord, ycoord),data,[red,color]))
    


    
    
        
class Sparks(Sprite):
    def __init__(self, angle, position,data,color,trail=None):   
        Sprite.__init__(self)
        self.screen=data.screen
        self.colorList=color
        self.time=0
        if trail==None:
            self.velocity=random.randint(1,2)
        elif trail == "disc":
            self.velocity=0.5
        self.originalColor=random.choice(self.colorList)
        self.color=self.originalColor
        #print self.originalColor
        self.angle=angle
        (self.x,self.y)=position
        self.rect=pygame.Rect(self.x,self.y,2,2)
                
##    def glow(self,data):
##        collideList=[]
##        collideList=pygame.sprite.spritecollide(self, data.sparks, False)
##        print len(collideList),len(data.sparks)
##        if len(self.originalColor)==3: (rVal,gVal,bVal)=self.originalColor
##        else: (rVal,gVal,bVal,alpha)=self.originalColor
##        for spark in collideList:
##            rVal+=4
##            gVal+=4
##            bVal+=4
##        rVal=min(255,rVal)
##        gVal=min(255,gVal)
##        bVal=min(255,bVal)
##        #self.color=self.originalColor
##        self.color=(rVal,gVal,bVal)
        
        
        
    def update(self,data):
        self.time+=1
        #self.glow(data)
        (self.x,self.y)=(self.x+self.velocity*math.cos(self.angle),
                         self.y-self.velocity*math.sin(self.angle))
        pygame.draw.rect(self.screen,self.color,(self.x,self.y,2,2))
        if self.time>60:
            self.kill()
        


        
