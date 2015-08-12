import pygame, math
from pygame.sprite import Sprite
from math import sin, cos, radians

pygame.init()

class Planet(Sprite):
    planetCount=0
    def __init__(self, data, position, radius, image):
        Planet.planetCount+=1
        self.name="planet%d" %(Planet.planetCount)
        Sprite.__init__(self)
        self.screen=data.screen
        self.position=position
        (self.x,self.y)=position
        self.radius=radius
        self.baseImage=image
        self.image=self.baseImage
        self.rect= self.image.get_rect()
        self.color = self.image.get_at((self.image.get_width()/2,
                                       self.image.get_height()/2))
        massProportionality=0.1
        self.mass=massProportionality*(math.pi*self.radius**2)
        if data.gameGameMode=="Gravity":
            self.count=3
        else:
            self.count=5
        self.state=Planet.alive
        fontSize=max(12,self.radius)
        self.font = pygame.font.Font(None,fontSize)

    def draw(self):
        #colourkey=self.image.get_at((0,0))
        #self.image.set_colorkey(colourkey)
        self.screen.blit(self.image,(self.x-self.radius,self.y-self.radius))
        text = self.font.render(str(self.count), True, (169,0,207))
        textpos= text.get_rect()
        textpos.centerx=self.x
        textpos.centery=self.y
        self.screen.blit(text,textpos)

    def update(self,data):
        if self.count>0:   
            self.draw()
        else:
            data.collisionCounter+=1
            if data.gameGameMode=="SuperNova":
                data.rings.add(Ring(data, self.position,self.radius,
                                    self.color))
            self.kill()
                
                

class Ring(Sprite):
    def __init__(self,data,position,radius,color):
        Sprite.__init__(self)
        self.screen=data.screen
        self.position=(int(position[0]),int(position[1]))
        (self.x,self.y)=position
        self.radius=radius
        self.maxRadius=self.radius*2
        self.growth=1.5
        self.ringWidth=5
        self.color=color
        #self.time=0
        self.collidedSet=set()

    def collided(self,data):
        for planet in data.planets:
            (x1,y1)=(self.x,self.y)
            (x2,y2)=(planet.x,planet.y)
            dx= x1-x2
            dy= y1-y2
            distance = math.hypot(dx, dy)
            if distance<=(self.radius+planet.radius):
                if planet.name not in self.collidedSet:
                    planet.count-=1
                    self.collidedSet.add(planet.name)
        
    def draw(self):
        radius=int(self.radius)
        pygame.draw.circle(self.screen,self.color,self.position,
                           radius,self.ringWidth)

    def update(self,data):
        self.draw()
        self.collided(data)
        #self.time+=1
        self.radius+=self.growth
        if self.radius>=self.maxRadius:
            self.kill()
        
        
        
    
        
