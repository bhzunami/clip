#!/usr/bin/env python3
#
# CONSRESPROP

from pyscipopt import Model, Conshdlr, SCIP_RESULT, quicksum
import pdb
import logging
import copy
import re
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
        solution = np.zeros((self.col, self.row), dtype=str)
        for x in range(self.row):
            for y in range(self.col):
                var_set = False
                for l in range(0, len(ALPHABET)):
                    var = vars[x, y, l]
                    if self.model.getSolVal(sol, var) > 0.5:
                        if var_set:
                            raise Exception("Invalid")
                        solution[x][y] = ALPHABET[l]
                        var_set = True
        return solution

    def checkCross(self, vars, solution=None):
        try:
            cross = self.buildCross(vars, solution)
        except Exception:
            return False

        if len(np.where(cross == '')[0]) > 0:
            return False

        for x, row in enumerate(cross):
            for y, letter in enumerate(row):
                col = [cross[el][y] for el in range(self.col)]

                is_26_left = y == 0 or row[y-1] == ' '
                is_26_right = y == self.row - 1 or row[y+1] == ' '
                is_26_up = x == 0 or col[x-1] == ' '
                is_26_down = x == self.col - 1 or col[x+1] == ' '

                if is_26_down and is_26_left and is_26_right and is_26_up:
                    return False

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

    def find_possible_letters(self, row, y,
                              possible_letters, possible_words):

        if len(row[y]) == 1:
            return row[y], False

        is_fixed_left = y == 0 or len(row[y-1]) == 1
        is_fixed_right = y == (self.row -1) or len(row[y+1]) == 1
        is_26_left = y == 0 or (is_fixed_left and row[y-1][0] == 26)
        is_26_right = y == (self.row -1) or (is_fixed_right and row[y+1][0] == 26)

        if (is_26_left and is_26_right) or len(possible_letters) == 0:
            return (list(range(len(ALPHABET))), True)

        def get_chars(chars):
            return ''.join([ALPHABET[l] for l in chars if l != 26])

        def get_left(row, y):
            if y < 0 or len(row[y]) == 0 or (len(row[y]) == 1 and row[y][0] == 26):
                return r"^"
            part = r"{}[{}]".format(get_left(row, y-1), get_chars(row[y]))
            if 26 in row[y]:
                return r"(?:{}|^)".format(part)
            return part

        def get_right(row, y):
            if y >= len(row) or len(row[y]) == 0 or (len(row[y]) == 1 and row[y][0] == 26):
                return r"$"
            part = r"[{}]{}".format(get_chars(row[y]), get_right(row, y+1))
            if 26 in row[y]:
                return r"(?:$|{})".format(part)
            return part

        regex = r"{}([{}]){}".format(get_left(row, y-1), get_chars(possible_letters), get_right(row, y+1))

        matched_letters = set()
        for word in possible_words:
            match = re.search(regex, word)
            if match:
                matched_letters.add(match.group(1))

        searched = [ALPHABET.index(l) for l in matched_letters]
        if len(matched_letters) == 0 or 26 in possible_letters:
            searched.append(26)

        if is_fixed_left and is_fixed_right:
            return searched, False

        if is_26_left or is_26_right:
            return possible_letters, True

        if is_fixed_left or is_fixed_right:
            return searched, False

        return possible_letters, False


    def words_possible_at(self, letter, row, y):
        letter = ALPHABET[letter]
        # All possible Words
        # Check if Bike can be placed
        possible_words = []
        for word in self.dictionary:
            if letter not in word:
                continue
            indices = [i for i, l in enumerate(word) if l == letter]
            # impossibles_indices = 0
            for idx in indices:
                if y - idx < 0:
                    # impossibles_indices += 1
                    continue
                temp_y = y - idx

                if temp_y + len(word) > self.col:
                    # impossibles_indices += 1
                    continue

                break_ = False
                for l_idx, l in enumerate(word):
                    if ALPHABET.index(l) not in row[temp_y+l_idx]:
                        break_ = True
                        break
                if break_:
                    continue
                possible_words.append(word)
        return possible_words


    def propagate_cons(self, cons):
        solution = np.zeros([self.row, self.col]).tolist()
        fixed_letters = np.zeros([self.row, self.col])

        for x in range(self.row):
            for y in range(self.col):
                solution[x][y] = []
                fixed_letters[x][y] = -1

        fixed_vars = 0
        for key, var in cons.data.vars.items():
            x, y, l = key
            # Not fixed but possible
            if var.getUbLocal() >= 0.5 and var.getLbLocal() <= 0.5:
                solution[x][y].append(l)

            # Fixed
            if var.getLbLocal() >= 0.5:
                solution[x][y].append(l)
                fixed_letters[x][y] = l
                fixed_vars += 1

        #print("FIXED: {}".format(fixed_vars))
        # All vars are fixed
        if fixed_vars == self.row * self.col:
            return SCIP_RESULT.DIDNOTFIND

        reduce_dom = False
        for x, row in enumerate(solution):
            #row = copy.deepcopy(solution[x])
            for y, let in enumerate(row):
                col = [solution[el][y] for el in range(self.col)]
                possible_letters_h = []
                possible_letters_v = []
                possible_words_h = set()
                possible_words_v = set()
                for letter in row[y]:
                    if letter == 26:
                        possible_letters_v.append(26)
                        possible_letters_h.append(26)
                        continue

                    words = self.words_possible_at(letter, row, y)
                    if len(words) > 0:
                        possible_letters_h.append(letter)
                        possible_words_h.update(words)

                    words = self.words_possible_at(letter, col, x)
                    if len(words) > 0:
                        possible_letters_v.append(letter)
                        possible_words_v.update(words)

                possible_letters_h, intersect_h = self.find_possible_letters(row, y, possible_letters_h, possible_words_h)
                possible_letters_v, intersect_v = self.find_possible_letters(col, x, possible_letters_v, possible_words_v)

                if not intersect_h and not intersect_v:
                    possible_letters = set(possible_letters_h + possible_letters_v)
                elif not intersect_v:
                    possible_letters = possible_letters_v
                elif not intersect_h:
                    possible_letters = possible_letters_h
                # elif len(possible_letters_h) == len(ALPHABET) and len(possible_letters_v) == len(ALPHABET):
                #     return SCIP_RESULT.CUTOFF
                else:
                    possible_letters = set(possible_letters_h).intersection(set(possible_letters_v))

                #print("*"*10)
                #print("pos: [{}][{}] {}".format(x, y, possible_letters))
                #pdb.set_trace()
                if len(possible_letters) == 0:
                    print("CUTOFF")
                    return SCIP_RESULT.CUTOFF

                for i in range(len(ALPHABET)):
                    if i not in possible_letters and cons.data.vars[x, y, i].getUbLocal() >= 0.5:
                        reduce_dom = True
                        self.model.chgVarUb(cons.data.vars[x, y, i], -0.0)


        if reduce_dom:
            return SCIP_RESULT.REDUCEDDOM

        return SCIP_RESULT.DIDNOTFIND

    def consprop(self, constraints, nusefulconss, nmarkedconss, proptiming):
        result = self.propagate_cons(constraints[0])
        return {"result": result}
