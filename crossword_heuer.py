#!/usr/bin/env python3

from pyscipopt import Model, Heur, SCIP_RESULT
from itertools import permutations
import pdb
import logging
import string
import numpy as np


EPS = 1.e-6
class CrosswordHeuerBrutetForce(Heur):

    def __init__(self, dict, length, logger=None):
        self.dict = dict
        self.length = length
        self.logger = logger or logging.getLogger(__name__)



    def check_cross(self, cross):
        builded_words = []
        for x in range(self.length):
            word = []
            for y in range(self.length):
                try:
                    word.append(cross[x][y])
                except IndexError:
                    print("Not valid")
                    return False
            # Create word
            builded_words.append(''.join(word))

        # Check horizontal words
        for x in range(self.length):
            word = []
            for y in range(self.length):
                word.append(cross[y][x])
            # Create word
            builded_words.append(''.join(word))

        for word in self.dict:
            if word not in builded_words:
                return False

        return True



    def heurexec(self, heurtiming, nodeinfeasible):
        cross = [[15, 8, 4, 17],
                 [8, 3, 11, 4],
                 [13, 14, 18, 4],
                 [18, 11, 4, 3]]

        # list(permutations(DICTIONARY))
        found = False
        possible_solutions = list(permutations(self.dict, self.length))
        print("Try {} solutions".format(len(possible_solutions)))
        for i, c in enumerate(possible_solutions):
            sol = self.model.createSol(self)
            vars = self.model.getVars()
            cross = []
            for x, word in enumerate(c):      # Row
                row = []
                for y, l in enumerate(word):  # Col
                    row.append(l)
                cross.append(row)
            accepted = self.check_cross(cross)
            if accepted:
                print("Found solution after {} attempts".format(i))
                found = True
                break
            if i % 1000 == 0:
                print("{} to go".format(len(possible_solutions) -i))

        if not found:
            return {"result": SCIP_RESULT.DIDNOTFIND}

        for x in range(self.length):
            for y in range(self.length):
                var = [v for v in vars if v.name == '{}-{}-{}'.format(x, y, string.ascii_uppercase.index(cross[x][y]))][0]
                self.model.setSolVal(sol, var, 1)

        accepted = self.model.trySol(sol)

        if accepted:
            return {"result": SCIP_RESULT.FOUNDSOL}
        else:
            return {"result": SCIP_RESULT.DIDNOTFIND}



class CrosswordHeuer(Heur):

    def __init__(self, dict, row, col, lb, ub, logger=None):
        self.dictionary = dict
        self.row = row
        self.col = col
        self.lb = lb
        self.ub = ub
        self.logger = logger or logging.getLogger(__name__)


    def check_words(self, solution, fixed_vars):
        if len(fixed_vars) >= self.row * self.col:
            return solution

        for var in fixed_vars:
            x, y, l = [int(x) for x in var.name.split('-')]
            possible_words_v = set([w for w in self.dictionary if w[x] == string.ascii_uppercase[l]])
            possible_words_h = set([w for w in self.dictionary if w[y] == string.ascii_uppercase[l]])

            # set horizontal word
            print(solution)
            for word in possible_words_h:
                print("Check word {}".format(word))
                offset = y
                for i, letter in enumerate(word):
                    pdb.set_trace()
                    if solution[x][y-offset+i] == -1 or solution[x][y-offset+i] == letter:
                        solution[x][y-offset+i] = letter
                        print("Set letter {} on pos {} {}".format(letter, x, y-offset+i))
                    else:
                        print("BREAK")
                index = x





    def heurexec(self, heurtiming, nodeinfeasible):
        # get fixed vars:
        vars = self.model.getVars()
        sol = self.model.createSol(self)
        solution = np.zeros([6, 6])
        solution[solution == 0] = -1
        solution = solution.tolist()

        fixed_vars = [v for v in vars if v.getLbLocal() >= 0.5]
        for var in fixed_vars:
            x, y, l = [int(x) for x in var.name.split('-')]
            solution[x][y] = string.ascii_uppercase[l]
        
        self.check_words(solution, fixed_vars)

        return {"result": SCIP_RESULT.DIDNOTFIND}
