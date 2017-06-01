#!/usr/bin/env python3
#
# CONSRESPROP

from pyscipopt import Model, Conshdlr, SCIP_RESULT, quicksum
import pdb
import logging
import numpy as np
from dictionary import ALPHABET

EPS = 1.e-6
class CrosswordsHdlr(Conshdlr):

    def __init__(self, dictionary, row=10, col=10, logger=None):
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

        if not cross or len(cross[0]) == 0:
            return False

        # self.print_cross(cross)
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

        builded_words = [word for word in builded_words if len(word) > 1]
        if len(builded_words) != len(set(builded_words)):
            return False

        if len(builded_words) == 0:
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

    def check_if_blank_is_possible(row, y):
        if y == 0:
            return True
        # Wenn nur 26 Möglich oder wenn im feld rechts mehr als 1 Buchstabe
        if len(row[y]) == 1 or len(row[y-1]) >= 1:
            return True
        if len(row[y-1]) == 1:
            # check if we found
            letter = ALPHABET[row[y-1][0]]
            possible_words = [word for word in self.dictionary if letter in word]
        

    def letter_is_possible_at(self, letter, row, y):
        if letter == 26:
            pdb.set_trace()
            return True

        letter = ALPHABET[letter]
        possible_words = [word for word in self.dictionary if letter in word]
        # All possible Words
        # Check if Bike can be placed
        deleted_words = 0

        for word in possible_words.copy():
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
            # Not fixed but possible
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

                possible_letters_v = []

                for letter in solution[x][y]:
                    if self.letter_is_possible_at(letter, row, y):
                        possible_letters_h.append(letter)
                    if self.letter_is_possible_at(letter, col, x):
                        possible_letters_v.append(letter)

                # Wenn x + 1 oder x-1 nicht definiert (len(solution[x+1][y]) > 1) dann kein Intersect
                is_fixed_up = x == 0 or len(solution[x-1][y]) == 1
                is_fixed_left = y == 0 or len(solution[x][y-1]) == 1
                is_fixed_down = x == (self.col - 1) or len(solution[x+1][y]) == 1
                is_fixed_right = y == (self.row -1) or len(solution[x][y+1]) == 1

                is_26_up = x == 0 or (is_fixed_up and solution[x-1][y][0] == 26)
                is_26_left = y == 0 or (is_fixed_left and solution[x][y-1][0] == 26)
                is_26_down = x == (self.col - 1) or (is_fixed_down and solution[x+1][y][0] == 26)
                is_26_right = y == (self.row -1) or (is_fixed_right and solution[x][y+1][0] == 26)

                # Rechts und links steht 26
                if is_26_left and is_26_right:
                    possible_letters = possible_letters_v

                # Oben unten steht 26
                elif is_26_up and is_26_down:
                    possible_letters = possible_letters_h

                # Oben fix und nicht 26 (oebn)
                # und links oder rechts ist fixiert aber nicht mit 26
                elif is_fixed_up and not is_26_up and ((is_fixed_left and not is_26_left) or (is_fixed_right and not is_26_right) ):
                    possible_letters = set(possible_letters_h).intersection(set(possible_letters_v))

                # unten fix und nicht 26 (unten)
                # und links oder rechts ist fixiert aber nicht mit 26
                elif is_fixed_down and not is_26_down and ((is_fixed_left and not is_26_left) or (is_fixed_right and not is_26_right) ):
                    possible_letters = set(possible_letters_h).intersection(set(possible_letters_v))
                # Ansonsten alles offen
                else:
                    possible_letters = set(possible_letters_h + possible_letters_v)

                # possible_letters = set(possible_letters_h).intersection(set(possible_letters_v))
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
