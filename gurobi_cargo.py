#!/usr/bin/python

# Copyright 2018, Gurobi Optimization, LLC


from gurobipy import *


# Create a new model
m = Model("cargo")

# Create variables
tf1 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="tf1")
tf2 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="tf2")
tf3 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="tf3")
tf4 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="tf4")
tm1 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="tm1")
tm2 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="tm2")
tm3 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="tm3")
tm4 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="tm4")
tb1 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="tb1")
tb2 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="tb2")
tb3 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="tb3")
tb4 = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="tb4")
w = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="w")


# Set objective
m.setObjective(280*tf1+280*tm1+280*tb1+360*tf2+360*tm2+360*tb2+320*tf3+320*tm3+320*tb3+250*tf4+250*tm4+250*tb4, GRB.MAXIMIZE)

# Add constraint: x + 2 y + 3 z <= 4
m.addConstr(tf1 + tf2 + tf3 + tf4 <= 12, "c0")
m.addConstr(tm1 + tm2 + tm3 + tm4 <= 18, "c1")
m.addConstr(tb1 + tb2 + tb3 + tb4 <= 10, "c2")
m.addConstr(500 * tf1 + 700 * tf2 + 600 * tf3 + 400 * tf4 <= 7000, "c3")
m.addConstr(500 * tm1 + 700 * tm2 + 600 * tm3 + 400 * tm4 <= 9000, "c4")
m.addConstr(500 * tb1 + 700 * tb2 + 600 * tb3 + 400 * tb4 <= 5000, "c5")
m.addConstr(tf1 + tm1 + tb1 <= 20, "c6")
m.addConstr(tf2 + tm2 + tb2 <= 16, "c7")
m.addConstr(tf3 + tm3 + tb3 <= 25, "c8")
m.addConstr(tf4 + tm4 + tb4 <= 13, "c9")
m.addConstr(tf1 + tf2 + tf3 + tf4 + tm1 + tm2 + tm3 + tm4 + tb1 + tb2 + tb3 + tb4 - w <= 0, "c10")
m.addConstr(10*tf1+10*tf2+10*tf3+10*tf4 <= 3 * w, "c11")
m.addConstr(20 * tm1 + 20 * tm2 + 20 * tm3 + 20 * tm4 <= 9 * w, "c12")
m.addConstr(4 * tb1 + 4 * tb2 + 4 * tb3 + 4 * tb4 <=  w, "c13")
m.addConstr(tf1 + tf2 + tf3 + tf4 + tm1 + tm2 + tm3 + tm4 + tb1 + tb2 + tb3 + tb4 - w >= 0, "c14")
m.addConstr(10*tf1+10*tf2+10*tf3+10*tf4 >= 3 * w, "c15")
m.addConstr(20 * tm1 + 20 * tm2 + 20 * tm3 + 20 * tm4 >= 9 * w, "c16")
m.addConstr(4 * tb1 + 4 * tb2 + 4 * tb3 + 4 * tb4 >=  w, "c17")


# Add constraint: x + y >= 1

m.optimize()

for v in m.getVars():
    print('%s %g' % (v.varName, v.x))

print('Obj: %g' % m.objVal)

