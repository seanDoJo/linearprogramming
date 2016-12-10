from value_solver import solve
from data_collection import collectData




test_data = {
    'start_address': '950 28th St, Boulder, CO',
    'keywords': ['restaurant', 'cafe', 'bar'],
    'radius': 1000,
#    'radius': 3000,
    'bounds': {'restaurant': 3600, 'cafe': 1800, 'bar': 1800, 'HOME': 0},
    'budget': 2,
    'time': 14400,
    'weights': {'restaurant': 3, 'cafe': 2, 'bar': 1, 'HOME': 0},
    'strictness': {},
}

data = collectData(test_data)
print("DONE COLLECTING DATA")
solve(data)
