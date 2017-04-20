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

def generate_votes(row=10, col=10, multiplier=3):
    votes = {}
    sum_demo = 0
    sum_repu = 0
    random.seed(0)
    for x in range(row):
        for y in range(col):
            democrats = random.randint(100, 5000)
            republicans = random.randint(100, 5000) * multiplier
            sum_demo += democrats
            sum_repu += republicans
            votes[x, y] = {'d': democrats*0.01, 'r': republicans*0.01}
    print("Democrats total: {} votes, Republicans total: {} votes".format(sum_demo, sum_repu))
    return votes


def solve(row=10, col=10, constituency=10):
    model = Model("Election")
    s = {}       # Stimme
    wd = {}      # Gewinner democ
    wr = {}      # Gewinner repub
    winner = {}  # Gewinner Wahlbezirk
    votes = generate_votes(row, col, multiplier=1)

    # Display Votes
    for x in range(row):
        out = ''
        for y in range(col):
            out += "{:2}/{:2} | ".format(votes[x, y]['d'], votes[x, y]['r'])
        print(out)

    heuristic = ElectionHeuer(s, logger=logger)
    # includeHeur(heur, name, desc, dispatcher, priority, freq)
    # model.includeHeur(heuristic, "PyHeur", "custom heuristic implemented in python", "Y",
    #                   timingmask=SCIP_HEURTIMING.BEFORENODE)
    # model.setPresolve(SCIP_PARAMSETTING.OFF)

    # Gewinner variabeln für die 10 Wahlbezirke
    for i in range(constituency):
        # Anzahl Stimmen von Demokraten in diesem Wahlbezirk
        wd[i] = model.addVar(vtype="C", name="wd{}".format(i))

        # Anzahl Stimmen von Republikaner in diesem Wahlbezirk
        wr[i] = model.addVar(vtype="C", name="wr{}".format(i))

        # 1 wenn Demokraten gewinnen, 0 wenn Republikaner gewinnen
        winner[i] = model.addVar(vtype="B", name="winner{}".format(i))

    # Variabeln für die einzelnen stimmen pro quadrat definieren
    for x in range(row):
        for y in range(col):
            for w in range(constituency):
                s[x, y, w] = model.addVar(vtype="B", name="{}-{}-{}".format(x, y, w))

    # CONSTRAINTS
    # - - - - - - - - - - - - - - - - - -
    # Jeder Staat nur in einem Bezirk
    for x in range(row):
        for y in range(col):
            model.addCons(quicksum(s[x, y, w] for w in range(constituency)) == 1)  # Nur 1 Bezirk

    # Nicht mehr als 10 quadrate pro Wahlbezirk
    for w in range(constituency):
        model.addCons(quicksum(s[x, y, w] for x in range(col) for y in range(row)) == row,
                      name="Bezirk_{}".format(w))

    # Es gibt eine neue Variable für jedes Wd[0...9] für demokraten und wr[0...9] für Republikaner
    # In diesem W summieren wir die Werte der Stimmen auf. Somit haben wir
    # ein wd_0, wd_1, wd_2 mit allen Stimmen für diesen Wahlbezirk
    # Stimme im W0_d = quicksum(s[x, y, 0] * v[0]{d}  for x in range(col) for y in range(row)
    for w in range(constituency):
        model.addCons(wd[w] == quicksum(s[x, y, w] * votes[x, y]['d']  for x in range(col) for y in range(row)))
        model.addCons(wr[w] == quicksum(s[x, y, w] * votes[x, y]['r']  for x in range(col) for y in range(row)))
        # wd[w] = quicksum(s[x, y, w] * votes[x,y]['d']  for x in range(col) for y in range(row))
        # wr[w] = quicksum(s[x, y, w] * votes[x,y]['r']  for x in range(col) for y in range(row))

    # w0_r = quicksum(s[x, y, 0] * v[0]{r}  for x in range(col) for y in range(row)
    # s[x, y, 0] * v[0]{d}
    # Hier wird der gewinner Festgelegt wenn demokraten höher sind,
    # dann wird ein 1 gemacht und ansonsten ein 0
    # Diese Variabelen müssen maximiert werden.
    # 1 neue model.addVar(vtype="B", name="demo_win_w0")
    # Diese Variable wird gesetzt: Diese Var ist 1 wen w0_d grösser ist als w0_r und ansonsten 0
    bimM = 20 * constituency * 2
    for w in range(constituency):
        model.addCons(wd[w] - wr[w] <= 10000 * winner[w])
        model.addCons(winner[w] <= (wd[w] - wr[w]) * winner[w])
        #model.addCons(wd[w] + 10000 * (1 - winner[w]) >= wr[w])
        #model.addCons(wd[w] - 10000 * winner[w] <= wr[w])

        if w > 0:
            model.addCons(wd[w-1] >= wd[w])
            # model.addCons(wr[w-1] <= wr[w])
        # wd[w] < wd[w-1] symetrie breaking constraings

    # model.addCons(quicksum(winner[w] for w in range(constituency)) >= 6)

    conshdlr = ElectionHdlr(s, row=row, col=col, cons=constituency, logger=logger)
    model.includeConshdlr(conshdlr, "election",
                          "Election", chckpriority=-10000,
                          needscons=False, propfreq=50)  # 
    model.setBoolParam("misc/allowdualreds", False)

    #cons1 = model.createCons(conshdlr, "election")
    #conshdlr.createData(cons1, 10, "cons1_anothername")
    #model.addPyCons(cons1)


    model.setObjective(quicksum(winner[w] for w in range(constituency)), "maximize")

    model.hideOutput()
    model.optimize()

    if model.getStatus() != 'optimal':
        print('No solution found!')
        return False

    print("Solution found")
    solution = {}
    ww = {}
    for w in range(constituency):
        ww[w+1] = {'d': 0, 'r': 0}

    for x in range(row):
        out = ''
        for y in range(col):
            for w in range(constituency):
                if model.getVal(s[x, y, w]) >= 0.8:
                    solution[x, y] = w + 1
                    ww[w+1]['d'] += votes[x, y]['d']
                    ww[w+1]['r'] += votes[x, y]['r']
            out += "{:2} | ".format(solution[x, y])
        print(out)

    print()
    for w in ww.keys():
        winner = 'D' if ww[w]['d'] >= ww[w]['r'] else 'R'
        print('{:2}: {} (Demo: {}, Repu: {})'.format(w, winner, ww[w]['d'], ww[w]['r']))

    del model # consfree get called
    return True


    # for x in range(row):
    #     out = ''
    #     for y in range(col):
    #         out += "{} | ".format(votes[x,y])
    #     print(out)

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
