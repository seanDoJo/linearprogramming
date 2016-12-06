from pulp import *
from bounds import time_constraints

"""

tfinley.net/software/pyglpk/discussion.html

"""

def solve(data):
    timeArray = []
    decisionArray = []
    edgeArray = []
    lp = LpProblem("value optimizer", LpMaximize)
    
    initialize(data, timeArray, decisionArray, edgeArray)

    addBudgetConstraint(data, decisionArray, lp)   
    
    
    # construction chain

def initialize(data, timeArray, decisionArray, edgeArray):
    # function to initialize the columns and rows of the problem
    place_data = data["place_data"]
    gdata = [ place_data[k]  for k in place_data ]
    gdata = [ item for row in gdata for item in row ]
    numberCols = len(data["distance_data"]) + 2*len(gdata)
    
    # define time variables for places
    for keyword in data["place_data"]:
        lb = time_constraints[keyword]
        for place in data["place_data"][keyword]:
            tVar = LpVariable("{}".format(place["name"]), lb, None, LpContinuous)
            tEntry = (tVar, keyword, place["price_level"])
            timeArray.append(tEntry)

            dVar = LpVariable("{}".format(place["name"]), 0, 1, LpBinary)
            dEntry = (dVar, keyword, place["price_level"])
            decisionArray.append(dEntry)
    
    for k in data["distance_data"]:
        frm, to = k
        dVar = LpVariable("({}, {})-Decision".format(frm, to), 0, 1, LpBinary)
        edgeArray.append(dVar)
            

    # define decision variables for places

def addObjectiveFunction(data, lp):
    # function to set the objective function

def addBudgetConstraint(data, decisonArray, lp):
    # function to add the budget constraint
    budget = data["user_data"]["budget"]
    lp += (sum(map(lambda (x, k, p): x*(p-budget), decisionArray)) <= 0)
            

def addPathConstraint(data, lp):
    # function to add the IN-OUT constraints

def addTimeConstraint(data, lp):
    # function to add the maximum time constraint

def addStrictConstraint(data, lp):
    # function to enforce a category of every kind

def addHomeConstraints(data, lp):
    # function to add constraints about the Home node

def addDecisionConstraints(data, lp):
    # function to add constraints defining decision variable behavior
