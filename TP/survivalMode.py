from composer import *
from markovMel import *
import time
import random
pygame.mixer.set_num_channels(3)
pygame.display.set_caption('SURVIVAL MODE')

def loadSound(noteName):
    sound=pygame.mixer.Sound('sounds/'+noteName+'.wav')
    sound.set_volume(.3)
    return sound

def loadImage(file,size=None,colorkey=None):
    image=pygame.image.load(file).convert()
    if size!=None:
        image=pygame.transform.scale(image,size)
    if colorkey!=None:
        image.set_colorkey(colorkey)
    return image

def enemySoundsDict():
    return {
    'enemySound0':None,'enemySound1':None,'enemySound2':None,
    'enemySound3':None,'enemySound4':None,'enemySound5':None,
    'enemySound6':None,'enemySound7':None
    }

def keyboardToNotesDict():
    return {
    'q':[loadSound('c3'),'C3'],'2':[loadSound('csh3'),'Csh3'],
    'w':[loadSound('d3'),'D3'],'3':[loadSound('dsh3'),'Dsh3'],
    'e':[loadSound('e3'),'E3'],'r':[loadSound('f3'),'F3'],
    '5':[loadSound('fsh3'),'Fsh3'],'t':[loadSound('g3'),'G3'],
    '6':[loadSound('gsh3'),'Gsh3'],'y':[loadSound('a3'),'A3'],
    '7':[loadSound('ash3'),'Ash3'],'u':[loadSound('b3'),'B3'],
    'i':[loadSound('c4'),'C4'],'9':[loadSound('csh4'),'Csh4'],
    'o':[loadSound('d4'),'D4'],'0':[loadSound('dsh4'),'Dsh4'],
    'p':[loadSound('e4'),'E4'],'LEFTBRACKET':[loadSound('f4'),'F4'],
    'EQUALS':[loadSound('fsh4'),'Fsh4'],'RIGHTBRACKET':[loadSound('g4'),'G4'],
    'a':[loadSound('gsh4'),'Gsh4'],'z':[loadSound('a4'),'A4'],
    's':[loadSound('ash4'),'Ash4'],'x':[loadSound('b4'),'B4'],
    'c':[loadSound('c5'),'C5'],'f':[loadSound('csh5'),'Csh5'],
    'v':[loadSound('d5'),'D5'],'g':[loadSound('dsh5'),'Dsh5'],
    'b':[loadSound('e5'),'E5'],'n':[loadSound('f5'),'F5'],
    'j':[loadSound('fsh5'),'Fsh5'],'m':[loadSound('g5'),'G5'],
    'k':[loadSound('gsh5'),'Gsh5'],'COMMA':[loadSound('a5'),'A5'],
    'l':[loadSound('ash5'),'Ash5'],'PERIOD':[loadSound('b5'),'B5'],
    'SLASH':[loadSound('c6'),'C6']
    }

def nameToImagesDict():
    white,black,=(255,255,255),(0,0,0)
    ninjaSize=(120,120)
    smallNinjaSize=(50,50)
    return {
    'earthImage':loadImage('images/earth.png',colorkey=white),
    'ninjaImage0':loadImage('images/ninjarun0.png',ninjaSize,white),
    'ninjaImage1':loadImage('images/ninjarun1.png',ninjaSize,white),
    'ninjaImage2':loadImage('images/ninjarun2.png',ninjaSize,white),
    'ninjaImage3':loadImage('images/ninjarun3.png',ninjaSize,white),
    'ninja1Image':loadImage('images/ninja1.png',smallNinjaSize,white),
    'ninja1backImage':loadImage('images/ninja1back.png',ninjaSize,white),
    'ninja2Image':loadImage('images/ninja2.png',smallNinjaSize,white),
    'ninja2backImage':loadImage('images/ninja2back.png',ninjaSize,white),
    'pianoImage':loadImage('images/piano.png',colorkey=white),
    'keyPressed':loadImage('images/keyPressed.png',colorkey=black),
    'keyPressedC':loadImage('images/keyPressedC.png',colorkey=black),
    'keyPressedE':loadImage('images/keyPressedE.png',colorkey=black),
    'keyPressedChr':loadImage('images/keyPressedChr.png',colorkey=black),
    'bambooImage':loadImage('images/bamboo.png',colorkey=white),
    'rock0Image':loadImage('images/rock0.png',colorkey=white),
    'rock1Image':loadImage('images/rock1.png',colorkey=white),
    'rock2Image':loadImage('images/rock2.png',colorkey=white),
    'rock3Image':loadImage('images/rock3.png',colorkey=white),
    'enemy0Image':loadImage('images/enemy0.png',colorkey=white),
    'enemy1Image':loadImage('images/enemy1.png',colorkey=white),
    'enemy2Image':loadImage('images/enemy2.png',colorkey=white),
    'ninjaStarImage':loadImage('images/ninjaStar.png',colorkey=white),
    'startImage':loadImage('images/start.png',colorkey=white),
    'pauseImage':loadImage('images/pause.png',colorkey=white),
    'gameOverImage':loadImage('images/gameOver.png',colorkey=white),
    'quitButtonImage':loadImage('images/quitButton.png',colorkey=white),
    'hpImage':loadImage('images/hp.png',colorkey=white)
    }

class var(object):
    width,height=1100,700
    white,black=(255,255,255),(0,0,0)
    curPlayerImage,trans=1,-1
    objList,ninjaStarList,keysPressed=[],[],[]
    playerInput,playerNotesDur,correctNotes=[],[],[]
    enemiesSeen,enemy,enemyPlaying,enemySize=0,None,False,30
    speed,timeAfterSlomo,paused,dir=35,20000,False,None
    totalEnemies,score=8,0
    enemyNotes,enemyNotesDur,enemyDur=[None]*totalEnemies,\
    [None]*totalEnemies,[None]*totalEnemies
    hitSound=pygame.mixer.Sound('hitSound.wav')
    enemySoundChannel=pygame.mixer.Channel(1)
    enemySounds=enemySoundsDict()
    keyboardToNotes=keyboardToNotesDict()
    nameToImages=nameToImagesDict()
    for i in xrange(totalEnemies):
        mel=writeMel('sounds/enemySound'+str(i)+'.wav')
        enemySounds['enemySound'+str(i)]=mel[0]
        notesTemp,durTemp=[None]*len(mel[1]),[None]*len(mel[1])
        for j in xrange(len(mel[1])):
            notesTemp[j],durTemp[j]=mel[1][j]
        enemyNotes[i],enemyNotesDur[i]=notesTemp,durTemp
        enemyDur[i]=sum(enemyNotesDur[i])

class Player(object):
    def __init__(self):
        self.pos=(540,490)
        self.hp=140

    def draw(self,surface):
        if var.speed==35:
            self.change(surface)
        else:
            if var.time%5<10:
                self.change(surface)

    def change(self,surface):
        var.curPlayerImage+=var.trans
        num=str(var.curPlayerImage)
        pos=(self.pos[0]-55,self.pos[1]-40)
        surface.blit(var.nameToImages['ninjaImage'+num],pos)
        if num=='0' or num=='3':
            var.trans*=(-1)

class Piano(object):
    def __init__(self):
        self.pos=(30,530)

    def draw(self,surface):
        surface.blit(var.nameToImages['pianoImage'],self.pos)

    def findNote(self,event):
        for i in var.keyboardToNotes:
            if event.key==eval('pygame.K_'+i):
                return var.keyboardToNotes[i]

    def keyPressed(self,event):
        if event.key==pygame.K_ESCAPE: pygame.quit()
        if event.key==pygame.K_SPACE and var.speed==35: var.paused=True
        note=self.findNote(event)
        if note!=None:
            noteNm=note[1]
            if var.speed==150:
                self.pressingStart=var.time
            note[0].play()
            var.keysPressed.append(Outline(noteNm))

    def keyReleased(self,event):
        taper=500
        note=self.findNote(event)
        if note!=None:
            noteNm=note[1]
            if var.speed==150:
                try:
                    var.playerInput.append(eval(noteNm))
                    var.playerNotesDur.append(var.time-self.pressingStart)
                except: pass
            pygame.mixer.fadeout(taper)
            for i in var.keysPressed:
                if i.noteNm==noteNm:
                    var.keysPressed.remove(i)

class Outline(object):
    def __init__(self,noteNm):
        self.noteNm=noteNm

    def draw(self,surface):
        noteNm=self.noteNm
        x=30+(notes.index(eval(noteNm))+1)*24
        if noteNm in ['C3','D3','E3','B3']: x-=6
        elif noteNm in ['Dsh3','Ash3']: x-=10
        elif noteNm in ['G4','C5','D5','F5','G5','A5']: x+=6
        elif noteNm in ['Fsh4','Csh5','Fsh5','Gsh5','C6']: x+=10
        y=var.height-145
        if len(noteNm)>2: type='Chr'; x+=20
        elif noteNm[0] in ['C','F']: type='C'
        elif noteNm[0] in ['E','B']: type='E'
        else: type=''
        noteNm='keyPressed'+type
        surface.blit(var.nameToImages[noteNm],(x,y))

class Earth(object):
    def draw(self,surface):
        image=var.nameToImages['earthImage']
        surface.blit(image,(0,0))
        roadColor=(200,200,150)
        roadPoints=((540,68),(560,68),(1000,700),(100,700))
        pygame.draw.polygon(surface,roadColor,roadPoints)

class NinjaStar(object):
    def __init__(self,pos):
        self.pos=pos
        self.angle=0

    def draw(self,surface):
        gap=self.pos[0]-(var.player.pos[0])
        if var.speed==150 and var.enemyPlaying and 490-self.pos[1]<200:
            yDelta=1
        else: yDelta=3
        self.pos=(self.pos[0]-gap/8.0,self.pos[1]+yDelta)
        image=var.nameToImages['ninjaStarImage']
        self.angle-=40
        image=pygame.transform.rotate(image,self.angle)
        x=int(45*(self.pos[1]/float(var.player.pos[1])))
        size=(x,x/2)
        image=pygame.transform.scale(image,size)
        pos=(self.pos[0]-20,self.pos[1])
        surface.blit(image,pos)
        if self.pos[0]<0 or self.pos[0]>var.width or self.pos[1]>var.height:
            var.ninjaStarList.pop(0)
            if var.ninjaStarList==[]: var.player.pos=(540,490)

class Enemy(object):
    def __init__(self,pos):
        var.timeAfterSlomo=0
        var.slomoStartTime=var.time
        taper=500
        pygame.mixer.fadeout(taper)
        var.playerInput,var.playerNotesDur,var.correctNotes=[],[],[]
        var.keysPressed=[]
        sound=var.enemySounds['enemySound'+str(var.enemiesSeen)]
        var.enemySoundChannel.play(sound)
        var.enemyPlaying=True
        var.enemiesSeen+=1
        self.pos,self.size=pos,var.enemySize
        if self.pos[0]>=550: self.image=random.choice(
            (var.nameToImages['enemy0Image'],var.nameToImages['enemy1Image']))
        else: self.image=var.nameToImages['enemy2Image']
        self.spawnTime=var.time
        var.ninjaStarList.append(NinjaStar(self.pos))

    def draw(self,surface):
        xdelta=self.pos[0]-var.width/2
        self.pos=(self.pos[0]+xdelta/200.0,self.pos[1]+.005)
        self.size+=1
        image=pygame.transform.scale(self.image,(self.size,int(self.size*.75)))
        surface.blit(image,self.pos)
        if self.pos[0]<0 or self.pos[0]>var.width or self.pos[1]>var.height:
            var.enemy=None
    
    def throwStar(self):
        if var.time-self.spawnTime>var.enemyNotesDur\
           [var.enemiesSeen-1][len(var.ninjaStarList)-1]-50:
            var.ninjaStarList.append(NinjaStar(self.pos))
            self.spawnTime=var.time

class Obj(object):
    def __init__(self,name,pos,size):
        self.name=name
        self.pos=pos
        self.size=size

    def offset(self,pos):
        if self.name[0]=='r' and len(var.objList)>1:
            proximity=self.pos[0]-var.objList[var.objList.index(self)-1].pos[0]
            if abs(proximity)<15:
                return (self.pos[0]+80*proximity/abs(proximity),self.pos[1])
            else: 
                return pos
        else:
            return pos

    def draw(self,surface):
        xdelta=self.pos[0]-var.width/2
        self.pos=(self.pos[0]+xdelta/200.0,self.pos[1]+.005)
        self.size=self.size+1
        objImage=var.nameToImages[self.name]
        objImage=pygame.transform.scale(objImage,(self.size,self.size))
        pos=self.offset(self.pos)
        surface.blit(objImage,pos)
        for i in var.objList:
            if i.pos[0]<0 or i.pos[0]>var.width or i.pos[1]>var.height-100:
                var.objList.remove(i)

def create():
    num=random.randint(0,500)
    if num in set([0,1,2,3]):
        name='rock'+str(num)+'Image'
    elif num in set([4,5,6,7]):
        name='bambooImage'
    if num in set([0,1,2,3,4,5,6,7]):
        pos=((random.randint(140,430),20),(random.randint(670,983),20))
        pos=pos[random.randint(0,1)]
        pos=(pos[0],pos[1]+abs(var.width/2-pos[0])/7)
        size=random.randint(40,60)
        var.objList.append(Obj(name,pos,size))

def spawn():
    if var.speed==35 and var.timeAfterSlomo>26000 and \
       var.enemiesSeen!=var.totalEnemies and var.ninjaStarList==[]:
        pos=((random.randint(400,430),50),(random.randint(670,700),50))
        pos=random.choice(pos)
        var.enemy=Enemy(pos)

def dodge():
    offset=20
    starList=var.ninjaStarList
    correctList=var.correctNotes
    for i in xrange(len(starList)):
        if abs(starList[i].pos[1]-(var.player.pos[1]+offset))<5:
            try:
                if correctList[i]:
                    pos=(random.randint(510,570),490)
                    var.player.pos=(pos)
            except: pass

def checkCollision():
    lst=var.ninjaStarList
    if (lst!=[] and abs(lst[0].pos[0]-var.player.pos[0])<6 and 
        abs(lst[0].pos[1]-(var.player.pos[1]+30))<6):
        var.hitSound.play()
        var.player.hp-=30
        lst.pop(0)
        return True

def checkScore():
    notes=var.enemyNotes[var.enemiesSeen-1]
    correct=var.correctNotes
    for i in xrange(len(notes)):
        if notes[i]!=var.playerInput[i]:
            correct.append(0)
            var.player.hp-=7
        else:
            accuracy=(1000.0/abs(var.enemyNotesDur[var.enemiesSeen-1][i]-
                      var.playerNotesDur[i]))
            correct.append(accuracy+20)
    var.score+=int(sum(correct))

def playersTurn(surface):
    enemysTurn=var.enemyDur[var.enemiesSeen-1]
    if not var.enemyPlaying:
        var.speed=150
        if var.time-var.slomoStartTime<4000:
            surface.blit(var.nameToImages['startImage'],(0,0))
    finished=len(var.playerInput)>=len(var.enemyNotes[var.enemiesSeen-1])
    if  finished or checkCollision():
        var.speed=35
        var.timeAfterSlomo=20000
        if finished: checkScore()

def drawOutlines(surface):
    for i in var.keysPressed:
        i.draw(surface)

def displayScore(surface):
    color=255-var.bgColor[0]
    font=pygame.font.Font(None,24)
    text=font.render('Score: '+str(var.score),True,(color,color,color))
    textPos=(780,30)
    surface.blit(text,textPos)

def changeBgColor():
    if var.time%70<3:
        if var.dark: var.bgColor=\
        tuple(i+1 if i!=255 else i for i in list(var.bgColor))
        else: var.bgColor=\
        tuple(i-1 if i!=0 else i for i in list(var.bgColor))

def draw(surface):
    quitPos,hpPos,rectPos=(10,10),(860,8),(890,50,(140-var.player.hp),15)
    changeBgColor()
    surface.fill(var.bgColor)
    var.earth.draw(surface)
    for i in var.objList:
        i.draw(surface)
    if var.enemy!=None:
        var.enemy.draw(surface)
    for i in var.ninjaStarList:
        i.draw(surface)
    var.piano.draw(surface)
    var.player.draw(surface)
    surface.blit(var.nameToImages['quitButtonImage'],quitPos)
    surface.blit(var.nameToImages['hpImage'],hpPos)
    pygame.draw.rect(surface,var.bgColor,rectPos)
    displayScore(surface)

def levelWon(surface):
    if var.enemiesSeen==var.totalEnemies and var.enemy==None: pygame.quit()
    if var.player.hp<=0: pause(surface,'gameOver')

def pause(surface,type):
    image=type+'Image'
    image=var.nameToImages[image]
    surface.blit(image,(0,0))
    pygame.display.update()
    while True:
        try:
            event=eventQueue()[0]
            if event.type==pygame.MOUSEBUTTONDOWN: checkQuit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: pygame.quit()
                if event.key==pygame.K_SPACE: break
        except: pass
    if type=='gameOver':
        var.playing=False
        import startScreen
    var.paused=False

def checkQuit():
    mousePos=pygame.mouse.get_pos()
    if (mousePos[0]>25 and mousePos[0]<44
        and mousePos[1]>33 and mousePos[1]<59):
        pygame.quit()

def eventQueue():
    return pygame.event.get()

def play(surface):
    var.earth,var.piano,var.player=Earth(),Piano(),Player()
    clock=pygame.time.Clock()
    time=0
    var.bgColor=random.choice([(0,0,0),(250,150,0),(240,240,240),\
                               (190,240,255)])
    var.dark=(var.bgColor==(0,0,0))
    var.playing=True
    while var.playing:
        tick=clock.tick()
        time+=tick; var.timeAfterSlomo+=tick
        var.time=pygame.time.get_ticks()
        if time>var.speed: draw(surface); create(); spawn(); time=0
        drawOutlines(surface); levelWon(surface)
        pygame.display.update()
        if var.timeAfterSlomo<20000: playersTurn(surface)
        elif var.timeAfterSlomo>=20000 and var.speed==150: var.speed=35
        if (var.enemyPlaying and len(var.ninjaStarList)<
        len(var.enemyNotesDur[var.enemiesSeen-1])): var.enemy.throwStar()
        if var.ninjaStarList!=[] and var.speed==35: dodge()
        for event in eventQueue():
            if var.enemyPlaying==False:
                if event.type==pygame.KEYDOWN: var.piano.keyPressed(event)
                if event.type==pygame.KEYUP: var.piano.keyReleased(event)
                if var.paused: pause(surface,'pause')
            if event.type==pygame.MOUSEBUTTONDOWN: checkQuit()
        if not var.enemySoundChannel.get_busy(): var.enemyPlaying=False
    pygame.quit()