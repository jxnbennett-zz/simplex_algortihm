#!/usr/bin/python

# Copyright 2018, Gurobi Optimization, LLC


from gurobipy import *


# Create a new model
m = Model("radio")

# Create variables
r1 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="r1")
r2 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="r2")
r3 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="r3")
r4 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="r4")
wr1 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="wr1")
wr2 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="wr2")
wr3 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="wr3")
wr4 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="wr4")
wt1 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="wt1")
wt2 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="wt2")
wt3 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="wt3")
wt4 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="wt4")
t1 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="t1")
t2 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="t2")
t3 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="t3")


# Set objective
m.setObjective(15*r1+13*r2+11*r3+9*r4-200*wr1-200*wt1-200*wr2-200*wt2-200*wr3-200*wt3-200*wr4-200*wt4-100*t1-100*t2-100*t3, GRB.MAXIMIZE)

# Add constraint: x + 2 y + 3 z <= 4
m.addConstr(r1-50*wr1 >= 0, "c0")
m.addConstr(r1-50*wr1 <= 0, "c1")
m.addConstr(r2-50*wr2 >= 0, "c2")
m.addConstr(r2-50*wr2 <= 0, "c3")
m.addConstr(r3-50*wr3 >= 0, "c4")
m.addConstr(r3-50*wr3 <= 0, "c5")
m.addConstr(r4-50*wr4 >= 0, "c6")
m.addConstr(r4-50*wr4 <= 0, "c7")
m.addConstr(wr1+wt1 >= 40, "c8")
m.addConstr(wr1+wt1 <= 40, "c9")
m.addConstr(wr2+wt2-wr1-4*wt1 >= 0, "c10")
m.addConstr(wr2+wt2-wr1-4*wt1 <= 0, "c11")
m.addConstr(wr3+wt3-wr2-4*wt2 >= 0, "c12")
m.addConstr(wr3+wt3-wr2-4*wt2 <= 0, "c13")
m.addConstr(wr4+wt4-wr3-4*wt3 >= 0, "c14")
m.addConstr(wr4+wt4-wr3-4*wt3 <= 0, "c15")
m.addConstr(t1-3*wt1 >= 0, "c16")
m.addConstr(t1-3*wt1 <= 0, "c17")
m.addConstr(t2-3*wt2 >= 0, "c18")
m.addConstr(t2-3*wt2 <= 0, "c19")
m.addConstr(t3-3*wt3 >= 0, "c20")
m.addConstr(t3-3*wt3 <= 0, "c21")
m.addConstr(r1+r2+r3+r4 >= 21475, "c22")
m.addConstr(r1+r2+r3+r4 <= 21475, "c23")

m.optimize()

for v in m.getVars():
    print('%s %g' % (v.varName, v.x))

print('Obj: %g' % m.objVal)
