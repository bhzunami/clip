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

"""
    P I E R
    I D L E
    N O S E
    S L E D

    A B
    A B

    C A N
    A G E
    R O W

    M I S L E D
    U M P I R E
    S P I G O T
    C Z R A T E
    I R I T I C
    D E T E C T
"""

DICTIONARY = ['PIER', 'IDLE', 'NOSE', 'SLED', 'PINS', 'IDOL', 'ELSE', 'REED']
DICTIONARY2 = ['AB', 'AB', 'AA', 'BB']
DICTIONARY2 = ['CAN', 'AGE', 'ROW', 'CAR', 'AGO', 'NEW']
DICTIONARY3 = ['MISLED', 'UMPIRE', 'SPIGOT', 'CURATE', 'IRITIC', 'DETECT', 'MUSCID', 'IMPURE', 'SPIRIT', 'LIGATE', 'EROTIC', 'DETECT']

def getWords():
    num_words = []
    count = {}
    for word in DICTIONARY:
        num_word = []
        for l in word:
            num = string.ascii_uppercase.index(l)
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
            for l in range(lb_global, ub_global+1):
                s[x, y, l] = model.addVar(vtype="B", name="{}-{}-{}".format(x, y, l))
            #s[x, y] = model.addVar(vtype="I", lb=lb_global, ub=ub_global, name="{}-{}".format(x, y))

    #pdb.set_trace()    
    # Nur 1 Buchstaben pro Feld
    for x in range(row):
        for y in range(col):
            model.addCons(quicksum(s[x, y, l] for l in range(lb_global, ub_global+1)) == 1)

    # Jeder Buchstaben muss mind 1 vorhanden ist
    for l in words_count.keys():
        model.addCons(quicksum(s[x, y, l]  for x in range(col) for y in range(row)) >= 1)

    # Buchstabe x darf nicht mehr vorkommen als gezählt
    for i, c in words_count.items():
        model.addCons(quicksum(s[x, y, i]  for x in range(col) for y in range(row)) <= c)

    # CONSTRAINTS
    # - - - - - - - - - - - - - - - - - -

    # for x in range(row):
    #     for y in range(col):
    #         model.addCons(s[x, y, l] for l in range(26)) == 1)  # Nur ein Buchstaben

    conshdlr = CrosswordsHdlr(DICTIONARY, lb_global, ub_global, row=row, col=col, logger=logger)
    random.shuffle(DICTIONARY)
    heuristic = CrosswordHeuerBrutetForce(DICTIONARY, row, logger=logger)
    #heuristic = CrosswordHeuer(DICTIONARY, row, col, lb_global, ub_global, logger=logger)
    #                 heur,        name,       desc,         dispatcher, priority, freq)
    # HEUER
    model.includeHeur(heuristic, "PyHeur", "custom heuristic implemented in python", "Y",
                      timingmask=SCIP_HEURTIMING.BEFORENODE)

    model.includeConshdlr(conshdlr, "crossword",
                          "Crossword", chckpriority=-10,
                          enfopriority = -10, propfreq=20)
    

    # Add horizontal 
    vars = []
    for x in range(row):
        for y in range(col):
            for l in range(lb_global, ub_global+1):
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
    model.setPresolve(SCIP_PARAMSETTING.OFF)  # Turn off presolver
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
            for l in range(lb_global, ub_global+1):
                #letter = 1
                if model.getVal(s[x, y, l]) >= 0.2:
                    letter = l
            out += "{:2} | ".format(string.ascii_uppercase[int(letter)])
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
