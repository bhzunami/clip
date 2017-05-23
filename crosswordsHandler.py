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
from types import SimpleNamespace

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "

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
class CrosswordsHdlr(Conshdlr):

    def __init__(self, dictionary, lb, ub, row=10, col=10, logger=None):
        self.row = row
        self.col = col
        self.dictionary = dictionary
        self.lb = lb
        self.ub = ub
        self.debug = False
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
                for l in range(self.lb, self.ub):
                    name = "{}-{}-{}".format(x, y, l)
                    var = [v for v in vars if v.name == name][0]
                    if self.model.getSolVal(sol, var) > 0.2:
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
                word.append(cross[y][x])
            # Create word
            builded_words.append(''.join(word))

        #builded_words = [word for word in builded_words if len(word) > 1]
        words = self.dictionary.copy()
        for word in builded_words:
            if word not in words:
                return False
            del words[words.index(word)]

        return True

    def conscheck(self, constraints, solution, checkintegrality,
                  checklprows, printreason, completely):

        cons = constraints[0]  # We only have one constraints
        vars = cons.data.vars
        sol = self.checkCross(vars, solution)
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
    # def get_possible_words(self, indexes, letters, x=True):
    #     if len(indexes) == 0:      # All words are possible
    #         # Give back words which can pass at this position
    #         if x:
    #             return [word for word in self.dictionary if len(word) <= self.row]

    #         return [word for word in self.dictionary if len(word) <= self.col]

    #     words = []
    #     for word in self.dictionary:
    #         words.append(word)
    #         for i, index in enumerate(indexes):
    #             if word[int(index)] != ALPHABET[int(letters[i])]:
    #                 del words[words.index(word)]
    #                 break
    #     return words

    def letter_is_possible_at(self, letter, row, y):
        #print("CHECK IF LETTER {} is possible at position {} row {}".format(letter, y, row))
        # if letter == 26:
        #     return True

        # # Check if pos-1 and pos+1 are black blocks
        # if y-1 < 0 and len(row[y+1]) == 1 and row[y+1][0] == 26:
        #     print("Fixed var pos 1")
        #     return True

        # if y+1 >= self.col and len(row[y-1]) == 1 and row[y-1][0] == 26:
        #     print("Fixed var pos 1")
        #     return True

        # if y-1 >= 0 and y+1 < self.col:
        #     if len(row[y-1]) == 1 and row[y-1][0] == 26 and len(row[y+1]) == 1 and row[y+1][0] == 26:
        #         print("Fixed var pos 1")
        #         return True

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
            #print("CHECK WORD: {}".format(word))
            indices = [i for i, l in enumerate(word) if l == ALPHABET[letter]]
            # if self.debug:
            #     print("INDICES: {}".format(indices))
            #correct = {}
            impossibles_indices = 0
            for idx in indices:
                #correct[idx] = True
                if y - idx < 0:
                    #print("TOO MUCH LEFT: {}".format(idx))
                    # Word is not possible with this index
                    #correct[idx] = False
                    impossibles_indices += 1
                    continue
                temp_y = y - idx
                #print("TEMP_Y: {}".format(temp_y))

                if temp_y + len(word) > self.col:
                    #correct[idx] = False
                    impossibles_indices += 1                    
                    #print("TOO MUCH RIGHT: {}".format(idx))
                    continue
                #print("CHECK WORD")
                for l_idx, l in enumerate(word):
                    #print("CHECK {} is in row{} row: {}:".format(l,temp_y+l_idx, row[temp_y+l_idx]))
                    if ALPHABET.index(l) not in row[temp_y+l_idx]:
                        #print("L {} not in {}".format(l, row[temp_y+l_idx]))
                        #correct[idx] = False
                        impossibles_indices += 1     
                        break

            # if self.debug:
            #     pdb.set_trace()
            if impossibles_indices == len(indices):
                deleted_words += 1
                
            # if not any(list(correct.values())):
            #     deleted_words += 1
            #     #del possible_words[possible_words.index(word)]


        return deleted_words != len(possible_words)
        # if len(possible_words) > 0:
        #     return True
        # return False

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

        # for x in range(self.col):
        #     for y in range(self.row):
        #         print("{} {}: {}".format(x, y, [string.ascii_uppercase[i] for i in solution[x][y]]))
        for x in range(self.row):
            for y in range(self.col):
                possible_letters_h = []
                row = solution[x]
                for letter in solution[x][y]:
                    if self.letter_is_possible_at(letter, row, y):
                        possible_letters_h.append(letter)

                #print("H Possibles Letters for {} {} are: {}".format(x, y, [ALPHABET[i] for i in possible_letters_h]))
                
                possible_letters_v = []
                # Build list for possible letters on y axis

                col = []
                for el in range(self.col):
                    col.append(solution[el][y])

                for letter in solution[x][y]:
                    if self.letter_is_possible_at(letter, col, x):
                        possible_letters_v.append(letter)
                #
                #print("V Possibles Letters for {} {} are: {}".format(x, y, [ALPHABET[i] for i in possible_letters_v]))
                
                possible_letters = set(possible_letters_h).intersection(set(possible_letters_v))


                if len(possible_letters) == 0:
                    #print("CUTOFF SOLUTION")
                    return SCIP_RESULT.CUTOFF

                for var in [v for v in cons.data.vars if v.name.startswith("{}-{}".format(x, y))]:
                    x2, y2, l2 = [int(v) for v in var.name.split('-')]
                    if l2 not in possible_letters:
                        self.model.chgVarUb(var, -0.0)

                #print("Possibles Letters for {} {} are: {}".format(x, y, [ALPHABET[i] for i in possible_letters]))

        #print("FINISH")
        return SCIP_RESULT.REDUCEDDOM
        # for i, x in enumerate(not_fixed_vars[0]):
        #     possible_letters = []
        #     y = not_fixed_vars[1][i]   # position of col
        #     indexes = np.where(solution[x] >= 0)[0]

        #     # horizontal
        #     possible_words = self.get_possible_words(np.where(solution[x] >= 0)[0],
        #                                              solution[x][np.where(solution[x] >= 0)],
        #                                              x=True)
        #     possible_letters_h = set([le[y] for le in possible_words])

        #     # Vertical
        #     possible_words = self.get_possible_words(np.where(solution.T[y] >= 0)[0],
        #                                              solution.T[y][np.where(solution.T[y] >= 0)],
        #                                              x=False)

        #     possible_letters_v = set([le[x] for le in possible_words])
        #     possible_letters = possible_letters_v.intersection(possible_letters_h)
            
        #     # Remove duplicate
        #     #print(possible_letters)
        #     possible_letters = set(possible_letters)
        #     if len(possible_letters) == 0:
        #         #print("No solution is possible for {}, {}".format(x, y))
        #         return SCIP_RESULT.CUTOFF

        #     # possible_letters = set([le[y] for le in possible_words]).union(set([le[x] for le in possible_words]))
        #     #if len(not_fixed_vars[0]) < 9:
        #     #    pdb.set_trace()
        #     #print("Possible letters at pos {}, {} are: {}".format(x, y, possible_letters))
        #     for var in [v for v in cons.data.vars if v.name.startswith("{}-{}".format(x, y))]:
        #         x2, y2, l2 = [int(v) for v in var.name.split('-')]
        #         # print("check possible words: {}".format(set([l[y] for l in possible_words])))
        #         if string.ascii_uppercase[l2] not in possible_letters:
        #             # print("Var {} ({})is not in list".format(l2, string.ascii_uppercase[l2]))
        #             self.model.chgVarUb(var, -0.0)
        #             reduce = True

        #         if len(possible_words) == 1 and string.ascii_uppercase[l2] in possible_letters:
        #             self.model.chgVarLb(var, 1.0)
        # #pdb.set_trace()
        # return SCIP_RESULT.REDUCEDDOM

    def consprop(self, constraints, nusefulconss, nmarkedconss, proptiming):
        result = SCIP_RESULT.DIDNOTFIND
        #print("CONSPROP: in stage: {}".format(self.model.getStage()))
        result = self.propagate_cons(constraints[0])
        #print("RESULT: {}".format(result))
        return {"result": result}
