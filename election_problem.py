#!/usr/bin/env python3

import sys
from pyscipopt import Model, quicksum
import pdb
import random

def generate_votes(row=10, col=10):
    votes = []
    v = []

    for x in range(row):
        for y in range(col):
            democrats = random.randint(0, 50)
            republicans = random.randint(0, 50) * 3
            votes += [1] if democrats > republicans else [0]
            v[x,y] = {'d': democrats, 'r': republicans}
    return votes


def main():
    model = Model("Election")
    row = 10
    col = 10
    constituency = 10
    s = {}
    w = {}
    votes = generate_votes(row, col)

    # Gewinner variabeln für die 10 Wahlbezirke
    for i in range(constituency):
        w[i] = model.addVar(vtype="I", name="win_w{}".format(i))

    # Variabeln für die einzelnen stimmen pro quadrat definieren
    for x in range(row):
        for y in range(col):
            for w in range(constituency):
                s[x, y, w] = model.addVar(vtype="B", name="{}-{}-{}".format(x, y, w))

    # Nur in einem Bezirk
    for x in range(row):
        for y in range(col):
            model.addCons(quicksum(s[x, y, w] for w in range(constituency)) == 1)  # Nur 1 Bezirk

    # Nicht mehr als 10 quadrate pro Wahlbezirk
    for w in range(constituency):
        model.addCons(quicksum(s[x, y, w] for x in range(col) for y in range(row)) = 10, name="Bezirk_{}".format(w))

    # Es gibt eine neue Variable für jedes W[0...9] für demokraten und für Republikaner
    # In diesem W summieren wir die Werte der Stimmen auf. Somit haben wir 
    # ein wd_0, wd_1, wd_2 mit allen stimmen für diesen wahlbezirk 
    # Diese wd und wr werden wir nachher mit einem IF abfühlen

    # Stimme im W0_d = quicksum(s[x, y, 0] * v[0]{d}  for x in range(col) for y in range(row)
    # w0_r = quicksum(s[x, y, 0] * v[0]{r}  for x in range(col) for y in range(row)
    # s[x, y, 0] * v[0]{d} 

    # Hier wird der gewinner Festgelegt wenn demokraten höher sind, dann wird ein 1 gemacht und ansonsten ein 0
    # Diese Variabel muss maximiert werden.
    # 1 neue model.addVar(vtype="B", name="demo_win_w0")
    # Diese Variable wird gesetzt: Diese Var ist 1 wen w0_d grösser ist als w0_r und ansonsten 0


    # Todo:
    # Bedingung: Welcher Wahlbezirk gewinnt
    # 10 quadrate = 1 Wahlbezirk

    for w in range(constituency):
        for i in [(x, y) for x in range(col) for y in range(row)]:
            if s[i[0], i[1], w] * v[i[0],i[1]]['d'] > s[i[0], i[1], w] * v[i[0],i[1]]['r']
        model.setObjective(quicksum(s[x, y, w]*v[x,y] for x in range(col) for y in range(row)), "maximize")

    # Total Democrats: w3 = total_d*1 + total_r
    # model.setObjective(quicksum(demo_win_w0[i] for i in range(10)), "maximize")

    model.hideOutput()
    model.optimize()

    if model.getStatus() != 'optimal':
        print('No solution found!') 
        sys.exit(1)
    print("Solution found")

    solution = {}
    for x in range(row):
        out = ''
        for y in range(col):
            for w in range(10):
                if model.getVal(s[x, y, w]) >= 0.5:
                    # print(w+1)
                    solution[x, y] = w + 1
            out += str(solution[x, y]) + ' '
        print(out)


# Create vars
if __name__ == "__main__":
    main()
