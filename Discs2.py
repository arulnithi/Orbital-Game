import pygame, math, random
from pygame.sprite import Sprite
from math import sin, cos, radians
from Planets import Planet
#from vec2d import vec2d
from Fizzle import Fizzle, Sparks

pygame.init()

class Discs(Sprite):
    def __init__(self, data, position, angle):
        Sprite.__init__(self)
        self.screen=data.screen
        (self.x,self.y)=position
        self.angle=math.radians(angle)
        self.baseImage=random.choice(data.discImgList)
        self.image=self.baseImage
        self.color = self.image.get_at((self.image.get_width()/2,
                                       self.image.get_height()/2))
        self.planets=data.planets
        self.radius=5
        self.diameter=self.radius*2
        self.usedimage=pygame.transform.scale(self.image,(self.diameter, self.diameter))
        self.initialVelocity=self.velocity=12
        self.drag=0.2
        self.lastChangedDir=None
        self.firstPass=False
        self.rect=self.usedimage.get_rect()
        (self.swidth,self.sheight)=(data.swidth,data.sheight)
        (self.lowerBound,self.upperBound)=(data.gameLowerBound,data.gameUpperBound)
        self.stopExpansion=False


    def newVelocity(self):
        velocity=self.velocity*(1-self.drag/100.0)
        self.velocity=max(0,velocity-0.08)

    def gravity(self):
        gravity=[ix,iy]=[0,0]
        for planet in self.planets:
            dx=(self.x-planet.x)
            dy=(self.y-planet.y)
            distance = math.hypot(dx, dy)
            gravForce=planet.mass/(distance**2)
            if dx!=0:
                angle=math.atan(dy/dx)
                (ix,iy)=(gravForce*math.cos(angle),gravForce*math.sin(angle))
            else:
                (ix,iy)=(0,gravForce)
            (ix,iy)=(abs(ix),abs(iy))
            #print "(%0.2f %0.2f)"%(ix,iy),
            if dx>0: ix*= -1
            if dy>0: iy*= -1
            gravity[0]+=ix
            gravity[1]+=iy
            #print "G: %0.2f,%0.2f" %(gravity[0],gravity[1]),
        (vx,vy)=(self.velocity*math.cos(self.angle),self.velocity*math.sin(self.angle))
        #print "Velocity (%0.2f,%0.2f)" %(vx,vy),
        (fx,fy)=(vx+gravity[0], vy-gravity[1])
        self.angle=math.atan2(fy,fx)
        #print "Deg: %0.1f" %(math.degrees(self.angle))
            

    def newDirection(self,data):
        if data.mainCounter%10==0:
            self.lastChangedDir=None
            
        if (self.x<2  and self.lastChangedDir!="x<0"):
            self.angle=(math.pi-self.angle)
            self.angle=self.angleConvert(self.angle)
            #data.musicBounce.play()
            self.lastChangedDir="x<0"
        if (self.x>self.swidth-2 and self.lastChangedDir!="x>width"):
            self.angle=(math.pi-self.angle)
            self.angle=self.angleConvert(self.angle)
            #data.musicBounce.play()
            self.lastChangedDir="x>width"
        if (self.y<self.upperBound and self.lastChangedDir!="y<0"):
            if self.firstPass==False:
                pass
            else:
                if data.playerTurn==0 and data.gamePlayerMode=="Multi":
                    data.playerRoundOver=True
                else:
                    self.angle*= -1
                    #data.musicBounce.play()
                    self.lastChangedDir="y<0"
        if (self.y>self.lowerBound and self.lastChangedDir!="y>height"):
            if self.firstPass==False:
                pass
            else:
                if data.playerTurn==1 or data.gamePlayerMode=="Single":
                    data.playerRoundOver=True
                else:
                    self.angle*= -1
                    #data.musicBounce.play()
                    self.lastChangedDir="y>height"
 
        for planet in self.planets:
            if self.collided(planet):
                if self.lastChangedDir!=planet.name:
                    #data.musicBounce.play()
                    self.lastChangedDir=planet.name
                    self.collision(planet)
                
            
    def collided(self,planet):
        (x1,y1)=(self.x,self.y)
        (x2,y2)=(planet.x,planet.y)
        dx= x1-x2
        dy= y1-y2
        distance = math.hypot(dx, dy)
        if distance<=(self.radius+planet.radius):
            return True
        else: return False
            
    def collision(self,planet):
        self.angle=self.angleConvert(self.angle)
        planet.count-=1
        if self.velocity>0.1:
            self.velocity*=0.95
        angleApproach = self.angle
        dx=(self.x-planet.x)
        dy=-(self.y-planet.y)
        tangent = math.atan2(dy, dx)
        if dy==0:
            self.angle=(math.pi-self.angle)
        elif dx==0:
            self.angle*= -1
        elif (angleApproach<0 and dy>0 and dx<0):
            #print 1,
            self.angle= 2*tangent-math.pi-angleApproach
        elif (angleApproach>0 and dy>0 and dx<0):
            #print 2,
            self.angle= 2*tangent-math.pi-angleApproach
        elif (angleApproach>0 and dy>0 and dx>0):
            #print 3,
            self.angle= 2*tangent+math.pi-angleApproach
        elif (angleApproach<0 and dy>0 and dx>0):
            #print 4,
            self.angle= 2*tangent-math.pi-angleApproach
        elif (angleApproach<0 and dy<0 and dx>0):
            #print 5,
            self.angle= 2*tangent-angleApproach-math.pi
        elif (angleApproach>0 and dy<0 and dx>0):
            #print 6,
            self.angle= 2*tangent+math.pi-angleApproach
        elif (angleApproach>0 and dy<0 and dx<0):
            #print 7,
            self.angle= 2*tangent+math.pi-angleApproach
        elif (angleApproach<0 and dy<0 and dx<0):
            #print 8,
            self.angle= 2*tangent+math.pi-angleApproach
        #print "%0.1f %0.1f %0.1f %0.1f %0.1f" % (math.degrees(angleApproach),dx,dy, math.degrees(tangent),math.degrees(self.angle))
        self.angle=self.angleConvert(self.angle)
##        self.angle = 2*tangent - self.angle + math.pi
####        theta=math.atan(dy/dx)+math.pi/2
####        self.angle=(math.pi+2*theta - angle)
        
    #Converts any angle to pi>angle>-pi
    def angleConvert(self,x):
        x=math.degrees(x)
        newX=x%360
        if newX>180:
            newX-=360
        newX=math.radians(newX)
        return newX

    def expand(self):
        self.radius+=1
        self.usedimage=pygame.transform.smoothscale(self.image, (self.radius*2,self.radius*2))
        if ((self.x-self.radius)<=2 or (self.x+self.radius)>=self.swidth-2 or
            (self.y-self.radius)<=self.upperBound or (self.y+self.radius)>=self.lowerBound):
            self.radius-=1
            self.stopExpansion=True
        for planet in self.planets:
            if self.collided(planet):
                self.radius-=1
                self.stopExpansion=True                
        

    def draw(self):
        colourkey=self.usedimage.get_at((0,0))
        self.usedimage.set_colorkey(colourkey)
        self.screen.blit(self.usedimage,(self.x-self.radius,self.y-self.radius))

    def move(self):
        self.x+=(self.velocity*cos(self.angle))
        self.y-=(self.velocity*sin(self.angle))

    def gameUpdate(self,data):
        if data.gamePlayerMode=="Single":
            if data.playerRoundOver==True:
                data.gameGameOver=True
        elif data.gamePlayerMode=="Multi":
            if data.playerRoundOver==True:
                data.playerRoundTally[data.playerTurn]+=1
                data.playerRound+=1
                winCondition=((data.gameRoundsToWin+1)/2)
                if (data.playerRoundTally[0]==winCondition or
                    data.playerRoundTally[1]==winCondition):
                    data.gameGameOver=True
        if self.velocity==0 and data.collisionCounter!=0:
            data.playerScore+=data.collisionCounter**2
            data.collisionCounter=0

    def trail(self,data):
        colorList=[(143,0,255),(75,0,130),(0,0,255),(0,255,0),(255,255,0),
                   (255,127,0),(255,0,0)]
        color=colorList[int(self.velocity*(7.0/self.initialVelocity))]
        if self.velocity<4:
            trailNo=random.randint(1,3)
        else: trailNo=random.randint(1,7)
        for i in xrange(trailNo):
            trailCone=random.randint(1,90)
            trailAngle=self.angle-math.pi+math.radians(trailCone)
            data.sparkTrail.add(Sparks(trailAngle,(self.x, self.y),data,[color],"disc"))
        
        
        
        

    def update(self,data):
        if self.firstPass==False and (self.upperBound<self.y<self.lowerBound):
            self.firstPass=True

        (self.y>self.lowerBound or self.y<self.upperBound)
        self.newDirection(data)
        self.gameUpdate(data)
        if self.velocity>0:
            self.newVelocity()
            if data.gameGameMode=="Gravity":
                self.gravity()
            self.move()
            self.trail(data)
        else:
            if self.stopExpansion==False:
                self.expand()
            else:
                self.position=(self.x,self.y)
                self.planets.add(Planet(data, self.position,self.radius,
                                        self.usedimage))
                self.kill()
                data.discActive=False
        self.draw()
        
            
            

    
                                              
