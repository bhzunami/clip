#!/usr/bin/env python3
#
# CONSRESPROP

from pyscipopt import Model, Conshdlr, SCIP_RESULT, quicksum
import pdb
import logging
import numpy as np
import timer
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
        self.print_cross(cross)

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

    def propagate_cons(self, cons):
        fixed_variables = []
        reduce = False
        #pdb.set_trace()

        for var in cons.data.vars:
            if var.getUbLocal() - var.getLbLocal() >= 0.5:  # If not set
                x, y, l = var.name.split('-')
                possible_letters_h = set([w[int(y)] for w in self.dictionary])
                possible_letters_v = set([w[int(x)] for w in self.dictionary])
                possible_letters = list(possible_letters_h - (possible_letters_h - possible_letters_v))

                if len(possible_letters) == 1 and possible_letters[0] == string.ascii_uppercase[int(l)]:
                    self.model.chgVarLb(var, 1.0)
                    reduce = True

                if string.ascii_uppercase[int(l)] not in possible_letters:
                    self.model.chgVarUb(var, -0.0)
                    reduce = True

        # for var in cons.data.vars:
        #     print("{}, lb: {} ub: {}".format(var.name, var.getLbLocal(), var.getUbLocal()))
        # pdb.set_trace()
        if reduce:
            return SCIP_RESULT.REDUCEDDOM

        return SCIP_RESULT.DIDNOTFIND

    def consprop(self, constraints, nusefulconss, nmarkedconss, proptiming):
        result = SCIP_RESULT.DIDNOTFIND
        #print("CONSPROP: in stage: {}".format(self.model.getStage()))
        result = self.propagate_cons(constraints[0])
        #print("RESULT: {}".format(result))
        return {"result": result}