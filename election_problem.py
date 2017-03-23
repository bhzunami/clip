#!/usr/bin/env python3

import sys
from pyscipopt import Model, quicksum
import pdb
import random

def generate_votes(row=10, col=10):
    votes = {}

    for x in range(row):
        for y in range(col):
            democrats = random.randint(0, 50)
            republicans = random.randint(0, 50) * 3
            votes[x, y] = {'d': democrats, 'r': republicans}
    return votes


def main():
    model = Model("Election")
    row = 10
    col = 10
    constituency = 10
    s = {}
    wd = {}
    wr = {}
    winner = {}
    votes = generate_votes(row, col)

    v = {}
    for x in range(row):
        out = ''
        for y in range(col):
            out += "{}  |  ".format(votes[x, y])
        #print(out)


    # Gewinner variabeln für die 10 Wahlbezirke
    for i in range(constituency):
        # Anzahl Stimmen von Demokraten in diesem Wahlbezirk
        wd[i] = model.addVar(vtype="I", name="wd{}".format(i))

        # Anzahl Stimmen von Republikaner in diesem Wahlbezirk
        wr[i] = model.addVar(vtype="I", name="wr{}".format(i))

        # 1 wenn Demokraten gewinnen, 0 wenn Republikaner gewinnen
        winner[i] = model.addVar(vtype="B", name="winner{}".format(i))

    # Variabeln für die einzelnen stimmen pro quadrat definieren
    for x in range(row):
        for y in range(col):
            for w in range(constituency):
                s[x, y, w] = model.addVar(vtype="B", name="{}-{}-{}".format(x, y, w))

    # Jeder Staat nur in einem Bezirk
    for x in range(row):
        for y in range(col):
            model.addCons(quicksum(s[x, y, w] for w in range(constituency)) == 1)  # Nur 1 Bezirk

    # Nicht mehr als 10 quadrate pro Wahlbezirk
    for w in range(constituency):
        model.addCons(quicksum(s[x, y, w] for x in range(col) for y in range(row)) == 10,
                      name="Bezirk_{}".format(w))

    # Es gibt eine neue Variable für jedes Wd[0...9] für demokraten und wr[0...9] für Republikaner
    # In diesem W summieren wir die Werte der Stimmen auf. Somit haben wir
    # ein wd_0, wd_1, wd_2 mit allen stimmen für diesen wahlbezirk
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
    for w in range(constituency):
        model.addCons(wd[w] - wr[w] <= 150 * winner[w])
        model.addCons(winner[w] <= (wd[w] - wr[w]) * winner[w])

    model.setObjective(quicksum(winner[w] for i in range(10)), "maximize")
    # Total Democrats: w3 = total_d*1 + total_r
    # model.setObjective(quicksum(demo_win_w0[i] for i in range(10)), "maximize")

    model.hideOutput()
    model.optimize()

    if model.getStatus() != 'optimal':
        print('No solution found!') 
        sys.exit(1)
    print("Solution found")

    solution = {}
    ww = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}, 10: {}}
    for x in range(row):
        out = ''
        for y in range(col):
            for w in range(10):
                if model.getVal(s[x, y, w]) >= 0.5:
                    solution[x, y] = w + 1

                    if 'd' not in ww[w+1]:
                        ww[w+1]['d'] = 0
                    if 'r' not in ww[w+1]:
                        ww[w+1]['r'] = 0
                    ww[w+1]['d'] += votes[x, y]['d']
                    ww[w+1]['r'] += votes[x, y]['r']

            out += "{} ({}/{}) | ".format(solution[x, y], ww[solution[x, y]]['d'], ww[solution[x, y]]['r'])
        print(out)


# Create vars
if __name__ == "__main__":
    main()
