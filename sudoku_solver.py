#!/usr/bin/env python3

import sys
from pyscipopt import Model, quicksum
import pdb

sudoku = [2, 0, 1, 5, 0, 0, 0, 0, 7,
          8, 7, 0, 0, 0, 3, 2, 0, 0,
          6, 0, 0, 2, 0, 0, 0, 0, 0,
          0, 3, 0, 4, 0, 0, 0, 0, 0,
          1, 0, 0, 0, 0, 0, 0, 0, 4,
          0, 0, 0, 0, 0, 1, 0, 3, 0,
          0, 0, 0, 0, 0, 8, 0, 0, 3,
          0, 0, 2, 1, 0, 0, 0, 9, 5,
          9, 0, 0, 0, 0, 4, 7, 0, 1]

sudoku = [0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 8, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0]

sudoku3 = [5, 3, 0, 0, 7, 0, 0, 0, 0,
           6, 0, 0, 1, 9, 5, 0, 0, 0,
           0, 9, 8, 0, 0, 0, 0, 6, 0,
           8, 0, 0, 0, 6, 0, 0, 0, 3,
           4, 0, 0, 8, 0, 3, 0, 0, 1,
           7, 0, 0, 0, 2, 0, 0, 0, 6,
           0, 6, 0, 0, 0, 0, 2, 8, 0,
           0, 0, 0, 4, 1, 9, 0, 0, 5,
           0, 0, 0, 0, 8, 0, 0, 7, 9]

# Create vars
model = Model("Sudoku")

s = {}
for x in range(9):
    for y in range(9):
        for z in range(9):
            s[x, y, z] = model.addVar(vtype="B", name="{}-{}-{}".format(x, y, z))

# set initail Value 
for x in range(9):
    for y in range(9):
        if sudoku[9*x +y] != 0:  # predefined number
            # model.setBoolParam(s[x, y, sudoku[9*x +y]-1], "1")
            model.addCons(s[x, y, sudoku[9*x +y]-1] == 1)

# only one value per field
for x in range(9):
    for y in range(9):
        model.addCons(quicksum(s[x, y, z] for z in range(9)) == 1)  # only one number
        model.addCons(quicksum(s[x, z, y] for z in range(9)) == 1)  # only in one col
        model.addCons(quicksum(s[z, x, y] for z in range(9)) == 1)  # only in one row

# Row
#for x in range(9):
#    for z in range(9):
#        model.addCons(quicksum(s[x, y, z] for y in range(9)) == 1)
#        model.addCons(quicksum(s[y, x, z] for y in range(9)) == 1)

# Column
#for y in range(9):
#    for z in range(9):
#        model.addCons(quicksum(s[x, y, z] for x in range(9)) == 1)

# Not same in quader
for row in range(3):
    for col in range(3):
        for z in range(9):
            el = []
            for i in range(3):
                for j in range(3):
                    el.append(s[i+row*3, j+col*3, z])
        # print("Elements: {}".format(el))
        model.addCons(quicksum(el) == 1)

model.hideOutput()
model.optimize()

if model.getStatus() != 'optimal':
    print('No solution found!')
    sys.exit(1)

solution = {}
for x in range(9):
    out = ''
    for y in range(9):
        for k in range(9):
            # print("X: {}, Y: {}, K: {}, model {}".format(x, y, k, model.getVal(s[x, y, k])))
            if model.getVal(s[x, y, k]) >= 0.5:
                 solution[x, y] = k + 1
        if y % 3 == 0:
             out += '| '
        out += str(solution.get((x, y), 'X')) + ' '
    if x % 3 == 0:
         print("="*24)
    print(out)
print("="*24)
    