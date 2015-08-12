import pygame, sys, os
from Turret import Turret
from ControlTurret import CTurret
from Discs2 import Discs
from Menu import Menu, PauseMenu, StatusDisplay, DisplayUI

         


def quitGame(event,data):
    pressedKeys= pygame.key.get_pressed()
    altPressed = pressedKeys[pygame.K_LALT] or pressedKeys[pygame.K_RALT]
    closeButton= (event.type== pygame.QUIT)
    altF4 = altPressed and event.type==pygame.KEYDOWN and event.key==pygame.K_F4
    escape = event.type ==pygame.KEYDOWN and event.key== pygame.K_ESCAPE
    return closeButton or altF4 or escape or data.gameQuit




def ballsImageEditor(image,cuts):
    imgWidth=image.get_width()/cuts
    imgList=[]
    for i in xrange(4):
        rect= pygame.Rect(i*imgWidth,0,imgWidth,image.get_height())
        img= pygame.Surface(rect.size).convert()
        img.blit(image,(0,0),rect)
        imgList.append(img)
    return imgList


def init1(data,screen):
    #Initialize Permanent Values
    data.screen=screen
    (data.swidth,data.sheight)=(data.screen.get_width(),data.screen.get_height())
    data.turretHeight=70
    data.fps=90

    #Initialize Images
    data.baseBackground=pygame.image.load('background1.png')
    data.background=pygame.transform.scale(data.baseBackground,
                                           (data.swidth,data.sheight))
    data.turret=pygame.image.load('turret.png')#.convert()
    data.discSheet=pygame.image.load('balls.png')
    data.discImgList=ballsImageEditor(data.discSheet,4)
    data.laserImg=pygame.image.load('laser.png')
    data.instructionSheet=pygame.image.load('instruction.png')
    data.instructionList=ballsImageEditor(data.instructionSheet,3)
    
    #Initialize Music
    data.musicMain=pygame.mixer.Sound('NemesisTheory - Overdriven.ogg')
    data.musicMain.set_volume(0.1)
    data.musicMenu=pygame.mixer.Sound('menu.ogg')
    data.musicMenu.set_volume(0.3)
    data.musicMenuMove=pygame.mixer.Sound('menu_move.ogg')
    data.musicMenuMove.set_volume(0.5)
    data.musicMenuSelect=pygame.mixer.Sound('menu_select.ogg')
    data.musicMenuSelect.set_volume(0.5)
    pygame.mixer.music.load('laser_shooting_sfx.wav')
    #data.musicBounce=
    #data.musicBounce.set_volume(0.5)
    #pygame.mixer.music.play(-1)
    data.gameChannel = pygame.mixer.find_channel()
    data.gameChannel.play(data.musicMain,-1)
    data.gameChannel.pause()
    data.menuChannel = pygame.mixer.find_channel()
    data.menuChannel.play(data.musicMenu,-1)
    
    #Initialize Classes and Groups
    data.pauseMenu = PauseMenu(data)
    data.menu=Menu(data)
    data.status=StatusDisplay(data)
    data.displayUI=DisplayUI(data)
    data.planets=pygame.sprite.Group()
    data.sparks=pygame.sprite.Group()
    data.sparkTrail=pygame.sprite.Group()
    data.rings=pygame.sprite.Group()
    data.clock = pygame.time.Clock()
    

def init2(data):
    data.initialize= False
    
    #Initialize Values
    data.gameStarted=False
    data.gamePlayerMode="Single"
    data.gameRoundsToWin=3
    data.gameGameMode="Gravity"
    data.gamePaused=False
    data.gameGameOver=False
    data.gameQuit=False
    
    
    data.playerRound=1
    data.playerScore=0
    data.playerRoundTally=[0,0]
    data.playerTurn=0
    data.playerTotal=1
    data.playerRoundOver=False

    data.collisionCounter=0
    data.mainCounter=0
    data.discActive=False
    data.gameUpperBound=0
    data.gameLowerBound=data.sheight-data.turretHeight

    #Music Values
    data.menuMusicPlaying=False
    data.gameMusicPlaying=False
    
    
    
    #New Values Based on Game Mode
    data.turrets=[]
    data.planets.empty()
    data.sparks.empty()
    data.sparkTrail.empty()
    data.rings.empty()

def audioManager(data):
##    if data.gamePaused==True:
##        data.gameChannel.pause()
##        data.menuChannel.unpause()
    if data.gameStarted==False:
        data.gameChannel.play(data.musicMain,-1)
        data.gameChannel.pause()
        data.menuChannel.unpause()
    else:
        data.menuChannel.play(data.musicMenu,-1)
        data.menuChannel.pause()
        data.gameChannel.unpause()


def paused(data):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                data.pauseMenu.update(event,data)
                if data.gamePaused==False:
                    return
        data.pauseMenu.draw()
        pygame.display.flip()
        data.clock.tick(data.fps)


def gameStatus(data):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                data.status.keyPressed(event,data)
                if data.playerRoundOver==False:
                    return
        data.status.draw(data)
        pygame.display.flip()
        data.clock.tick(data.fps)

def runOrbitals():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.mixer.pre_init(44100,-16,2,512)
    pygame.init()
    screen=pygame.display.set_mode((400,600))
    gameName= pygame.display.set_caption('Orbitals')
    pygame.key.set_repeat (500, 10)
    
    #os.environ['SDL_VIDEO_WINDOW_POS'] = ''
    
    class Struct:pass
    data= Struct()
    init1(data,screen)
    init2(data)


    while True:
        data.mainCounter+=1
        audioManager(data)
        if data.gamePaused==True:paused(data)
        if data.playerRoundOver==True:gameStatus(data)
        if data.initialize== True: init2(data)
        
        
        for event in pygame.event.get():
            if quitGame(event,data): 
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if data.gameStarted==False:
                    data.menu.update(event,data)
                elif event.key==pygame.K_p:
                    data.gamePaused=True
                elif event.key==pygame.K_w:
                    #data.initialize= True
                    data.gameChannel.pause()
                elif event.key==pygame.K_e:
                    data.gameChannel.unpause()
                
                else:
                    if data.discActive==False:
                        currentTurret=data.turrets[data.playerTurn]    
                        if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                            if data.gameGameMode=="SuperNova":
                                currentTurret.keyPressed(event)                            
                        elif event.key == pygame.K_SPACE:
                            #pygame.mixer.music.play()
                            (position, angle)=currentTurret.getinfo()
                            data.disc= Discs(data,position,angle)
                            data.discActive=True
                            data.playerTurn=(data.playerTurn+1)%data.playerTotal

        screen.blit(data.background, (0,0))
        if data.gameStarted==False:
            data.menu.draw(data)
        else:
            data.displayUI.update(data)
            currentTurret=data.turrets[data.playerTurn]
            otherTurret=data.turrets[(data.playerTurn+1)%data.playerTotal]
            if data.gameGameMode=="SuperNova":
                otherTurret.displayLaser=False
                currentTurret.displayLaser=True
            else:
                otherTurret.rotate=False
                currentTurret.rotate=True
            for turret in data.turrets:
                turret.update(data)
            data.sparkTrail.update(data)
            if data.discActive==True:
                data.disc.update(data)
            data.rings.update(data)
            data.planets.update(data)
            data.sparks.update(data)
            
            

        data.clock.tick(data.fps)
        pygame.display.flip()


    
runOrbitals()
