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
    max_var_value = -1
    max_var = None
    for var in vars:
        if max_var_value < var.getLbLocal():
            max_var = var
            max_var_value = var.getLbLocal()

    return max_var


EPS = 1.e-6
class CrosswordsHdlr(Conshdlr):

    def __init__(self, dictionary, variables, lb, ub, row=10, col=10, logger=None):
        self.row = row
        self.col = col
        self.variables = variables
        self.dictionary = dictionary
        self.lb = lb
        self.ub = ub
        self.used_words = []
        self.run = False
        self.logger = logger or logging.getLogger(__name__)


    def buildCross(self, vars, sol=None):
        solution = []
        for x in range(self.row):
            row = []
            for y in range(self.col):
                for l in range(self.lb, self.ub+1):
                    var = [v for v in vars if v.name == "{}-{}-{}".format(x, y, l)][0]
                    if self.model.getSolVal(sol, var) > EPS:
                        row.append(string.ascii_uppercase[l])

            # Only one letter per field is allowed
            if len(row) != self.row:
                return None
            
            solution.append(row)
        return solution

    def checkCross(self, vars, solution=None):
        cross = self.buildCross(vars, solution)
        
        if not cross or len(cross[0]) == 0:
            return False

        #print("CHECK CROSS {}".format(cross))
        builded_words = []
        # Check vertical words
        for x in range(self.row):
            word = []
            for y in range(self.col):
                word.append(cross[x][y])
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
                  
        if self.checkCross(vars, solution):
            return {"result": SCIP_RESULT.FEASIBLE}
        return {"result": SCIP_RESULT.INFEASIBLE}

    def consenfolp(self, constraints, n_useful_conss, sol_infeasible):
        cons = constraints[0]  # We only have one constraints
        vars = cons.data.vars
        if self.checkCross(vars):
            return {"result": SCIP_RESULT.FEASIBLE}
        return {"result": SCIP_RESULT.INFEASIBLE}


    def conslock(self, constraint, nlockspos, nlocksneg):
        pass

#==========================================

    def find_horizontal_fixed_vars(self, cross, x, letter):
        return [(i, w[1]) for i, w in enumerate(cross[x]) if w[0] is not None and w[1] is not letter]
        
    def find_vertical_fixed_vars(self, cross, y, letter):
        """
        Get col
        """
        elements = []
        for row in cross:
            elements.append(row[y])
        
        return [(i, w[1]) for i, w in enumerate(elements) if w[0] is not None and w[1] is not letter]

    def filter_possible_words(self, possible, filter):
        if len(filter) < 1:
            return possible

        pos = []
        for f in filter:
            pos.extend(w for w in possible if w[f[0]] == f[1])

        return pos

    def set_word_v(self, word, cross, y, cons):
        
        for i, w in enumerate(word):
            var = [v for v in cons.data.vars if v.name == '{}-{}-{}'.format(i, y, string.ascii_uppercase.index(w))][0]
            try:
                del cons.data.domains[var.ptr()]
            except Exception:
                return SCIP_RESULT.DIDNOTFIND

            for var in [v for v in cons.data.vars if v.name.startswith('{}-{}'.format(i, y))]:
                if var.name == '{}-{}-{}'.format(i, y, string.ascii_uppercase.index(w)):
                    self.model.chgVarLb(var, 1)
                    self.model.chgVarUb(var, 1)
                else:
                    self.model.chgVarLb(var, 0)
                    self.model.chgVarUb(var, 0)
            cross[i][y] = (var, w)

        
        self.run = True
        cros2 = self.buildCross(cons.data.vars)
        print("INSERT: {} in cross {}".format(word, cross))
        pdb.set_trace()
        return SCIP_RESULT.REDUCEDDOM

    def find_words(self, cross, cons):
        for x in range(self.row):
            for y in range(self.col):
                # Ignoriere (None, None) einträge
                if cross[x][y][0] is None:
                    continue
                
                # Wir haben ein Buchstaben an Position x, y
                l = cross[x][y][1]

                # horizonal
                # Welche Wörter haben wir im dictionary an der der Buchstabe l an y-Position vorkommt
                possible_words_h = list(set([w for w in self.dictionary if w[y] == l]))
                # If there is no word which can be set, it must be a wrong letter
                if len(possible_words_h) < 1:
                    return SCIP_RESULT.CUTOFF

                # vertical
                # Welche Wörter haben wir im dictionary an der der Buchstabe l an x-Position vorkommt                
                possible_words_v = list(set([w for w in self.dictionary if w[x] == l]))
                if len(possible_words_v) < 1:
                    return SCIP_RESULT.CUTOFF

                # Hole definierte felder um zu filtern.
                fixed_h = self.find_horizontal_fixed_vars(cross, x, l)

                fixed_v = self.find_vertical_fixed_vars(cross, y, l)
            
                # Gebe nur wörter zurück, die auch möglich sind
                possible_words_h = self.filter_possible_words(possible_words_h, fixed_h)
                if len(possible_words_h) < 1:
                    return SCIP_RESULT.CUTOFF

                if len(possible_words_h) == 1:
                    # Only this word can be set
                    pass


                possible_words_v = self.filter_possible_words(possible_words_v, fixed_v)
                if len(possible_words_v) < 1:
                    return SCIP_RESULT.CUTOFF

                if len(possible_words_v) == 1:
                    return self.set_word_v(possible_words_v[0], cross, y, cons)

        return SCIP_RESULT.DIDNOTFIND    
    
    def propagate_cons(self, cons):
        vars = cons.data.vars
        fixed_variables = []
        for var in vars:
            if var.getUbLocal() - var.getLbLocal() <= 0.5:
                fixed_variables.append(var)
        
        if len(fixed_variables) == 0 or len(fixed_variables) == self.row:
            return SCIP_RESULT.DIDNOTFIND
        
        cross = []
        for x in range(self.row):
            row = []
            for y in range(self.col):
                # Hole nur die Variabeln, die zu diesem Quadrat (x,y) gehören. Maximal so viele wie es Buchstaben hat
                # Und hole die Variable die Auf 1 gesetzt ist
                var = max_var([var for var in fixed_variables if var.name.startswith('{}-{}'.format(x, y))])
                try:
                    letter = string.ascii_uppercase[int(var.name.split('-')[-1])]
                    row.append((var, letter))
                except AttributeError:
                    row.append((None, None))
            cross.append(row)
        # Ich weiss an welchem Ort im Kreuzworträtsel welche Buchstaben gesetzt ist
        return self.find_words(cross, cons)  # setWords

    def consprop(self, constraints, nusefulconss, nmarkedconss, proptiming):
        result = SCIP_RESULT.DIDNOTFIND
        for cons in constraints:
            if len(cons.data.domains.keys()) < 1:
                return {"result": result}
            result = self.propagate_cons(cons)
 
        return {"result": result}
