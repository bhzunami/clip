#!/usr/bin/env python3

import logging
import time
import pdb
import random
import math
from pyscipopt import Model, quicksum, Conshdlr, SCIP_RESULT, SCIP_PARAMSETTING, SCIP_HEURTIMING, SCIP_PARAMEMPHASIS
from crosswordsHandler import CrosswordsHdlr
from crossword_heuer import CrosswordHeuerBrutetForce, CrosswordHeuer

from types import SimpleNamespace
import string
#logging.basicConfig(level=logging.INFO)
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "

"""
    P I E R
    I D L E
    N O S E
    S L E D

    C A N
    A G E
    R O W

    M I S L E D
    U M P I R E
    S P I G O T
    C U R A T E
    I R I T I C
    D E T E C T

    C A L L E T
    O P I A T E
    M I M B A R
    P E N I L E 
    O C E L O T
    S E R E N E 
"""

DICTIONARY = ['PIER', 'IDLE', 'NOSE', 'SLED', 'PINS', 'IDOL', 'ELSE', 'REED']
DICTIONARY3 = ['AB', 'AB', 'AA', 'BB']
DICTIONARY2 = ['CAN', 'AGE', 'ROW', 'CAR', 'AGO', 'NEW']
DICTIONARY2 = ['CALLET', 'OPIATE', 'MIMBAR', 'PENILE', 'OCELOT', 'SERENE', 'COMPOS', 'APIECE', 'LIMNER', 'LABILE', 'ETALON', 'TERETE']

DICTIONARY2 = ['ABLE', 'ACID', 'AGED', 'ALSO', 'AREA', 'ARMY', 'AWAY', 'BABY', 'BACK', 'BALL', 'BAND', 'BANK', 'BASE', 'BATH', 'BEAR', 'BEAT', 'BEEN', 'BEER', 'BELL', 'BELT', 'BEST', 'BILL', 'BIRD', 'BLOW', 'BLUE', 'BOAT', 'BODY', 'BOMB', 'BOND', 'BONE', 'BOOK', 'BOOM', 'BORN', 'BOSS', 'BOTH', 'BOWL', 'BULK', 'BURN', 'BUSH', 'BUSY', 'CALL', 'CALM', 'CAME', 'CAMP', 'CARD', 'CARE', 'CASE', 'CASH', 'CAST', 'CELL', 'CHAT', 'CHIP', 'CITY', 'CLUB', 'COAL', 'COAT', 'CODE', 'COLD', 'COME', 'COOK', 'COOL', 'COPE', 'COPY', 'CORE', 'COST', 'CREW', 'CROP', 'DARK', 'DATA', 'DATE', 'DAWN', 'DAYS', 'DEAD', 'DEAL', 'DEAN', 'DEAR', 'DEBT', 'DEEP', 'DENY', 'DESK', 'DIAL', 'DICK', 'DIET', 'DISC', 'DISK', 'DOES', 'DONE', 'DOOR', 'DOSE', 'DOWN', 'DRAW', 'DREW', 'DROP', 'DRUG', 'DUAL', 'DUKE', 'DUST', 'DUTY', 'EACH', 'EARN', 'EASE', 'EAST', 'EASY', 'EDGE', 'ELSE', 'EVEN', 'EVER', 'EVIL', 'EXIT', 'FACE', 'FACT', 'FAIL', 'FAIR', 'FALL', 'FARM', 'FAST', 'FATE', 'FEAR', 'FEED', 'FEEL', 'FEET', 'FELL', 'FELT', 'FILE', 'FILL', 'FILM', 'FIND', 'FINE', 'FIRE', 'FIRM', 'FISH', 'FIVE', 'FLAT', 'FLOW', 'FOOD', 'FOOT', 'FORD', 'FORM', 'FORT', 'FOUR', 'FREE', 'FROM', 'FUEL', 'FULL', 'FUND', 'GAIN', 'GAME', 'GATE', 'GAVE', 'GEAR', 'GENE', 'GIFT', 'GIRL', 'GIVE', 'GLAD', 'GOAL', 'GOES', 'GOLD', 'GOLF', 'GONE', 'GOOD', 'GRAY', 'GREW', 'GREY', 'GROW', 'GULF', 'HAIR', 'HALF', 'HALL', 'HAND', 'HANG', 'HARD', 'HARM', 'HATE', 'HAVE', 'HEAD', 'HEAR', 'HEAT', 'HELD', 'HELL', 'HELP', 'HERE', 'HERO', 'HIGH', 'HILL', 'HIRE', 'HOLD', 'HOLE', 'HOLY', 'HOME', 'HOPE', 'HOST', 'HOUR', 'HUGE', 'HUNG', 'HUNT', 'HURT', 'IDEA', 'INCH', 'INTO', 'IRON', 'ITEM', 'JACK', 'JANE', 'JEAN', 'JOHN', 'JOIN', 'JUMP', 'JURY', 'JUST', 'KEEN', 'KEEP', 'KENT', 'KEPT', 'KICK', 'KILL', 'KIND', 'KING', 'KNEE', 'KNEW', 'KNOW', 'LACK', 'LADY', 'LAID', 'LAKE', 'LAND', 'LANE', 'LAST', 'LATE', 'LEAD', 'LEFT', 'LESS', 'LIFE', 'LIFT', 'LIKE', 'LINE', 'LINK', 'LIST', 'LIVE', 'LOAD', 'LOAN', 'LOCK', 'LOGO', 'LONG', 'LOOK', 'LORD', 'LOSE', 'LOSS', 'LOST', 'LOVE', 'LUCK', 'MADE', 'MAIL', 'MAIN', 'MAKE', 'MALE', 'MANY', 'MARK', 'MASS', 'MATT', 'MEAL', 'MEAN', 'MEAT', 'MEET', 'MENU', 'MERE', 'MIKE', 'MILE', 'MILK', 'MILL', 'MIND', 'MINE', 'MISS', 'MODE', 'MOOD', 'MOON', 'MORE', 'MOST', 'MOVE', 'MUCH', 'MUST', 'NAME', 'NAVY', 'NEAR', 'NECK', 'NEED', 'NEWS', 'NEXT', 'NICE', 'NICK', 'NINE', 'NONE', 'NOSE', 'NOTE', 'OKAY', 'ONCE', 'ONLY', 'ONTO', 'OPEN', 'ORAL', 'OVER', 'PACE', 'PACK', 'PAGE', 'PAID', 'PAIN', 'PAIR', 'PALM', 'PARK', 'PART', 'PASS', 'PAST', 'PATH', 'PEAK', 'PICK', 'PINK', 'PIPE', 'PLAN', 'PLAY', 'PLOT', 'PLUG', 'PLUS', 'POLL', 'POOL', 'POOR', 'PORT', 'POST', 'PULL', 'PURE', 'PUSH', 'RACE', 'RAIL', 'RAIN', 'RANK', 'RARE', 'RATE', 'READ', 'REAL', 'REAR', 'RELY', 'RENT', 'REST', 'RICE', 'RICH', 'RIDE', 'RING', 'RISE', 'RISK', 'ROAD', 'ROCK', 'ROLE', 'ROLL', 'ROOF', 'ROOM', 'ROOT', 'ROSE', 'RULE', 'RUSH', 'RUTH', 'SAFE', 'SAID', 'SAKE', 'SALE', 'SALT', 'SAME', 'SAND', 'SAVE', 'SEAT', 'SEED', 'SEEK', 'SEEM', 'SEEN', 'SELF', 'SELL', 'SEND', 'SENT', 'SEPT', 'SHIP', 'SHOP', 'SHOT', 'SHOW', 'SHUT', 'SICK', 'SIDE', 'SIGN', 'SITE', 'SIZE', 'SKIN', 'SLIP', 'SLOW', 'SNOW', 'SOFT', 'SOIL', 'SOLD', 'SOLE', 'SOME', 'SONG', 'SOON', 'SORT', 'SOUL', 'SPOT', 'STAR', 'STAY', 'STEP', 'STOP', 'SUCH', 'SUIT', 'SURE', 'TAKE', 'TALE', 'TALK', 'TALL', 'TANK', 'TAPE', 'TASK', 'TEAM', 'TECH', 'TELL', 'TEND', 'TERM', 'TEST', 'TEXT', 'THAN', 'THAT', 'THEM', 'THEN', 'THEY', 'THIN', 'THIS', 'THUS', 'TILL', 'TIME', 'TINY', 'TOLD', 'TOLL', 'TONE', 'TONY', 'TOOK', 'TOOL', 'TOUR', 'TOWN', 'TREE', 'TRIP', 'TRUE', 'TUNE', 'TURN', 'TWIN', 'TYPE', 'UNIT', 'UPON', 'USED', 'USER', 'VARY', 'VAST', 'VERY', 'VICE', 'VIEW', 'VOTE', 'WAGE', 'WAIT', 'WAKE', 'WALK', 'WALL', 'WANT', 'WARD', 'WARM', 'WASH', 'WAVE', 'WAYS', 'WEAK', 'WEAR', 'WEEK', 'WELL', 'WENT', 'WERE', 'WEST', 'WHAT', 'WHEN', 'WHOM', 'WIDE', 'WIFE', 'WILD', 'WILL', 'WIND', 'WINE', 'WING', 'WIRE', 'WISE', 'WISH', 'WITH', 'WOOD', 'WORD', 'WORE', 'WORK', 'YARD', 'YEAH', 'YEAR', 'YOUR', 'ZERO', 'ZONE']

DICTIONARY2 = ['BRAUSE', 'RASA', 'ANONYM', 'UHUS', 'SALATE',
              'DEN', 'LOS', 'BREZEL', 'ECK', 'NATION', 'ANHAND',
              'SOUL', 'ANSAGE', 'ALBEN', 'ORCA', 'INSEKT', 'DIEB',
              'REGATTA', 'BOLERO', 'RAMPE', 'MALEN', 'OFEN',
              'EIGELB', 'ALBEREI', 'EAN', 'SULTAN', 'AKTE', 'RATE',
              'ETAT', 'SPAT', 'APFEL', 'EIBE', 'PANGEA', 'ERN',
              'SOLE', 'BIS', 'LATERAL', 'TAKT', 'TEEN', 'OMA',
              'GAGA', 'SET', 'NON', 'RAPS', 'ASBEST', 'UHRWERK',
              'ADELIGER', 'MAGD', 'GR', 'DE', 'FLAU', 'OFT', 'UMTUN',
              'MIES', 'ROH', 'SEMINAR', 'FASELEI', 'EGO']

"""
T U N
A   U
T O T

T A T
U   O
N U T

B A
C
"""

DICTIONARY2 = ['TUN', 'NUT', 'TAT', 'TOT']
DICTIONARY2 = ['BA', 'BC']


def getWords():
    num_words = []
    count = {}
    for word in DICTIONARY:
        num_word = []
        for l in word:
            num = ALPHABET.index(l)
            num_word.append(num)
            if num in count.keys():
                count[num] = count[num] + 1
            else:
               count[num] = 1 
        num_words.append(num_word)
    return num_words, count

def solve(row=10, col=10):
    model = Model("Crossword")
    s = {}

    words, words_count = getWords()

    lb_global = min(words_count.keys())
    ub_global = max(words_count.keys())
    print(lb_global, ub_global)
    # Variabeln für die einzelnen stimmen pro quadrat definieren
    for x in range(row):
        for y in range(col):
            for l in range(0, len(ALPHABET)):
                s[x, y, l] = model.addVar(vtype="B", name="{}-{}-{}".format(x, y, l))
            #s[x, y] = model.addVar(vtype="I", lb=lb_global, ub=ub_global, name="{}-{}".format(x, y))

    #pdb.set_trace()    
    # Nur 1 Buchstaben pro Feld
    for x in range(row):
        for y in range(col):
            model.addCons(quicksum(s[x, y, l] for l in range(0, len(ALPHABET))) == 1)

    # Jeder Buchstaben muss mind 1 vorhanden ist
    # for l in words_count.keys():
    #     model.addCons(quicksum(s[x, y, l]  for x in range(col) for y in range(row)) >= 1)

    # Buchstabe x darf nicht mehr vorkommen als gezählt
    # for i, c in words_count.items():
    #     model.addCons(quicksum(s[x, y, i]  for x in range(col) for y in range(row)) <= c)

    # CONSTRAINTS
    # - - - - - - - - - - - - - - - - - -

    # for x in range(row):
    #     for y in range(col):
    #         model.addCons(s[x, y, l] for l in range(26)) == 1)  # Nur ein Buchstaben

    conshdlr = CrosswordsHdlr(DICTIONARY, 0, len(ALPHABET), row=row, col=col, logger=logger)
    random.shuffle(DICTIONARY)
    heuristic = CrosswordHeuerBrutetForce(DICTIONARY, row, logger=logger)
    #heuristic = CrosswordHeuer(DICTIONARY, row, col, lb_global, ub_global, logger=logger)
    #                 heur,        name,       desc,         dispatcher, priority, freq)
    # HEUER
    # model.includeHeur(heuristic, "PyHeur", "custom heuristic implemented in python", "Y",
    #                   timingmask=SCIP_HEURTIMING.BEFORENODE)

    model.includeConshdlr(conshdlr, "crossword",
                          "Crossword", chckpriority=-10, maxprerounds=1,
                          enfopriority=-10, propfreq=10)
    
    model.setObjective(quicksum(s[x, y, 26] for x in range(col) for y in range(row)), "minimize")

    # Add horizontal 
    vars = []
    for x in range(row):
        for y in range(col):
            for l in range(0, len(ALPHABET)):
                var = s[x, y, l]
                vars.append(var)
                #vals = set(range(int(round(var.getLbLocal())), int(round(var.getUbLocal())) + 1))
                #domains[var.ptr()] = vals
    cons = model.createCons(conshdlr, "crossword")
    cons.data = SimpleNamespace() 
    cons.data.vars = vars
    #cons.data.domains = domains
    model.addPyCons(cons)

    # http://scip.zib.de/doc/html/group__ParameterMethods.php#gab2bc4ccd8d9797f1e1b2d7aaefa6500e
    #model.setEmphasis(SCIP_PARAMEMPHASIS.CPSOLVER) # No LP Relaxtion
    #model.setPresolve(SCIP_PARAMSETTING.OFF)  # Turn off presolver
    model.setBoolParam("misc/allowdualreds", False)
    #model.hideOutput()
    model.optimize()

    if model.getStatus() != 'optimal':
        print('No solution found! {}'.format(model.getStatus()))
        return False

    print("Solution found")

    for x in range(row):
        out = ''
        for y in range(col):
            for l in range(0, len(ALPHABET)):
                #letter = 1
                if model.getVal(s[x, y, l]) >= 0.2:
                    letter = l
            out += "{:2} | ".format(ALPHABET[int(letter)])
        print(out)

    del model # consfree get called
    return True


def main():
    count = 4
    solve(row=count, col=count)

if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    # create a file handler
    handler = logging.FileHandler('/tmp/election.log', mode='w')
    handler.setLevel(logging.DEBUG)

    # create a logging format
    formatter = logging.Formatter('%(name)s: [%(levelname)s] - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)
    logger.info("Start Problem")
    main()
