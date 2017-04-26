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
class CrosswordsHdlr(Conshdlr):

    def __init__(self, variables, row=10, col=10, logger=None):
        self.row = row
        self.col = col
        self.variables = variables
        self.logger = logger or logging.getLogger(__name__)


    def conscheck(self, constraints, solution, checkintegrality,
                  checklprows, printreason, completely):
        return {"result": SCIP_RESULT.FEASIBLE}

    def consenfolp(self, constraints, n_useful_conss, sol_infeasible):
        return {"result": SCIP_RESULT.FEASIBLE}


    def conslock(self, constraint, nlockspos, nlocksneg):
        pass


    def propagate_cons(cons):
        pass

    def consprop(self, constraints, nusefulconss, nmarkedconss, proptiming):
        # pdb.set_trace()
        return {"result": SCIP_RESULT.DIDNOTFIND}
