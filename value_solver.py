from pulp import *
from bounds import time_constraints

"""

tfinley.net/software/pyglpk/discussion.html

"""
var_mapping = {}

def cascade(data):
    timeArray = []
    decisionArray = []
    edgeArray = []

    lp = LpProblem("value optimizer", LpMaximize)
    
    initialize(data, timeArray, decisionArray, edgeArray)

    addBudgetConstraint(data, decisionArray, lp)   
   
    addPathConstraint(data, decisionArray, edgeArray, lp)

    addTimeConstraint(data, timeArray, edgeArray, lp)

    addHomeConstraints(data, timeArray, decisionArray, lp)

    addDecisionConstraints(data, timeArray, decisionArray, lp) 

    addObjectiveFunction(data, timeArray, decisionArray, lp)

    return (timeArray, decisionArray, edgeArray, lp)

def solve(data):
    
    (timeArray, decisionArray, edgeArray, lp) = cascade(data) 
    
    status = lp.solve(GLPK(msg=0))

    
    subtours = collectSubtours(edgeArray)
    while len(subtours) > 1:
        for subtour in subtours:
            addSubtourConstraint(data, subtour, edgeArray, lp)
        status = lp.solve(GLPK(msg=0))
        subtours = collectSubtours(edgeArray)

    print(LpStatus[status])
    place_data = data["place_data"]
    gdata = [ place_data[k]  for k in place_data ]
    gdata = [ item for row in gdata for item in row ]
    for (x, k, p) in timeArray:
        lastItem = None
        for item in gdata:
            if item["name"] == var_mapping[x.name]:
                lastItem = item
                break
        print("\t{}: {}, {}, {}".format(var_mapping[x.name], value(x), lastItem["rating"], lastItem["price_level"]))

    chosenEdges = []
    
    for (e, t) in edgeArray:
        if value(e):
            frm = var_mapping[e.name].split(",")[0].strip()
            to = var_mapping[e.name].split(",")[1].strip()
            chosenEdges.append((frm, to))

    last = ""
    for x in chosenEdges:
        if x[0] == "HOME":
            last = x[1]
            chosenEdges.remove(x)
            break

    if len(chosenEdges) > 0:
        print("HOME")
        while last != "HOME":
            print(last) 
            for x in chosenEdges:
                if x[0] == last:
                    last = x[1]
                    chosenEdges.remove(x)
                    break

        print("HOME")
    print(chosenEdges)
    print(len(chosenEdges))
            
    print("Total: {}".format(value(lp.objective)))

def initialize(data, timeArray, decisionArray, edgeArray):
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
            tVar = LpVariable("x{}".format(curr_int), 0, float(ub), LpContinuous)
            tEntry = (tVar, keyword, place["price_level"])
            timeArray.append(tEntry)
            var_mapping[tVar.name] = place["name"]
            curr_int += 1

            if place["name"] == "HOME":
                dVar = LpVariable("x{}".format(curr_int), 1, 1, LpBinary)
            else:
                dVar = LpVariable("x{}".format(curr_int), 0, 1, LpBinary) 
            dEntry = (dVar, keyword, place["price_level"])
            decisionArray.append(dEntry)
            var_mapping[dVar.name] = place["name"]
            curr_int += 1

    for k in data["distance_data"]:
        frm, to = k
        dVar = LpVariable("x{}".format(curr_int), 0, 1, LpBinary)
        dEntry = (dVar, data["distance_data"][k])
        edgeArray.append(dEntry)
        var_mapping[dVar.name] = "{}, {}".format(frm, to)
        curr_int += 1

def addObjectiveFunction(data, timeArray, decisionArray, lp):
    # function to set the objective function
    tuples = []
    for (x, k, p) in timeArray:
        for keyword in data["place_data"]:
            for place in data["place_data"][keyword]:
                if (var_mapping[x.name] == place["name"]):
                    tuples.append((x, place["rating"]))

    lp += sum(map(lambda x: x[0]*x[1], tuples)) + -1*sum(map(lambda x: x[0], decisionArray))

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
    lp += home_d == 1

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

def collectSubtours(edgeArray):
    tours = []
    edgeCopy = [ k for k in edgeArray if value(k[0])] 
   
    for edge in edgeCopy:

        original = var_mapping[edge[0].name].split(",")[0].strip()

        last = var_mapping[edge[0].name].split(",")[1].strip()

        inTour = False
        for subtour in tours:
            for node in subtour:
                if original == node or last == node:
                    inTour = True
                    break
            if inTour:
                break
                
        if inTour:
            continue

        subtour = []         

        subtour.append(original)

        while last != original:
            seen = False
            for e in edgeCopy:
                frm = var_mapping[e[0].name].split(",")[0].strip()
                to = var_mapping[e[0].name].split(",")[1].strip()

                if frm == last:
                    subtour.append(last)
                    last = to
                    seen = True
                    break
            if not seen:
                print(tours)
                print(subtour)
                exit(0)

        tours.append(subtour)
    return tours

def addSubtourConstraint(data, subtour, edgeArray, lp):    
    inBound = []
    outBound = []
    for nodeName in subtour:
        for (x, t) in edgeArray:
            frm = var_mapping[x.name].split(",")[0].strip()
            to = var_mapping[x.name].split(",")[1].strip()
        
            if to == nodeName and frm not in subtour:
                inBound.append(x)
            elif frm == nodeName and to not in subtour:
                outBound.append(x)
    nconst = sum(inBound) + sum(outBound) >= 2
    lp += nconst
