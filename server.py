from value_solver import solve
from data_collection import collectData




test_data = {
    'start_address': '1769 Rockies Ct, Lafayette, CO',
    'keywords': ['restaurant', 'cafe'],
    'radius': 1609,
    'bounds': {'restaurant': 1800, 'cafe': 1800, 'HOME': 0},
    'budget': 4,
    'time': 28800,
}

data = collectData(test_data)
print("DONE COLLECTING DATA")
solve(data)
