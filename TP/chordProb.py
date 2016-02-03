import random

def oneProb():
    num=random.randint(1,100)
    if num<21: return 'two'
    elif num<22: return 'three'
    elif num<47: return 'four'
    elif num<68: return 'five'
    elif num<83: return 'fsev'
    elif num<86: return 'six'
    elif num<90: return 'seven'
    elif num<96: return 'fof'
    else: return 'nea'

def twoProb():
    num=random.randint(1,100)
    if num<11: return 'one'
    elif num<18: return 'cadsf'
    elif num<51: return 'five'
    elif num<78: return 'fsev'
    elif num<81: return 'six'
    elif num<91: return 'seven'
    else: return 'fof'

def threeProb():
    num=random.randint(1,100)
    if num<31: return 'four'
    elif num<51: return 'fsev'
    elif num<81: return 'five'
    else: return 'nea'

def fourProb():
    num=random.randint(1,100)
    if num<21: return 'one'
    elif num<36: return 'cadsf'
    elif num<46: return 'two'
    elif num<61: return 'fsev'
    elif num<91: return 'five'
    elif num<96: return 'six'
    else: return 'seven'

def fiveProb():
    num=random.randint(1,100)
    if num<85: return 'one'
    elif num<90: return 'three'
    else: return 'six'

def sixProb():
    num=random.randint(1,100)
    if num<21: return 'two'
    elif num<51: return 'four'
    elif num<61: return 'fsev'
    elif num<91: return 'five'
    elif num<96: return 'seven'
    else: return 'nea'

def sevenProb():
    num=random.randint(1,100)
    if num<51: return 'one'
    elif num<71: return 'fsev'
    else: return 'six'

def fsevProb():
    num=random.randint(1,100)
    if num<71: return 'one'
    else: return 'six'

def cadsfProb():
    return 'five'

def fofProb():
    return random.choice(['five','fsev'])

def neaProb():
    return random.choice(['five','fsev'])
