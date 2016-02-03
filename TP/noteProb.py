import random

def doProb():
    num=random.randint(1,100)
    if num<11: return 'do'
    elif num<31: return 're'
    elif num<38: return 'resh'
    elif num<50: return 'mi'
    elif num<58: return 'fa'
    elif num<64: return 'fash'
    elif num<76: return 'sol'
    elif num<79: return 'solsh'
    elif num<90: return 'la'
    else: return 'si'

def doshProb():
    num=random.randint(1,100)
    if num<61: return 'do'
    else: return 're'

def reProb():
    num=random.randint(1,100)
    if num<31: return 'do'
    elif num<41: return 'dosh'
    elif num<51: return 'resh'
    elif num<61: return 'mi'
    elif num<71: return 'fa'
    elif num<81: return 'sol'
    elif num<91: return 'la'
    else: return 'si'

def reshProb():
    num=random.randint(1,100)
    if num<51: return 're'
    else: return 'mi'

def miProb():
    num=random.randint(1,100)
    if num<13: return 'do'
    elif num<33: return 're'
    elif num<38: return 'resh'
    elif num<45: return 'mi'
    elif num<70: return 'fa'
    elif num<85: return 'sol'
    elif num<96: return 'la'
    else: return 'si'


def faProb():
    num=random.randint(1,100)
    if num<11: return 'do'
    elif num<26: return 're'
    elif num<56: return 'mi'
    elif num<66: return 'fash'
    elif num<81: return 'sol'
    elif num<98: return 'la'
    else: return 'si'


def fashProb():
    num=random.randint(1,100)
    if num<51: return 'fa'
    else: return 'sol'


def solProb():
    num=random.randint(1,100)
    if num<23: return 'do'
    elif num<28: return 're'
    elif num<40: return 'mi'
    elif num<54: return 'fa'
    elif num<62: return 'fash'
    elif num<70: return 'sol'
    elif num<74: return 'solsh'
    elif num<85: return 'la'
    else: return 'si'


def solshProb():
    num=random.randint(1,100)
    if num<51: return 'sol'
    else: return 'la'


def laProb():
    num=random.randint(1,100)
    if num<21: return 'do'
    elif num<26: return 're'
    elif num<34: return 'mi'
    elif num<39: return 'fa'
    elif num<40: return 'fash'
    elif num<66: return 'sol'
    elif num<74: return 'solsh'
    elif num<80: return 'la'
    elif num<85: return 'lash'
    else: return 'si'


def lashProb():
    num=random.randint(1,100)
    if num<31: return 'la'
    else: return 'si'


def siProb():
    num=random.randint(1,100)
    if num<51: return 'do'
    elif num<64: return 're'
    elif num<68: return 'mi'
    elif num<71: return 'fa'
    elif num<84: return 'sol'
    elif num<97: return 'la'
    else: return 'lash'

