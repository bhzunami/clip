#!/usr/bin/env python3

import logging
import time
import pdb
import random
import math
from pyscipopt import Model, quicksum, Conshdlr, SCIP_RESULT, SCIP_PARAMSETTING, SCIP_HEURTIMING
from electionHandler import ElectionHdlr
from election_heuer import ElectionHeuer

#logging.basicConfig(level=logging.INFO)

WORDS = ['HALLO', 'NAME', 'OBEN', 'NACHT']

def solve(row=10, col=10):
    model = Model("Election")
    # Variabeln für die einzelnen stimmen pro quadrat definieren
    for x in range(row):
        for y in range(col):
            for l in range(27):  # Alle Wörter plus kein
                s[x, y, l] = model.addVar(vtype="B", name="{}-{}-{}".format(x, y, l))

    # CONSTRAINTS
    # - - - - - - - - - - - - - - - - - -
   
    model.hideOutput()
    model.optimize()

    
    del model # consfree get called
    return True


def main():
    count = 4
    solve(row=count, col=count, constituency=count)

if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    # create a file handler
    handler = logging.FileHandler('/tmp/election.log', mode='w')
    handler.setLevel(logging.DEBUG)

    # create a logging format
    formatter = logging.Formatter('%(name)s: [%(levelname)s] - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)
    logger.info("Start Problem")
    main()
