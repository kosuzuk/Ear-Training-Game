import pygame
import sys
pygame.mixer.init()
pygame.init()
pygame.display.set_caption('TONED NINJA1!!')

def loadImage(file,colorkey=None):
    pygame.display.set_mode((1100,700))
    image=pygame.image.load(file).convert()
    if colorkey!=None:
        image.set_colorkey(colorkey)
    if file=='images/ninjaStarBackground.png':
        image.set_alpha(110)
    return image

class images(object):
    white=(255,255,255)
    bckgrnd=loadImage('images/ninjaBackground.png')
    ninjaStarBckgrnd=loadImage('images/ninjaStarBackground.png',white)
    signs=loadImage('images/signs.png',white)
    words=loadImage('images/words.png',white)
    quitSign=loadImage('images/quitSign.png',white)
    quitButton=loadImage('images/quitButton.png',white)
    imagesList=[bckgrnd,ninjaStarBckgrnd,signs,words,quitSign,quitButton]
    posList=[(0,0),(0,0),(0,0),(300,300),(10,10),(20,10)]

def drawStartScreen(surface):
    for i in xrange(len(images.imagesList)):
        surface.blit(images.imagesList[i],images.posList[i])
    pygame.display.update()

def playMusic(nxt,reversedTune):
    if nxt=='A': reversedTune=not reversedTune
    musicDict={'A':'B','B':'C','C':'D','D':'S','S':'A'}
    while pygame.mixer.music.get_busy()==0:
        path='sounds/greensleeves'+nxt+'.wav'
        if reversedTune: path=path[:19]+nxt+'rev.wav'
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(0)
        nxt=musicDict[nxt]
    return (nxt,reversedTune)

def loadingScreen(surface):
    loadingImage=pygame.image.load('images/loading.png')
    loadingDotImage=pygame.image.load('images/loadingDot.png')
    loadingDotImage.set_colorkey((255,255,255))
    surface.blit(loadingImage,(0,0))
    surface.blit(loadingDotImage,(960,642))

def setUp(surface):
    taper=600
    pygame.mixer.music.fadeout(taper)
    loadingScreen(surface)
    pygame.display.update()
    if 'survivalMode' in sys.modules:
        del(sys.modules['survivalMode'])
    if 'vsMode' in sys.modules:
        del(sys.modules['vslMode'])


def checkMousePress(event,surface):
    if event.type==pygame.KEYDOWN:
        if event.key==pygame.K_ESCAPE: return True
    if event.type==pygame.MOUSEBUTTONDOWN:
        mousePos=pygame.mouse.get_pos()
        if (mousePos[0]>405 and mousePos[0]<665
            and mousePos[1]>296 and mousePos[1]<366):
            setUp(surface)
            import survivalMode; survivalMode.play(surface)
        elif (mousePos[0]>405 and mousePos[0]<665
            and mousePos[1]>502 and mousePos[1]<575):
            setUp(surface)
            import vsMode; vsMode.play(surface)
        elif (mousePos[0]>35 and mousePos[0]<54
            and mousePos[1]>33 and mousePos[1]<59):
            return True

def start():
    canvasSize=(1100,700)
    surface=pygame.display.set_mode(canvasSize)
    drawStartScreen(surface)
    playing=True
    nxt='A'; reversedTune=False
    while playing:
        nxt,reversedTune=playMusic(nxt,reversedTune)
        for event in pygame.event.get():
            if checkMousePress(event,surface): 
                playing=False
    pygame.quit()

start()
