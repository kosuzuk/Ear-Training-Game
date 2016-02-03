from composer import *
from chordProb import *
import random
import pygame

pygame.mixer.init()

####chord structure generator####

#dict of chord types. Numbers represent notes in chord.
#numbers are indeces of the notes list in composer.py
chordsDict={
'one':[12,16,19],'two':[14,17,21],'three':[16,19,23],
'four':[17,21,24],'five':[19,23,26],'six':[21,24,28],'seven':[11,14,17],
'fsev':[19,23,29],'cadsf':[19,24,28],'fof':[14,18,21],'nea':[17,20,25]
}

chosenKey='c'

keys=['c','cs','d','ds','e','f','fs','g','gs','a','as','b']

if chosenKey!='c':
    for chord in chordsDict:
        for i in xrange (len(chordsDict[chord])):
            chordsDict[chord][i]+=keys.index(chosenKey)

def getNextChord(PrevChord):
    return eval(PrevChord+'Prob()')

def isLegal(chordProg,nextChord,current,max):#will allow I,V,I but not I,V,I,V
    notRepetitive=okLastChord=None
    try: #do this if chordProg is long enough
        if chordProg[len(chordProg)-3]==chordProg[len(chordProg)-1]:
            if nextChord==chordProg[len(chordProg)-2]:
                notRepetitive=False
    except:
        pass
    if notRepetitive==None: notRepetitive=True
    if current+2==max: #last chord must be I V or vi
        if nextChord not in ['one','five','six']:
            okLastChord=False
    if okLastChord==None: okLastChord=True
    return (notRepetitive and okLastChord)

def getChordProg(chordProg,current,max,depth=0): #give it a chord progression,
    if current+1==max:                   #what number of chord you are on,
        return chordProg                 #and number of chords you want
    else:
        nextChord=getNextChord(chordProg[current])
        if isLegal(chordProg,nextChord,current,max) or depth==20:
            chordProg.append(nextChord)
            return getChordProg(chordProg,current+1,max,depth+1)
        else:
            return getChordProg(chordProg,current,max,depth+1)

def generateProg(numChords=4):
    startChord=random.choice(['one','one','two','four','five','six','fof'])
    chordProg=getChordProg([startChord],0,numChords)
    return chordProg

def getBassRoute(lst,dontInvertThese):
    route=[]
    incr=3
    for i in xrange(0,len(lst)-3,3):
        if i in dontInvertThese: route.append(0) #don't invert Neapolitan sixth 
        else:                                    #or Cadential six-four chords
            root=lst[i+incr]-lst[0]
            third=lst[i+incr+1]-lst[0]
            fifth=lst[i+incr+2]-lst[0]
            chordLst=[root,third,fifth]
            route.append(chordLst.index(min(chordLst[::-1])))
    return route

def invert(chord,inv):
    if inv==1:
        chord[0],chord[1],chord[2]=chord[1],chord[2],chord[0]
        chord[2]+=12
    if inv==2:
        chord[0],chord[1],chord[2]=chord[2],chord[0],chord[1]
        chord[0]-=12
    return chord

def transposeNotes(lst):
    for i in xrange(len(lst)):
        lst[i]+=keys.index(chosenKey)

def getNewNote(firstBass,note):
    totalNotes,middle=12,6
    newNote=note%totalNotes-firstBass
    while newNote<0: newNote+=totalNotes
    if newNote>6: newNote=newNote-2*(newNote-middle)
    return newNote

def dontInvertThis(chordProg,chord):
    if chordProg[chord]=='cadsf' or chordProg[chord]=='nea':
        return True
    if chordProg[chord-1]=='cadsf' and chordProg[chord]=='five':
        return True
    if chord==len(chordProg)-1:
        if (chordProg[chord-1]=='five' and chordProg[chord]=='one') or\
           (chordProg[chord-1]=='one' and chordProg[chord]=='five'):
            return True

def inversion(chordProg): #create chord inversions so the bass moves smoother
    temp,result=[],[]
    dontInvertThese=[]
    firstBass=chordsDict[chordProg[0]][0]
    for chord in xrange(len(chordProg)):
        if chord!=0 and dontInvertThis(chordProg,chord): 
            dontInvertThese.append(chord)
        for note in chordsDict[chordProg[chord]]:
            if chord in dontInvertThese: 
                firstBass=chordsDict[chordProg[chord]][0]
            newNote=getNewNote(firstBass,note)
            temp.append(newNote); result.append(note)
    dontInvertThese=[i-1*3 for i in dontInvertThese]
    route=getBassRoute(temp,dontInvertThese)
    for chord in xrange(3,len(result),3):
        result[chord:chord+3]=invert(result[chord:chord+3],route[chord/3-1])
        if abs(result[chord-3]-result[chord])>6: 
            if result[chord-3]<result[chord]:
                for note in xrange(3): result[chord+note]-=12
            else:
                for note in xrange(3): result[chord-3+note]-=12
    #transposeNotes(result)
    return result

def writeProg(filename): #makes a chord progression, inverts chords, saves it
    result=[]
    prog=generateProg()
    print prog
    N=inversion(prog)
    for note in N:
        result.append([notes[note],q])
    '''for chord in prog: #if easier stage, don't invert chords
        for note in chordsDict[chord]:
            result.append([notes[note],q])'''
    write_tune(result,filename)
    s= pygame.mixer.Sound(filename)
    s.play()





