"""
Authors: Sean Donohoe

A flask server for interfacing the linear program with users
"""

from value_solver import solve
from data_collection import collectData
from flask import Flask, request, send_file, jsonify
from app import MyApp
from bounds import time_constraints

app = Flask(__name__)
mapp = None

@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.route('/getRoute/', methods=['GET', 'POST'])
def solveRoute():
    if request.method == "POST":
        d = {}

        keywords = []
        for keyword in time_constraints:
            kname = "{}-selected".format(keyword)
            if kname in request.form:
                keywords.append(keyword)
        d["keywords"] = keywords
        
        d["start_address"] = request.form["start_address"]

        d["radius"] = int(request.form["searchRadius"])

        d["budget"] = int(request.form["budget"])

        hour = int(request.form["userHour"])
        minute = int(request.form["userMinute"])

        d["time"] = (hour + minute)

        weights = {"HOME": 0}
        strictness = {}
        bounds = {"HOME": 0}
        for keyword in keywords:
            kname = "{}-multiplier".format(keyword)
            weights[keyword] = int(request.form[kname])

            kname = "{}-equality".format(keyword)
            equality = request.form[kname]
            if equality != "NONE":
                kname = "{}-strictness".format(keyword)
                value = int(request.form[kname])

                strictness[keyword] = (equality, value)

            kname = "{}-upperHour".format(keyword)
            upperHour = int(request.form[kname])
            kname = "{}-upperMinute".format(keyword)
            upperMinute = int(request.form[kname])
            bounds[keyword] = (upperHour + upperMinute)

        d["weights"] = weights
        d["strictness"] = strictness
        d["bounds"] = bounds

        print(d)

        data = collectData(d)
        print("DONE COLLECTING DATA")
        path_data = solve(data)

        return jsonify(**path_data)
    else:
        return "ERROR"

if __name__ == '__main__':
    mapp = MyApp()
    app.run(host='0.0.0.0', port=8000)
