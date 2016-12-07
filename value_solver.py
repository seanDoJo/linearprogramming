from pulp import *
from bounds import time_constraints

"""

tfinley.net/software/pyglpk/discussion.html

"""
var_mapping = {}

def solve(data):
    timeArray = []
    decisionArray = []
    edgeArray = []
    flowArray = []
    lp = LpProblem("value optimizer", LpMaximize)
    
    initialize(data, timeArray, decisionArray, edgeArray, flowArray)

    addBudgetConstraint(data, decisionArray, lp)   
   
    addPathConstraint(data, decisionArray, edgeArray, lp)

    addTimeConstraint(data, timeArray, edgeArray, lp)

    addHomeConstraints(data, timeArray, decisionArray, lp)

    addDecisionConstraints(data, timeArray, decisionArray, lp)

    addFlowOutgoing(data, flowArray, lp)

    addFlowConservation(data, flowArray, lp)

    addFlowDecision(data, flowArray, decisionArray, lp)

    addObjectiveFunction(data, timeArray, decisionArray, flowArray, lp)

    print(lp)
    
    status = lp.solve(GLPK(msg=0))
    print(LpStatus[status])

    print("Time Values:")
    for (x, k, p) in timeArray:
        print("\t{}: {} seconds".format(var_mapping[x.name], value(x)))

    print("Choice Values:")
    for (x, k, p) in decisionArray:
        print("\t{}: {}".format(var_mapping[x.name], value(x)))

    print("Edge Values:")
    for (x, t) in edgeArray:
        print("\t{}: {}".format(var_mapping[x.name], value(x)))

    print("Total: {}".format(value(lp.objective)))

def initialize(data, timeArray, decisionArray, edgeArray, flowArray):
    # function to initialize the columns and rows of the problem
    global var_mapping
    place_data = data["place_data"]
    gdata = [ place_data[k]  for k in place_data ]
    gdata = [ item for row in gdata for item in row ]
    numberCols = len(data["distance_data"]) + 2*len(gdata)
    
    # define time variables for places
    curr_int = 0
    for keyword in data["place_data"]:
        lb = time_constraints[keyword]
        ub = data["user_data"]["bounds"][keyword]
        for place in data["place_data"][keyword]:
            tVar = LpVariable("x{}".format(curr_int), lb, ub, LpContinuous)
            tEntry = (tVar, keyword, place["price_level"])
            timeArray.append(tEntry)
            var_mapping[tVar.name] = place["name"]
            curr_int += 1

            if place["name"] == "HOME":
                dVar = LpVariable("x{}".format(curr_int), 1, 1, LpInteger)
                print("HOME: {}".format(dVar.name))
            else:
                dVar = LpVariable("x{}".format(curr_int), 0, 1, LpInteger) 
            dEntry = (dVar, keyword, place["price_level"])
            decisionArray.append(dEntry)
            var_mapping[dVar.name] = place["name"]
            curr_int += 1

    for k in data["distance_data"]:
        frm, to = k
        dVar = LpVariable("x{}".format(curr_int), 0, 1, LpInteger)
        dEntry = (dVar, data["distance_data"][k])
        edgeArray.append(dEntry)
        var_mapping[dVar.name] = "{}, {}".format(frm, to)
        curr_int += 1

        fVar = LpVariable("x{}".format(curr_int), 0, 1, LpInteger)
        flowArray.append(fVar)
        var_mapping[fVar.name] = "{}, {}".format(frm, to)
        curr_int += 1
            

def addObjectiveFunction(data, timeArray, decisionArray, flowArray, lp):
    # function to set the objective function
    tuples = []
    for (x, k, p) in timeArray:
        for keyword in data["place_data"]:
            for place in data["place_data"][keyword]:
                if (var_mapping[x.name] == place["name"]):
                    tuples.append((x, place["rating"]))

    inBoundHome = []
    for x in flowArray:
        to = var_mapping[x.name].split(",")[1].strip()
        if (to == "HOME"):
            inBoundHome.append(x)

    lp += sum(map(lambda x: x[0]*x[1], tuples)) + -1*sum(map(lambda x: x[0], decisionArray)) + sum(inBoundHome)

def addBudgetConstraint(data, decisionArray, lp):
    # function to add the budget constraint
    budget = data["user_data"]["budget"]
    lp += (sum(map(lambda x: x[0]*(x[2]-budget), decisionArray)) <= 0)
            

def addPathConstraint(data, decisionArray, edgeArray, lp):
    # function to add the IN-OUT constraints
    for (x, k, p) in decisionArray:
        nodeName = var_mapping[x.name]
        inBound = []
        outBound = []

        for (y, t) in edgeArray:
            frm, to = var_mapping[y.name].split(',')
            if nodeName == frm.strip():
                outBound.append(y)
            elif nodeName == to.strip():
                inBound.append(y)
        
        # inbound constraint
        lp += (sum(inBound) - x == 0)
        
        # outbound constraint
        lp += (sum(outBound) - x == 0)

def addTimeConstraint(data, timeArray, edgeArray, lp):
    # function to add the maximum time constraint
    p1 = sum(map(lambda e: e[0], timeArray))
    p2 = sum(map(lambda e: e[0]*e[1], edgeArray))
    lp += (p1 + p2 - data["user_data"]["time"]) <= 0
     
    

def addStrictConstraint(data, lp):
    # function to enforce a category of every kind
    pass

def addHomeConstraints(data, timeArray, decisionArray, lp):
    # function to add constraints about the Home node
    home_time = None
    home_d = None

    for (x, k, p) in timeArray:
        if (var_mapping[x.name] == "HOME"):
            home_time = x
            break

    for (x, k, p) in decisionArray:
        if (var_mapping[x.name] == "HOME"):
            home_d = x
            break
    
    lp += home_time == 0
    lp += home_d >= 1
    lp += home_d <= 1
        

def addDecisionConstraints(data, timeArray, decisionArray, lp):
    # function to add constraints defining decision variable behavior
    tuples = []
    for (x, k, p) in timeArray:
        for (y, l, q) in decisionArray:
            if (var_mapping[x.name] == var_mapping[y.name]):
                tuples.append((x, y))
                break

    for (x, y) in tuples:
        lp += y*x.lowBound - x <= 0
        lp += x - y*x.upBound <= 0

def addFlowOutgoing(data, flowArray, lp):
    homeVars = []
    for x in flowArray:
        frm = var_mapping[x.name].split(",")[0].strip()
        if (frm == "HOME"):
            homeVars.append(x)
    
    lp += (sum(homeVars) == 1)

def addFlowConservation(data, flowArray, lp):
    place_data = data["place_data"]
    gdata = [ place_data[k]  for k in place_data ]
    gdata = [ item for row in gdata for item in row ]

    for place in gdata:
        nodeName = place["name"]

        inBound = []
        outBound = []

        for x in flowArray:
            frm = var_mapping[x.name].split(",")[0].strip()
            to = var_mapping[x.name].split(",")[1].strip()
            
            if frm == nodeName:
                outBound.append(x)
            elif to == nodeName:
                inBound.append(x)
        
        lp += (sum(inBound) - sum(outBound)) == 0

def addFlowDecision(data, flowArray, decisionArray, lp):
    tuples = []    

    for x in flowArray:
        fName = var_mapping[x.name]
        for (y, k, p) in decisionArray:
            if fName == var_mapping[y.name]:
                tuples.add((x, y))
                break

    for (x, y) in tuples:
        lp += (x - y == 0)
