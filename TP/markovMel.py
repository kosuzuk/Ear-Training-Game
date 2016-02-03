import pygame
from composer import * 
from markovProgression import *
from noteProb import *
import random

#note name will be a string of solfege name mapping to an index in one of
#the values in chordsDict so that transposing will be done automatically for 
#notes, when chords are transposed.
notesDict={
'do':chordsDict['one'][0],'dosh':chordsDict['nea'][2],
're':chordsDict['two'][0],'resh':chordsDict['two'][0]+1,
'mi':chordsDict['three'][0],'fa':chordsDict['four'][0],
'fash': chordsDict['fof'][1],'sol':chordsDict['five'][0],
'solsh':chordsDict['nea'][1],'la':chordsDict['six'][0],
'lash':chordsDict['six'][0]+1,'si':chordsDict['seven'][0]
}

def noteInChord(note,chord):
    note=note%12
    chord=[i%12 for i in chord]
    return note in chord

def stepAfterLeap(note,result): #if there is a big leap between notes,make sure 
    returnThis=False #the next note steps in the other direction
    try:
        interval=result[len(result)-2][0]-result[len(result)-1][0]
        if abs(interval)>4:
            if interval>0:
                if 0<note-result[len(result)-1][0]<5: returnThis=True
            else:
                if 0<result[len(result)-1][0]-note<5: returnThis=True
    except: returnThis=True
    return returnThis

def isRepetitive(note,result):
    notRepetitive=True
    try: #do this if chordProg is long enough
        if result[len(result)-3][0]==result[len(result)-1][0]:
            if note==result[len(result)-2][0]:
                notRepetitive=False
    except:
        pass
    return notRepetitive

def isLegal(note,result):
    return (stepAfterLeap(note,result) and (not isRepetitive(note,result)))

def checkOctave(nextNote,note):
    interval=note-nextNote
    if abs(interval)>6:
        num=random.randint(0,4)
        if abs(interval)<10 and num==0: pass
        elif (interval>0 and 
            interval>abs(note-(nextNote+12))):
            nextNote+=12
        elif (interval<0 and 
            abs(interval)>abs(note-(nextNote-12))):
            nextNote-=12
    return nextNote

def getNextNote(note,solf,chord,isChordTone,result,loopCount=0):
    nextSolf=eval(solf+'Prob()')
    nextNote=notesDict[nextSolf]
    nextNote=checkOctave(nextNote,note)
    if isChordTone!=noteInChord(nextNote,chord) or \
       not isLegal(nextNote,result):
        if loopCount>10: isChordTone=not isChordTone
        if loopCount>20: return (nextNote,nextSolf)
        return getNextNote(note,solf,chord,isChordTone,result,loopCount+1)
    return (nextNote,nextSolf)

def checkLastNote(solf,dur,result):
    if solf[-2:]=='sh':
        result.append((notesDict[eval(solf+'Prob()')],dur))
        return result
    elif solf=='fa':
        result.append((notesDict[random.choice(['mi','sol'])],dur))
        return result
    elif solf=='si':
        result.append((notesDict[random.choice(['do','do','sol','la'])],dur))
        return result
    else: return result

def bringDownOct(result):
    temp=[None]*len(result)
    while True:
        for i in xrange(len(result)):
            if result[i][0]<17: return result
            temp[i]=[result[i][0]-12,result[i][1]]
        result=temp

def generateMel(chordProg=None,timeLeft=2400,note=None,solf=None,result=None):
    dur=random.choice([e,q,q,dq,h])
    if timeLeft<10: return bringDownOct(checkLastNote(solf,dur,result))
    isChordTone=True if dur!=e else False
    if chordProg==None:
        numChords=(timeLeft+dur)/600
        chordProg=generateProg(numChords)
        chordProg=inversion(chordProg)
    if note==None:#first note of melody
        solf=random.choice(['do','re','mi','fa','sol','la','si'])
        note=notesDict[solf]#solf is name of note in solfege
        loopCount=0
        while isChordTone!=noteInChord(note,chordProg[0:3]):
            loopCount+=1
            if loopCount>10: isChordTone=not isChordTone
            if loopCount>20: break
            solf=random.choice(['do','re','mi','fa','sol','la','si'])
            note=notesDict[solf]
        result.append((note,dur))
        return generateMel(chordProg,timeLeft-dur,note,solf,result)
    curPos=int(timeLeft/q)*3
    note,solf=\
    getNextNote(note,solf,chordProg[curPos:curPos+3],isChordTone,result)
    result.append((note,dur))
    return generateMel(chordProg,timeLeft-dur,note,solf,result)

def generateMelWrapper():
    return generateMel(result=[])

def writeMel(filename):
    mel=generateMelWrapper()
    mel=[[notes[i[0]],i[1]] for i in mel]
    write_tune(mel,filename)
    melObj=pygame.mixer.Sound(filename)
    return (melObj,mel)

