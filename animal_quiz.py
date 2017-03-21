from pyscipopt import Model

model = Model("Animal quiz")

x = model.addVar(vtype="I", name="octopus")
y = model.addVar(vtype="I", name="turtel")
z = model.addVar(vtype="I", name="bird")

model.addCons(x + y + z == 32, name="Heads")
model.addCons(8*x +4*y+2*z == 80, name="Legs")

model.setObjective(x+y, "minimize")

model.hideOutput()
model.optimize()

print("Optimal value:", model.getObjVal())
print((x.name, y.name, z.name), " = ", (model.getVal(x), model.getVal(y), model.getVal(z)))
