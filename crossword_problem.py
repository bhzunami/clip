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
from dictionary import DICTIONARY, ALPHABET
#logging.basicConfig(level=logging.INFO)
#ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "

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
    # Variabeln für die einzelnen stimmen pro quadrat definieren
    for x in range(row):
        for y in range(col):
            for l in range(0, len(ALPHABET)):
                s[x, y, l] = model.addVar(vtype="B", name="{}-{}-{}".format(x, y, l))

    # Nur 1 Buchstaben pro Feld
    for x in range(row):
        for y in range(col):
            model.addCons(quicksum(s[x, y, l] for l in range(0, len(ALPHABET))) == 1)

    # CONSTRAINTS
    # - - - - - - - - - - - - - - - - - -
    conshdlr = CrosswordsHdlr(DICTIONARY, row=row, col=col, logger=logger)
    random.shuffle(DICTIONARY)
    heuristic = CrosswordHeuerBrutetForce(DICTIONARY, row, logger=logger)
    #heuristic = CrosswordHeuer(DICTIONARY, row, col, lb_global, ub_global, logger=logger)
    #                 heur,        name,       desc,         dispatcher, priority, freq)
    # HEUER
    # model.includeHeur(heuristic, "PyHeur", "custom heuristic implemented in python", "Y",
    #                   timingmask=SCIP_HEURTIMING.BEFORENODE)

    model.includeConshdlr(conshdlr, "crossword",
                          "Crossword", chckpriority=-10, maxprerounds=1,
                          enfopriority=-10, propfreq=1)

    #model.addCons(quicksum(s[x, y, 26] for x in range(col) for y in range(row)) == 8)
    model.setObjective(quicksum(s[x, y, 26] for x in range(col) for y in range(row)), "minimize")

    # Add horizontal
    vars = {}
    for x in range(row):
        for y in range(col):
            for l in range(0, len(ALPHABET)):
                vars[x, y, l] = s[x, y, l]
    cons = model.createCons(conshdlr, "crossword")
    cons.data = SimpleNamespace()
    cons.data.vars = vars
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
            for l in range(0, len(ALPHABET)):
                #letter = 1
                if model.getVal(s[x, y, l]) >= 0.2:
                    letter = l
            out += "{:2} | ".format(ALPHABET[int(letter)])
        print(out)

    del model # consfree get called
    return True


def main():
    count = 6
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
