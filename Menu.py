import pygame, sys
from Turret import Turret
from ControlTurret import CTurret

class Menu(object):
    def __init__(self,data):
        self.screen=data.screen
        self.instructionList=data.instructionList
        fontSize=20
        self.font = pygame.font.SysFont('arial', fontSize)
        self.rect=self.screen.get_rect()
        self.colors=[(255,255,255),(255,0,255),(0,0,0)]
        self.indexCount=0
        self.indexSubCount=[0,0,0,0]
        self.menuMain=["Start Game", "Game Mode", "Instructions", "Quit"]
        self.menuMode=[["Single Player Mode", "Multi Player Mode"],
                       ["Best of [3] 5  7 ","Best of  3 [5] 7 ","Best of  3  5 [7]"],
                       ["Game Mode: Gravity", "Game Mode: SuperNova"],
                       ["Back"]]
        self.menuTextOffset=fontSize+10
        self.displayModeMenu=False
        self.displayInstructions=False

    def draw(self,data):
        if self.displayInstructions==True:
            if self.indexCount<3:
                instructionImg=self.instructionList[self.indexCount]
                displayImg=pygame.transform.scale(instructionImg,
                                           (data.swidth,data.sheight))
                self.screen.blit(displayImg, (0,0))
            else:
                self.indexCount=0
                self.displayInstructions=False
        elif self.displayModeMenu==False:
            for i in xrange(len(self.menuMain)):
                if i==self.indexCount:
                    color=self.colors[1]
                else:
                    color=self.colors[0]
                text= self.font.render(self.menuMain[i], True, color)
                textpos= text.get_rect()
                textpos.centerx=self.screen.get_width()/2
                textpos.centery=self.screen.get_height()/2 + i* self.menuTextOffset - len(self.menuMain)/2*self.menuTextOffset
                self.screen.blit(text,textpos)
        elif self.displayModeMenu==True:
            for i in xrange(len(self.menuMode)):
                if i==self.indexCount:
                    color=self.colors[1]
                else:
                    color=self.colors[0]
                text= self.font.render(self.menuMode[i][self.indexSubCount[i]], True, color)
                textpos= text.get_rect()
                textpos.centerx=self.screen.get_width()/2
                textpos.centery=self.screen.get_height()/2 + i* self.menuTextOffset - len(self.menuMode)/2*self.menuTextOffset
                self.screen.blit(text,textpos)            
            

    def keyPressed(self,event,data):
        if self.displayInstructions==True:
            self.indexCount+=1
        elif self.displayModeMenu==False:
            if event.key == pygame.K_UP:
                self.indexCount= (self.indexCount-1) % len(self.menuMain)
            elif event.key == pygame.K_DOWN:
                self.indexCount= (self.indexCount+1) % len(self.menuMain)
            elif event.key == pygame.K_SPACE:
                if self.menuMain[self.indexCount]== "Start Game":
                    data.gameStarted=True
                    gameCreate(data)
                elif self.menuMain[self.indexCount]== "Game Mode":
                    self.displayModeMenu=True
                    self.indexCount=0
                elif self.menuMain[self.indexCount]== "Instructions":
                    self.displayInstructions=True
                    self.indexCount=0
                elif self.menuMain[self.indexCount]== "Quit":
                    data.gameQuit=True
        elif self.displayModeMenu==True:
            if event.key == pygame.K_UP:
                self.indexCount= (self.indexCount-1) % len(self.menuMode)
            elif event.key == pygame.K_DOWN:
                self.indexCount= (self.indexCount+1) % len(self.menuMode)
            elif event.key == pygame.K_LEFT:
                self.indexSubCount[self.indexCount]+=1
                self.indexSubCount[self.indexCount]%=len(self.menuMode[self.indexCount])
            elif event.key == pygame.K_RIGHT:
                self.indexSubCount[self.indexCount]-=1
                self.indexSubCount[self.indexCount]%=len(self.menuMode[self.indexCount])                
            elif event.key == pygame.K_SPACE:
                if self.menuMode[self.indexCount][self.indexSubCount[self.indexCount]]== "Back":
                    self.displayModeMenu=False
                    self.indexCount=0
                    
    def dataUpdate(self,data):
        if self.displayModeMenu==True:
            if self.indexSubCount[0]==0:
                data.gamePlayerMode="Single"
            elif self.indexSubCount[0]==1:
                data.gamePlayerMode="Multi"
            if self.indexSubCount[1]==0:
                data.gameRoundsToWin=3
            elif self.indexSubCount[1]==1:
                data.gameRoundsToWin=5
            elif self.indexSubCount[1]==2:
                data.gameRoundsToWin=7
            if self.indexSubCount[2]==0:
                data.gameGameMode="Gravity"
            elif self.indexSubCount[2]==1:
                data.gameGameMode="SuperNova"
                
    def update(self,event,data):
        self.keyPressed(event,data)
        self.dataUpdate(data)

def gameCreate(data):
    data.turrets=[]
    if data.gameGameMode=="Gravity":
        turret1= Turret(data.screen, (data.swidth/2,data.sheight), (10,170), data.turret)
        data.turrets+=[turret1]
        if data.gamePlayerMode=="Multi":
            data.gameUpperBound=70
            data.playerTotal=2
            turret2= Turret(data.screen, (data.swidth/2,0), (-10,-170), data.turret)
            data.turrets+=[turret2]
    elif data.gameGameMode=="SuperNova":
        turret1= CTurret(data.screen, (data.swidth/2,data.sheight), (10,170), data.turret)
        data.turrets+=[turret1]
        if data.gamePlayerMode=="Multi":
            data.gameUpperBound=70
            data.playerTotal=2
            turret2= CTurret(data.screen, (data.swidth/2,0), (-10,-170), data.turret)
            data.turrets+=[turret2]

class PauseMenu(object):
    def __init__(self,data):
        self.screen=data.screen
        fontSize=20
        self.font = pygame.font.SysFont('arial', fontSize)
        self.rect=self.screen.get_rect()
        self.colors=[(255,255,255),(255,0,255),(0,0,0)]
        self.indexCount=0
        self.menuMain=["Resume", "Main Menu", "Quit"]
        self.menuTextOffset=fontSize+10

    def draw(self):
        rect = pygame.Surface((self.screen.get_width(),
                               120),pygame.SRCALPHA, 32)
        rect.fill((229, 255, 204, 2))
        self.screen.blit(rect,(0,self.screen.get_width()/2+40))
                                            
        for i in xrange(len(self.menuMain)):
            if i==self.indexCount:
                color=self.colors[2]
            else:
                color=self.colors[0]
            text= self.font.render(self.menuMain[i], True, color)
            textpos= text.get_rect()
            textpos.centerx=self.screen.get_width()/2
            textpos.centery=self.screen.get_height()/2 + i* self.menuTextOffset - len(self.menuMain)/2*self.menuTextOffset
            self.screen.blit(text,textpos)
            
    def quitGame(self,event):
        pressedKeys= pygame.key.get_pressed()
        altPressed = pressedKeys[pygame.K_LALT] or pressedKeys[pygame.K_RALT]
        closeButton= (event.type== pygame.QUIT)
        altF4 = altPressed and event.type==pygame.KEYDOWN and event.key==pygame.K_F4
        escape = event.type ==pygame.KEYDOWN and event.key== pygame.K_ESCAPE
        return closeButton or altF4 or escape
    
    def keyPressed(self,event,data):
        if self.quitGame(event):
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_UP:
            self.indexCount= (self.indexCount-1) % len(self.menuMain)
        elif event.key == pygame.K_DOWN:
            self.indexCount= (self.indexCount+1) % len(self.menuMain)
        elif event.key == pygame.K_SPACE:
            if self.menuMain[self.indexCount]== "Resume":
                data.gamePaused=False
            elif self.menuMain[self.indexCount]== "Main Menu":
                data.playerTurn=0
                if data.discActive==True:
                    data.disc.kill()
                data.initialize= True
                data.gamePaused=False
                
            elif self.menuMain[self.indexCount]== "Quit":
                pygame.quit()
                sys.exit()
                    
                
    def update(self,event,data):
        self.keyPressed(event,data)


class StatusDisplay(object):
    def __init__(self,data):
        self.screen=data.screen
        fontSize=20
        self.font = pygame.font.SysFont('arial', fontSize)
        self.rect=self.screen.get_rect()
        self.colors=[(255,255,255),(255,0,255),(0,0,0)]
        self.menuTextOffset=fontSize+10
        
        
    def draw(self,data):
        rect = pygame.Surface((self.screen.get_width(),
                               120),pygame.SRCALPHA, 32)
        rect.fill((229, 255, 204, 2))
        self.screen.blit(rect,(0,self.screen.get_width()/2+40))
        if data.gamePlayerMode=="Single":
            scoreText= "Your Score is: %d" %(data.playerScore)
            textMenu= [ scoreText, "Press 'r' to restart", "Press any other key for Menu"]
        else:
            if data.gameGameOver!=True:
                currentPlayer=  (data.playerTurn+2)%2 + 1
                winningText= "Player %d scores!" % (currentPlayer)
                textMenu= [winningText, "Press any key to continue"]
            else:
                if data.playerRoundTally[0]>data.playerRoundTally[1]: winner=1
                else: winner=2
                winningText= "Player %d wins!" % (winner)
                textMenu= [ winningText, "Press 'r' to restart", "Press any other key for Menu"]
        for i in xrange(len(textMenu)):
            text= self.font.render(textMenu[i], True, self.colors[2])
            textpos= text.get_rect()
            textpos.centerx=self.screen.get_width()/2
            textpos.centery=self.screen.get_height()/2 + i* self.menuTextOffset - len(textMenu)/2*self.menuTextOffset
            self.screen.blit(text,textpos)
        

    def keyPressed(self,event,data):
        if data.gamePlayerMode=="Single" or data.gameGameOver==True:
            if event.key == pygame.K_r:
                gameCreate(data)
                data.gameStarted=True
                data.planets.empty()
                data.sparkTrail.empty()
                data.sparks.empty()
                data.rings.empty()
                data.playerRound=1
                data.playerScore=0
                data.playerRoundTally=[0,0]
                data.playerTurn=0
                data.gameGameOver=False
                if data.discActive==True:
                    data.discActive=False
                    data.disc.kill()                
                data.playerRoundOver=False
            elif event.type == pygame.KEYDOWN:

                if data.discActive==True:
                    #data.discActive=False
                    data.disc.kill() 
                data.playerRoundOver=False
                data.gameStarted=False
                data.initialize= True
        else:
            if event.type == pygame.KEYDOWN:
                data.planets.empty()
                data.sparkTrail.empty()
                data.sparks.empty()
                data.rings.empty()
                if data.discActive==True:
                    data.discActive=False
                    data.disc.kill() 
                data.playerRoundOver=False

                    
                
    def update(self,event,data):
        self.keyPressed(event,data)


class DisplayUI(object):
    def __init__(self,data):
        self.screen=data.screen
        self.fontSize=20
        self.font = pygame.font.SysFont('arial', self.fontSize)
        self.rect=self.screen.get_rect()
        self.colors=[(255,255,255),(255,0,255)]
        self.shield=pygame.Surface((data.swidth,data.turretHeight),pygame.SRCALPHA)
        self.shield.fill((255,255,255,128))
        self.lastPlayer=0
        self.shieldTimer=0
        

    def update(self,data):
        self.draw(data)

    def draw(self,data):
        if data.gamePlayerMode=="Single":
            scoreText= "Score: %d" %(data.playerScore)
            text= self.font.render(scoreText, True, self.colors[0])
            self.screen.blit(text,(0,data.sheight-self.fontSize))
##            pygame.draw.line(self.screen,self.colors[0],[0,data.gameLowerBound],
##                             [data.swidth,data.gameLowerBound],5)
            rect=[0,data.gameUpperBound,data.swidth,data.gameLowerBound+5]
            pygame.draw.rect(self.screen,self.colors[0],rect,3)
                             
        elif data.gamePlayerMode=="Multi":
##            pygame.draw.line(self.screen,self.colors[0],[0,data.gameLowerBound+5],
##                             [data.swidth,data.gameLowerBound+5],5)
##            pygame.draw.line(self.screen,self.colors[0],[0,data.gameUpperBound-5],
##                             [data.swidth,data.gameUpperBound-5],5)
            innerRect=[0,data.gameUpperBound-5,data.swidth,
                  data.gameLowerBound-data.gameUpperBound+10]
            outerRect=[0,0,data.swidth,data.sheight]
            pygame.draw.rect(self.screen,self.colors[0],innerRect,3)
            pygame.draw.rect(self.screen,self.colors[0],outerRect,3)
            [player1Count,player2Count]=data.playerRoundTally
            for i in xrange((data.gameRoundsToWin+1)/2):
                if i<player1Count:
                    pygame.draw.rect(self.screen,self.colors[1],
                                     [5+20*i,data.sheight-40,15,30])
                elif i>=player1Count:
                    pygame.draw.rect(self.screen,self.colors[1],
                                     [5+20*i,data.sheight-40,15,30],2)

                if i<player2Count:
                    pygame.draw.rect(self.screen,self.colors[1],
                                     [data.swidth-20-20*i,10,15,30])
                elif i>=player2Count:
                    pygame.draw.rect(self.screen,self.colors[1],
                                     [data.swidth-20-20*i,10,15,30],2)
            if data.playerTurn==0:
                if data.discActive==False and self.lastPlayer!=1:
                    self.lastPlayer=1
                    self.shieldTimer=0
                    self.shieldLocation=-data.turretHeight

                self.shieldTimer+=1
                if self.shieldTimer<=(data.fps+5):
                    self.shieldLocation+=int((data.turretHeight*1.0)/data.fps)
                    
            elif data.playerTurn==1:
                if data.discActive==False and self.lastPlayer!=0:
                    self.lastPlayer=0
                    self.shieldTimer=0
                    self.shieldLocation=data.sheight

                self.shieldTimer+=1
                if self.shieldTimer<=(data.fps+5):
                    self.shieldLocation-=int((data.turretHeight*1.0)/data.fps)

            self.currentShieldLocation=(0,self.shieldLocation)
            self.screen.blit(self.shield,self.currentShieldLocation)

                
                    
                    
                
                    
                    
            
                             
        
            


        
