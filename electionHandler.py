#!/usr/bin/env python3
#
# CONSRESPROP

from pyscipopt import Model, Conshdlr, SCIP_RESULT, quicksum
import pdb
import logging
import numpy as np
import timer
from types import SimpleNamespace

EPS = 1.e-6
class ElectionHdlr(Conshdlr):

    def __init__(self, variables, row=10, col=10, cons=10, logger=None):
        self.row = row
        self.col = col
        self.constituency = cons
        self.variables = variables
        self.logger = logger or logging.getLogger(__name__)
        self.time_deepsearch = []
        self.time_check_neighbour = []
        self.count_check_neighbour = 0
        self.checked = False


    def createData(self, constraint, nvars, othername):
        print("Creating data for my constraint: %s"%constraint.name)
        constraint.data = SimpleNamespace()
        constraint.data.nvars = nvars
        constraint.data.myothername = othername

    def checkValue(self, val, x, y):
        try:
            val[x][y]
            return True
        except IndexError:
            return False

    def deepSearch(self, solution, pos_x, pos_y):
        """From the given start point check all direction (star formation),
         if the next neigbhour has the same value as the start point.
         If yes add this next point to our list
        """
        fields = [{'x': pos_x, 'y': pos_y}]
        value = solution[pos_x][pos_y]
        while len(fields) > 0:
            field = fields.pop(0)
            x = field['x']
            y = field['y']

            solution[x][y] = -1

            # Check right:
            if y < self.col and \
               self.checkValue(solution, x, y+1) and \
               solution[x][y+1] != -1 and \
               solution[x][y+1] == value:
                fields.append({'x': x, 'y': y+1})

            # check left
            if y > 0 and \
               self.checkValue(solution, x, y-1) and \
               solution[x][y-1] != -1 and \
               solution[x][y-1] == value:
                fields.append({'x': x, 'y': y-1})

            # Check down
            if x < self.row and \
               self.checkValue(solution, x+1, y) and \
               solution[x+1][y] != -1 and \
               solution[x+1][y] == value:
                fields.append({'x': x+1, 'y': y})

            # Check up
            if x > 0 and \
               self.checkValue(solution, x-1, y) and \
               solution[x-1][y] != -1 and \
               solution[x-1][y]== value:
                fields.append({'x': x-1, 'y': y})

            # Check vertical right down
            if x < self.row and \
               y < self.col and \
               self.checkValue(solution, x+1, y+1) and \
               solution[x+1][y+1] != -1 and \
               solution[x+1][y+1] == value:
                fields.append({'x': x+1, 'y': y+1})

            # Check vertical right up
            if x > 0 and \
               y < self.col and \
               self.checkValue(solution, x-1, y+1) and \
               solution[x-1][y+1] != -1 and \
               solution[x-1][y+1] == value:
                fields.append({'x': x-1, 'y': y+1})

            # Check vertical left up
            if x > 0 and y > 0 and \
               self.checkValue(solution, x-1, y-1) and \
               solution[x-1][y-1] != -1 and \
               solution[x-1][y-1] == value:
                fields.append({'x': x-1, 'y': y-1})

            # Check vertical left down
            if x < self.row and \
               y > 0 and \
               self.checkValue(solution, x+1, y-1) and \
               solution[x+1][y-1] != -1 and \
               solution[x+1][y-1] == value:
                fields.append({'x': x+1, 'y': y-1})


    def checkNeighbour(self, sol=None):
        """Check if the constituency are all aside
        """
        solution = []
        #self.count_check_neighbour += 1
        #print("Check neigh: {}".format(self.count_check_neighbour%100))
        var = self.variables
        for x in range(self.row):
            row = []
            for y in range(self.col):
                for w in range(self.constituency):
                    if self.model.getSolVal(sol, var[x, y, w]) > EPS:
                        row.append(w)

            if len(row) != self.col:
                return {'solution': False}

            solution.append(row)
        

        if not solution[0]:
            return {'solution': False}

        visited_constituency = set()
        for x in range(self.row):
            for y in range(self.col):

                try:
                    solution[x][y]
                except IndexError:
                    continue
                
                if solution[x][y] == -1:  # Visited
                    continue
                # Check if this constituency is in our list

                if solution[x][y] in visited_constituency:
                    return {'solution': False, 'x': x, 'y': y, 'w': solution[x][y]}
                # Set visited flag for
                visited_constituency.add(solution[x][y])
                self.logger.info("Deep search from x: {}, y: {} for element {}".format(x,
                                                                                       y,
                                                                                       solution[x][y]))

                with timer.Timer() as t:
                    # print("DEEPSEARCH FOR {}".format(solution[x][y]))
                    self.deepSearch(solution, x, y)
                self.time_deepsearch.append(t.msecs)

                if len(self.time_deepsearch) == 100:
                    #print("Avg deep search time: {}".format(np.mean(self.time_deepsearch)))
                    self.time_deepsearch = []

        return {'solution': True}

    def conscheck(self, constraints, solution, checkintegrality,
                  checklprows, printreason, completely):
        self.logger.info("-"*20)
        sol = self.checkNeighbour(solution)
        if sol['solution']:
            self.logger.info("Solution seems OK")
            return {"result": SCIP_RESULT.FEASIBLE}
        else:
            self.logger.info("Solution is not OK")
            return {"result": SCIP_RESULT.INFEASIBLE}


    def consenfolp(self, constraints, n_useful_conss, sol_infeasible):
        # pdb.set_trace()
        sol = self.checkNeighbour()
        if sol['solution']:
            return {"result": SCIP_RESULT.FEASIBLE}
        
        # Add cons to avoid using at this position [x,y,w] != 1
        # self.model.addCons(var[sol['x'], sol['y'], sol['w']] == 0)
        #self.addConstraint()
        #return {"result": SCIP_RESULT.CONSADDED}
        return {"result": SCIP_RESULT.CUTOFF}
        #return {"result": SCIP_RESULT.INFEASIBLE}


    def addConstraint(self):
        var = self.variables
        for x in range(1, self.col-1):
            for y in range(1, self.row-1):
                constraints = []
                # Get the index where w = 1
                w = [i for i, j in enumerate(self.model.getSolVal(None, var[x, y, w]) for w in range(self.constituency)) if j > EPS][0]
                # Left
                constraints.append(var[x, y+1, w])
                # right
                constraints.append(var[x, y-1, w])
                # up
                constraints.append(var[x-1, y, w])
                #down
                constraints.append(var[x+1, y+1, w])
                #left up
                constraints.append(var[x-1, y+1, w])
                # left down
                constraints.append(var[x+1, y+1, w])
                # right up
                constraints.append(var[x-1, y-1, w])
                # right down
                constraints.append(var[x+1, y+1, w])
                self.model.addCons(quicksum(constraints) >= 2)


    def conslock(self, constraint, nlockspos, nlocksneg):
        pass
    #     pdb.set_trace()
    #     #for var in constraint.data.vars:
    #     #    self.model.addVarLocks(var, nlockspos + nlocksneg , nlockspos + nlocksneg)
    #     return {}

    # def constrans(self, constraint):
    #     return {}


    # def conscopy(self):
    #     print("COPY")

    #     pdb.set_trace()
    #     return {}

    # def consinitsol(self, constraints):
    #     pdb.set_trace()
    #     return {}
        

    # def consenfops(self, constraints, nusefulconss, solinfeasible, objinfeasible):
    #     # The CONSENFOPS callback is similar to the CONSENFOLP callback, but deals with pseudo solutions instead of LP solutions. because numerical difficulties in the LP solving process were detected
    #     pass
    #     pdb.set_trace()

    def consprop(self, constraints, nusefulconss, nmarkedconss, proptiming):
        #pdb.set_trace()
        return {"result": SCIP_RESULT.DIDNOTFIND}

    # def conspresol(self, constraints, nrounds, presoltiming,
    #                nnewfixedvars, nnewaggrvars, nnewchgvartypes, nnewchgbds, nnewholes,
    #                nnewdelconss, nnewaddconss, nnewupgdconss, nnewchgcoefs, nnewchgsides, result_dict):
    #     pdb.set_trace()
    #     return result_dict