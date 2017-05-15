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
                for l in range(self.lb, self.ub+1):
                    name = "{}-{}-{}".format(x, y, l)
                    var = [v for v in vars if v.name == name][0]
                    if self.model.getSolVal(sol, var) > 0.2:
                        row.append(string.ascii_uppercase[l])

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

        for word in self.dictionary:
            if word not in builded_words:
                return False

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
    def get_possible_words(self, indexes, letters):
        words = []
        for word in self.dictionary:
            words.append(word)
            for i, index in enumerate(indexes):
                if word[int(index)] != string.ascii_uppercase[int(letters[i])]:
                    try:
                        del words[words.index(word)]
                    except ValueError:
                        pass
                    continue
        return words


    def propagate_cons(self, cons):
        reduce = False
        solution = np.zeros([self.row, self.col])
        solution[solution == 0] = -1

        for var in cons.data.vars:
            x, y, l = [int(v) for v in var.name.split('-')]
            if var.getLbLocal() >= 0.5:
                solution[x][y] = l

        #print(solution)
        for x in range(self.row):
            for y in range(self.col):
                if solution[x][y] <= 0:  # Letter not fix try to fix it
                    #print("Found [{}] [{}] which is not set".format(x, y))
                    # Get indexes where letter is set
                    indexes = np.where(solution[x] > 0)[0]
                    possible_words = []
                    letters = []
                    for index in indexes:
                        letters.append(solution[x][index])
                    possible_words.extend(self.get_possible_words(indexes, letters))
                    #print("Possible horizontal words: {}".format(possible_words))

                    letters = []
                    indexes = np.where(solution.T[x] > 0)[0]
                    for index in indexes:
                        letters.append(solution.T[x][index])

                    possible_words.extend(self.get_possible_words(indexes, letters))
                    #print("Possible vertical words: {}".format(possible_words))

                    if len(possible_words) == 0:
                        print("Cut Node")
                        return SCIP_RESULT.CUTOFF

                    for var in [v for v in cons.data.vars if v.name.startswith("{}-{}".format(x, y))]:
                        x2, y2, l2 = [int(v) for v in var.name.split('-')]
                        # print("check possible words: {}".format(set([l[y] for l in possible_words])))
                        if string.ascii_uppercase[l2] not in set([l[y] for l in possible_words]):
                            # print("Var {} ({})is not in list".format(l2, string.ascii_uppercase[l2]))
                            self.model.chgVarUb(var, -0.0)
                            reduce = True

                        if len(possible_words) == 1 and string.ascii_uppercase[l2] in set([l[y] for l in possible_words]):
                            self.model.chgVarLb(var, 1.0)

        if reduce:
            #print("REDUCE DOM")
            return SCIP_RESULT.REDUCEDDOM
        return SCIP_RESULT.DIDNOTFIND

    def consprop(self, constraints, nusefulconss, nmarkedconss, proptiming):
        result = SCIP_RESULT.DIDNOTFIND
        #print("CONSPROP: in stage: {}".format(self.model.getStage()))
        result = self.propagate_cons(constraints[0])
        #print("RESULT: {}".format(result))
        return {"result": result}