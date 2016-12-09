from value_solver import solve
from data_collection import collectData




test_data = {
    'start_address': '950 28th St, Boulder, CO',
    'keywords': ['restaurant', 'cafe', 'bar'],
    'radius': 1200,
#    'radius': 3000,
    'bounds': {'restaurant': 3600, 'cafe': 1800, 'bar': 1800, 'HOME': 0},
    'budget': 4,
    'time': 9000,
}

data = collectData(test_data)
print("DONE COLLECTING DATA")
solve(data)
