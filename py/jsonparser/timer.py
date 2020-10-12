import time
from parser import Parser
p = Parser()
def timer(f):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        print(time.time() - start)
        return result
    return wrapper

def parse_x_times(string, x):
    for _ in range(x):
        p.parse(string)

parse_x_times = timer(parse_x_times)
string = """
      [
        {
           "precision": "zip",
           "Latitude":  37.7668,
           "Longitude": -122.3959,
           "Address":   "",
           "City":      "SAN FRANCISCO",
           "State":     "CA",
           "Zip":       "94107",
           "Country":   "US"
        },
        {
           "precision": "zip",
           "Latitude":  37.371991,
           "Longitude": -122.026020,
           "Address":   "",
           "City":      "SUNNYVALE",
           "State":     "CA",
           "Zip":       "94085",
           "Country":   "US"
        }
      ]
"""
import json
def load_x_times(string, x):
    for _ in range(x):
        json.loads(string)

load_x_times = timer(load_x_times)
print(parse_x_times(string, 10000))
print(load_x_times(string, 10000))
