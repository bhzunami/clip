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
    w_h = {}
    w_v = {}
    r_ = {}
    c_ = {}

    words, words_count = getWords()

    lb_global = min(words_count.keys())
    ub_global = max(words_count.keys())
    print(lb_global, ub_global)
    # Variabeln für die einzelnen stimmen pro quadrat definieren
    for x in range(row):
        for y in range(col):
            for l in range(0, len(ALPHABET)):
                s[x, y, l] = model.addVar(vtype="B", name="{}-{}-{}".format(x, y, l))

    # ROW
    for r in range(row):
        for i, words in enumerate(DICTIONARY):
            w_h[r, i] = model.addVar(vtype="B", name="word-{}-{}".format(r, i))
            w_v[r, i] = model.addVar(vtype="B", name="word-{}-{}".format(r, i))
        r_[r] = model.addVar(vtype="B", name="row-{}".format(r))
        c_[r] = model.addVar(vtype="B", name="row-{}".format(r))

    # Nur 1 Buchstaben pro Feld
    for x in range(row):
        for y in range(col):
            model.addCons(quicksum(s[x, y, l] for l in range(0, len(ALPHABET))) == 1)

    # Nur 1 Buchstaben pro Feld
    for x in range(row):
        for y in range(col):
            model.addCons(quicksum(s[x, y, l] for l in range(0, len(ALPHABET))) == 1)

    # CONSTRAINTS
    # C A N
    # A G E
    # R O W
    # - - - - - - - - - - - - - - - - - -
    """
    OR
    d ≥ d1
    d ≥ d2
    d ≥ d3
    d ≤ d1 + d2 +d3
    d≤1

    AND
    d ≤ d1 
    d ≤ d2 
    d ≥ d1+d2−1 
    d ≥ 0
    """
    #( s[0, 0, 2] AND s[0, 1, 0] AND s[0, 2, 13] ) OR (s[0, 0, 0] AND  s[1, 1, 6] AND s[1, 2, 4]) OR ....
    # Word 0 (AND)
    for r in range(row):
        word_list = []
        for i, word in enumerate(DICTIONARY):
            indexes = []
            for j, letter in enumerate(word):
                idx = ALPHABET.index(letter)
                indexes.append(s[r, j, idx])
                model.addCons(w_h[r, i] <= s[r, j, idx])
            model.addCons(w_h[r, i] >= quicksum(indexes) - (row-1))
            model.addCons(w_h[r, i] >= 0)

            # wort 0 bei row 0 oder wort 1 bei row 0 oder ...
            model.addCons(r_[r] >= w_h[r, i])
            word_list.append(w_h[r, i])
        model.addCons(r_[r] <= quicksum(word_list))
        model.addCons(r_[r] <= 1)

    # ein wort
    for r in range(row):
        model.addCons(quicksum(w_h[r, i] for i in range(0, len(DICTIONARY))) == 1)

    # Does not work
    #model.addCons(quicksum(r_[r] for r in range(0, 3)) == 1)
    # for i, word in enumerate(DICTIONARY):
    #     if i > 2:
    #         continue
    #     model.addCons(quicksum(w_h[r, i] for r in range(0,3)) >= 1)

    # =========================================================
    for c in range(col):
        word_list = []
        for i, word in enumerate(DICTIONARY):
            indexes = []
            for j, letter in enumerate(word):
                idx = ALPHABET.index(letter)
                indexes.append(s[j, c, idx])
                model.addCons(w_v[c, i] <= s[j, c, idx])
            model.addCons(w_v[c, i] >= quicksum(indexes) - (row-1))
            model.addCons(w_v[c, i] >= 0)

            # wort 0 bei row 0 oder wort 1 bei row 0 oder ...
            model.addCons(c_[c] >= w_v[c, i])
            word_list.append(w_v[c, i])
        model.addCons(c_[c] <= quicksum(word_list))
        model.addCons(c_[c] <= 1)

    for r in range(row):
        model.addCons(quicksum(w_v[r, i] for i in range(0, len(DICTIONARY))) == 1)
        model.addCons(quicksum(w_h[r, i] for i in range(0, len(DICTIONARY))) == 1)


    model.setBoolParam("misc/allowdualreds", False)
    #model.writeProblem('/tmp/Crossword.lp')
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
    handler = logging.FileHandler('/tmp/crossword_MIP.log', mode='w')
    handler.setLevel(logging.DEBUG)

    # create a logging format
    formatter = logging.Formatter('%(name)s: [%(levelname)s] - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)
    logger.info("Start Problem")
    main()
