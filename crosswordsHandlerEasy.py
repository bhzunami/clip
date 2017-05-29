#!/usr/bin/env python3
#
# CONSRESPROP

from pyscipopt import Model, Conshdlr, SCIP_RESULT, quicksum
import pdb
import logging
import numpy as np
from types import SimpleNamespace
from dictionary import ALPHABET

EPS = 1.e-6
class CrosswordsEasyHdlr(Conshdlr):
    def __init__(self, dictionary, lb, ub, row=10, col=10, logger=None):
        self.row = row
        self.col = col
        self.dictionary = dictionary
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
                    var = vars[x, y, l]
                    if self.model.getSolVal(sol, var) > 0.5:
                        row.append(ALPHABET[l])
            solution.append(row)
        return solution

    def checkCross(self, vars, solution=None):
        cross = self.buildCross(vars, solution)

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

        if len(builded_words) != len(set(builded_words)):
            return False

        words = self.dictionary.copy()
        for word in builded_words:
            if word not in words:
                return False
        return True

    def conscheck(self, constraints, solution, checkintegrality,
                  checklprows, printreason, completely):
        sol = self.checkCross(constraints[0].data.vars, solution)
        if sol:
            return {"result": SCIP_RESULT.FEASIBLE}
        return {"result": SCIP_RESULT.INFEASIBLE}

    def consenfolp(self, constraints, n_useful_conss, sol_infeasible):
        sol = self.checkCross(constraints[0].data.vars)
        if sol:
            return {"result": SCIP_RESULT.FEASIBLE}
        return {"result": SCIP_RESULT.INFEASIBLE}


    def conslock(self, constraint, nlockspos, nlocksneg):
        pass

    def letter_is_possible_at(self, letter, row, y):
        letter = ALPHABET[letter]
        possible_words = [word for word in self.dictionary if letter in word]
        deleted_words = 0
        for word in possible_words:
            indices = [i for i, l in enumerate(word) if l == letter]
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
        for key, var in cons.data.vars.items():
            x, y, l = key
            # Not fixed
            if var.getUbLocal() >= 0.5 and var.getLbLocal() <= 0.5:
                solution[x][y].append(l)

            # Fixed
            if var.getLbLocal() >= 0.5:
                solution[x][y].append(l)
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

                possible_letters = []
                for letter in solution[x][y]:
                    if self.letter_is_possible_at(letter, row, y):
                        possible_letters_h.append(letter)

                for letter in possible_letters_h:
                    if self.letter_is_possible_at(letter, col, x):
                        possible_letters.append(letter)

                if len(possible_letters) == 0:
                    return SCIP_RESULT.CUTOFF

                for i in range(len(ALPHABET)):
                    if i not in possible_letters and cons.data.vars[x, y, i].getUbLocal() >= 0.5:
                        reduce_dom = True
                        self.model.chgVarUb(cons.data.vars[x, y, i], -0.0)

        if reduce_dom:
            return SCIP_RESULT.REDUCEDDOM

        return SCIP_RESULT.DIDNOTFIND

    def consprop(self, constraints, nusefulconss, nmarkedconss, proptiming):
        return {"result": self.propagate_cons(constraints[0])}
