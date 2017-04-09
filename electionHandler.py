#!/usr/bin/env python3
#
# CONSRESPROP

from pyscipopt import Model, Conshdlr, SCIP_RESULT
import pdb
import logging
import numpy as np
import timer

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


    def deepSearch(self, solution, pos_x, pos_y):
        """From the given start point check all direction (star formation),
         if the next neigbhour has the same value as the start point.
         If yes add this next point to our list
        """
        fields = [{'x': pos_x, 'y': pos_y}]
        value = solution[pos_x, pos_y]['value']
        while len(fields) > 0:
            field = fields.pop(0)
            x = field['x']
            y = field['y']

            solution[x, y]['visited'] = True

            # Check right:
            if y < self.col and \
               solution.get((x, y+1), None) and \
               not solution[x, y+1]['visited'] and \
               solution[x, y+1]['value'] == value:
                fields.append({'x': x, 'y': y+1})

            # check left
            if y > 0 and \
               solution.get((x, y-1), None) and \
               not solution[x, y-1]['visited'] \
               and solution[x, y-1]['value'] == value:
                fields.append({'x': x, 'y': y-1})

            # Check down
            if x < self.row and \
               solution.get((x+1, y), None) and \
               not solution[x+1, y]['visited'] and \
               solution[x+1, y]['value'] == value:
                fields.append({'x': x+1, 'y': y})

            # Check up
            if x > 0 and \
               solution.get((x-1, y), None) and \
               not solution[x-1, y]['visited'] and \
               solution[x-1, y]['value'] == value:
                fields.append({'x': x-1, 'y': y})

            # Check vertical right down
            if x < self.row and \
               y < self.col and \
               solution.get((x+1, y+1), None) and \
               not solution[x+1, y+1]['visited'] and \
               solution[x+1, y+1]['value'] == value:
                fields.append({'x': x+1, 'y': y+1})

            # Check vertical right up
            if x > 0 and \
               y < self.col and \
               solution.get((x-1, y+1), None) and \
               not solution[x-1, y+1]['visited'] and \
               solution[x-1, y+1]['value'] == value:
                fields.append({'x': x-1, 'y': y+1})

            # Check vertical left up
            if x > 0 and y > 0 and \
               solution.get((x-1, y-1), None) and \
               not solution[x-1, y-1]['visited'] and \
               solution[x-1, y-1]['value'] == value:
                fields.append({'x': x-1, 'y': y-1})

            # Check vertical left down
            if x < self.row and \
               y > 0 and \
               solution.get((x+1, y-1), None) and \
               not solution[x+1, y-1]['visited'] and \
               solution[x+1, y-1]['value'] == value:
                fields.append({'x': x+1, 'y': y-1})

    def checkNeighbour(self, sol=None):
        """Check if the constituency are all aside
        """
        solution = {}
        #self.count_check_neighbour += 1
        #print("Check neigh: {}".format(self.count_check_neighbour%100))
        var = self.variables
        for x in range(self.row):
            for y in range(self.col):
                for w in range(self.constituency):
                    if self.model.getSolVal(sol, var[x, y, w]) > EPS:
                        solution[x, y] = {'visited': False, 'value': w}

        if not solution:
            return {'solution': False}

        visited_constituency = [] # set()
        for x in range(self.row):
            for y in range(self.col):

                # Check if this value already is visited
                if not solution.get((x, y), None):
                    continue
                if solution[x, y]['visited']:
                    continue
                # Check if this constituency is in our list
                
                if solution[x, y]['value'] in visited_constituency:
                    try:
                        if len([i for i, x in enumerate(visited_constituency) if x == solution[x, y]['value']]) > 2:
                            self.logger.info("Value: {} was in set".format(solution[x, y]['value']))
                            return {'solution': False, 'x': x, 'y': y, 'w': solution[x, y]['value']}
                    except Exception:
                        return {'solution': False, 'x': x, 'y': y, 'w': solution[x, y]['value']}

                # Set visited flag for
                visited_constituency.append(solution[x, y]['value'])
                self.logger.info("Deep search from x: {}, y: {} for element {}".format(x,
                                                                                       y,
                                                                                       solution[x, y]['value']))

                with timer.Timer() as t:
                    self.deepSearch(solution, x, y)
                self.time_deepsearch.append(t.msecs)

                if len(self.time_deepsearch) == 100:
                    print("Avg deep search time: {}".format(np.mean(self.time_deepsearch)))
                    self.time_deepsearch = []

        return {'solution': True}

    def conscheck(self, constraints, solution, checkintegrality,
                  checklprows, printreason, completely):
        self.logger.info("Check one solution")
        self.logger.info("-"*20)
        with timer.Timer() as t:
            sol = self.checkNeighbour(solution)
        self.time_check_neighbour.append(t.msecs)

        if len(self.time_check_neighbour) == 100:
            print("Avg check neighbour time: {}".format(np.mean(self.time_check_neighbour)))
            self.time_check_neighbour = []

        if sol['solution']:
            self.logger.info("Solution seems OK")
            return {"result": SCIP_RESULT.FEASIBLE}
        else:
            self.logger.info("Solution is not OK")
            return {"result": SCIP_RESULT.INFEASIBLE}


    def consenfolp(self, constraints, n_useful_conss, sol_infeasible):
        self.logger.info("Check CONSENS")
        self.logger.info("="*20)
        with timer.Timer() as t:
            sol = self.checkNeighbour()
        self.time_check_neighbour.append(t.msecs)

        if len(self.time_check_neighbour) == 100:
            print("Avg check neighbour time: {}".format(np.mean(self.time_check_neighbour)))
            self.time_check_neighbour = []

        if sol['solution']:
            {"result": SCIP_RESULT.FEASIBLE}
        else:
            # Add cons to avoid using at this position [x,y,w] != 1
            # self.model.addCons(var[sol['x'], sol['y'], sol['w']] == 0)
            return {"result": SCIP_RESULT.CUTOFF}

    def conslock(self, constraint, nlockspos, nlocksneg):
        pass
        # sol = {}
        # var = self.variables
        # for x in range(self.row):
        #     out = ''
        #     for y in range(self.col):
        #         for w in range(self.constituency):
        #             if self.model.getSolVal(None, var[x, y, w]) > EPS:
        #                 sol[x, y] = w + 1
        #         out += "{:2} | ".format(sol.get((x, y), "--"))
        #     print(out)

        #pdb.set_trace()

        pass


    def conscopy(self):
        print("COPY")
        pass

    def consinitsol(self, constraints):
        pass
        

    def consenfops(self, constraints, nusefulconss, solinfeasible, objinfeasible):
        # The CONSENFOPS callback is similar to the CONSENFOLP callback, but deals with pseudo solutions instead of LP solutions. because numerical difficulties in the LP solving process were detected
        pass

    def consprop(self, constraints, nusefulconss, nmarkedconss, proptiming):
        print("consprop")
        pdb.set_trace()

    def consresprop(self):
        print("consresprop")
        pdb.set_trace()