#!/usr/bin/env python3

from pyscipopt import Model, Conshdlr, SCIP_RESULT
import pdb
import logging


EPS = 1.e-6
class ElectionHdlr(Conshdlr):

    def __init__(self, variables, row=10, col=10, cons=10, logger=None):
        self.row = row
        self.col = col
        self.constituency = cons
        self.variables = variables
        self.logger = logger or logging.getLogger(__name__)



    def deepSearch(self, solution, pos_x, pos_y):
        fields = [{'x': pos_x, 'y': pos_y}]
        value = solution[pos_x, pos_y]['value']
        while len(fields) > 0:
            field = fields.pop(0)
            x = field['x']
            y = field['y']

            solution[x, y]['visited'] = True
            # Check right:
            if y < 9 and not solution[x, y+1 ]['visited'] and solution[x, y+1 ]['value'] == value:
                fields.append({'x': x, 'y': y+1})

            # Check down
            if x < 9 and not solution[x+1, y ]['visited'] and solution[x+1, y ]['value'] == value:
                fields.append({'x': x+1, 'y': y})

            # Check vertical
            if x < 9 and y < 9 and not solution[x+1, y+1 ]['visited'] and solution[x+1, y+1 ]['value'] == value:
                fields.append({'x': x+1, 'y': y+1})


    def checkNeighbour(self, sol=None):
        """self.model.getSolVal(solution, x[i,j]) > EPS:
        """
        solution = {}
        var = self.variables
        for x in range(self.row):
            for y in range(self.col):
                for w in range(self.constituency):
                    if self.model.getSolVal(sol, var[x, y, w]) > EPS:
                        solution[x, y] = {'visited': False, 'value': w}

        if not solution:
            return {'solution': False}

        visited_constituency = set()
        for x in range(self.row):
            for y in range(self.col):

                # Check if this value already is visited
                if solution[x, y]['visited']:
                    continue
                # Check if this constituency is in our list
                if solution[x, y]['value'] in visited_constituency:
                    self.logger.info("Value: {} was already searched".format(solution[x, y]['value']))
                    return {'solution': False, 'x': x, 'y': y, 'w': solution[x, y]['value']}

                # Set visited flag for
                visited_constituency.add(solution[x, y]['value'])
                self.logger.info("Deep search from x: {}, y: {} for element {}".format(x, y, solution[x, y]['value']))
                self.deepSearch(solution, x, y)


        return {'solution': True}


    def conscheck(self, constraints, solution, checkintegrality,
                  checklprows, printreason, completely):
        self.logger.info("Check one solution")
        self.logger.info("-"*20)
        sol = self.checkNeighbour(solution)
        if sol['solution']:
            self.logger.info("Solution seems OK")
            return {"result": SCIP_RESULT.FEASIBLE} 
        else:
            self.logger.info("Solution is not OK")
            return {"result": SCIP_RESULT.INFEASIBLE}


    def consenfolp(self, constraints, n_useful_conss, sol_infeasible):
        self.logger.info("Check CONSENS")
        self.logger.info("="*20)
        var = self.variables
        sol = self.checkNeighbour()
        if sol['solution']:
            {"result": SCIP_RESULT.FEASIBLE}
        else:
            # Add cons to avoid using at this position [x,y,w] != 1
            # self.model.addCons(var[sol['x'], sol['y'], sol['w']] == 0)
            return {"result": SCIP_RESULT.CUTOFF}

    def conslock(self, constraint, nlockspos, nlocksneg):
        pass
