#!/usr/bin/env python3
#
# CONSRESPROP

from pyscipopt import Model, Conshdlr, SCIP_RESULT, quicksum
import pdb
import logging
import numpy as np
import timer
import time
import string
import datetime
from types import SimpleNamespace
#from crossword_problem import ALPHABET
from dictionary import ALPHABET
#ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def max_var(vars):
    """
    Gibt das höchste l zurück
    für die Position x,y l
    """
    max_var_value = -1
    max_var = None
    for var in vars:
        if max_var_value < var.getLbLocal():
            max_var = var
            max_var_value = var.getLbLocal()

    return max_var


EPS = 1.e-6
class CrosswordsEasyHdlr(Conshdlr):

    def __init__(self, dictionary, lb, ub, row=10, col=10, logger=None):
        self.row = row
        self.col = col
        self.dictionary = dictionary
        self.lb = lb
        self.ub = ub
        self.debug = False
        self.propagater = 0
        self.time = 0
        self.logger = logger or logging.getLogger(__name__)

    def print_cross(self, cross):
        for r in range(self.row):
            col = []
            for c in range(self.col):
                try:
                    col.append(cross[r][c])
                except IndexError:
                    col.append(None)
            print(col)
        print("-----------------")

    def buildCross(self, vars, sol=None):
        solution = []
        for x in range(self.row):
            row = []
            for y in range(self.col):
                for l in range(0, len(ALPHABET)):
                    name = "{}-{}-{}".format(x, y, l)
                    var = [v for v in vars if v.name == name][0]
                    if self.model.getSolVal(sol, var) > 0.5:
                        row.append(ALPHABET[l])

            # Only one letter per field is allowed
            #if len(row) != self.row:
            #    return None

            solution.append(row)
        return solution

    def checkCross(self, vars, solution=None):
        cross = self.buildCross(vars, solution)

        if not cross or len(cross[0]) == 0:
            return False

        #print("CHECK CROSS {}".format(cross))
        #self.print_cross(cross)

        builded_words = []
        # Check vertical words
        for x in range(self.row):
            word = []
            for y in range(self.col):
                try:
                    if cross[x][y] == ' ':
                        builded_words.append(''.join(word))
                        word = []
                    else:
                        word.append(cross[x][y])
                except IndexError:
                    print("Not valid")
                    return False
            # Create word
            builded_words.append(''.join(word))

        
        # Check horizontal words
        for x in range(self.row):
            word = []
            for y in range(self.col):
                if cross[y][x] == ' ':
                    builded_words.append(''.join(word))
                    word = []
                else:
                    word.append(cross[y][x])
            # Create word
            builded_words.append(''.join(word))

        #pdb.set_trace()

        builded_words = [word for word in builded_words if len(word) > 1]
        
        if len(builded_words) != len(set(builded_words)):
            return False

        words = self.dictionary.copy()
        for word in builded_words:
            if word not in words:
                return False
            #del words[words.index(word)]

        return True

    def conscheck(self, constraints, solution, checkintegrality,
                  checklprows, printreason, completely):

        cons = constraints[0]  # We only have one constraints
        vars = cons.data.vars
        t1 = datetime.datetime.now()        
        sol = self.checkCross(vars, solution)
        t2 = datetime.datetime.now()
        #print("CONSCHECKTIME: {}".format(t2 - t1))
        #print("conscheck: {} in stage: {}".format(sol, self.model.getStage()))
        if sol:
            return {"result": SCIP_RESULT.FEASIBLE}
        return {"result": SCIP_RESULT.INFEASIBLE}

    def consenfolp(self, constraints, n_useful_conss, sol_infeasible):
        cons = constraints[0]  # We only have one constraints
        vars = cons.data.vars
        sol = self.checkCross(vars)
        #print("CONSENFOLP: {} in stage: {}".format(sol, self.model.getStage()))

        if sol:
            return {"result": SCIP_RESULT.FEASIBLE}
        return {"result": SCIP_RESULT.INFEASIBLE}


    def conslock(self, constraint, nlockspos, nlocksneg):
        pass

#==========================================

    def letter_is_possible_at(self, letter, row, y):
        possible_words = []
        for word in self.dictionary:
            if ALPHABET[letter] in word:
                possible_words.append(word)

        # All possible Words
        # Check if Bike can be placed
        deleted_words = 0
        # if self.debug:
        #     pdb.set_trace()
        for word in possible_words.copy():
            indices = [i for i, l in enumerate(word) if l == ALPHABET[letter]]
            impossibles_indices = 0
            for idx in indices:
                if y - idx < 0:
                    impossibles_indices += 1
                    continue
                temp_y = y - idx

                if temp_y + len(word) > self.col:
                    impossibles_indices += 1
                    continue

                for l_idx, l in enumerate(word):
                    if ALPHABET.index(l) not in row[temp_y+l_idx]:
                        impossibles_indices += 1
                        break

            if impossibles_indices == len(indices):
                deleted_words += 1
       
        return deleted_words != len(possible_words)

    def propagate_cons(self, cons):
        solution = np.zeros([self.row, self.col]).tolist()

        for x in range(self.row):
            for y in range(self.col):
                solution[x][y] = []

        fixed_vars = 0
        fff = []
        for var in cons.data.vars:
            x, y, l = [int(v) for v in var.name.split('-')]
            # Not fixed
            if var.getUbLocal() >= 0.5 and var.getLbLocal() <= 0.5:
                solution[x][y].append(l)

            # Fixed
            if var.getLbLocal() >= 0.5:
                solution[x][y].append(l)
                fff.append(l)
                fixed_vars += 1

        # All vars are fixed
        if fixed_vars == self.row * self.col:
            return SCIP_RESULT.DIDNOTFIND

        reduce_dom = False
        for x in range(self.row):
            for y in range(self.col):
                possible_letters_h = []
                row = solution[x]
                col = []
                for el in range(self.col):
                    col.append(solution[el][y])

                possible_letters_v = []
                for letter in solution[x][y]:
                    if self.letter_is_possible_at(letter, row, y):
                        possible_letters_h.append(letter)
                    if self.letter_is_possible_at(letter, col, x):
                        possible_letters_v.append(letter)

                possible_letters = set(possible_letters_h).intersection(set(possible_letters_v))

                if len(possible_letters) == 0:
                    return SCIP_RESULT.CUTOFF

                for var in [v for v in cons.data.vars if v.name.startswith("{}-{}".format(x, y))]:
                    x2, y2, l2 = [int(v) for v in var.name.split('-')]
                    if l2 not in possible_letters and var.getUbLocal() >= 0.5:
                        reduce_dom = True
                        self.model.chgVarUb(var, -0.0)

        if reduce_dom:
            return SCIP_RESULT.REDUCEDDOM

        return SCIP_RESULT.DIDNOTFIND

    def consprop(self, constraints, nusefulconss, nmarkedconss, proptiming):
        result = SCIP_RESULT.DIDNOTFIND
        self.propagater += 1
        #print("CONSPROP: in stage: {}".format(self.model.getStage()))
        t1 = datetime.datetime.now()
        result = self.propagate_cons(constraints[0])
        t2 = datetime.datetime.now()
        #print("Time: {}".format(t2 - t1))
        self.time = self.time + (t2 - t1).total_seconds()
        #print("TIME TOTAL: {}".format(self.time))
        #print("RESULT: {}".format(result))
        return {"result": result}
