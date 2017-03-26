#!/usr/bin/env python3

from pyscipopt import Model, Heur, SCIP_RESULT
import pdb
import logging



EPS = 1.e-6
class ElectionHeuer(Heur):

    def __init__(self, variables, logger=None):
        self.variables = variables
        self.logger = logger or logging.getLogger(__name__)


    def heurexec(self, heurtiming, nodeinfeasible):

        sol = self.model.createSol(self)
        vars = self.model.getVars()
        pdb.set_trace()

        self.model.setSolVal(sol, vars[0], 5.0)
        self.model.setSolVal(sol, vars[1], 0.0)

        accepted = self.model.trySol(sol)

        if accepted:
            return {"result": SCIP_RESULT.FOUNDSOL}
        else:
            return {"result": SCIP_RESULT.DIDNOTFIND}
