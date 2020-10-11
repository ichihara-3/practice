自作ツールの方が100倍遅い


```python
Python 3.7.8 (default, Jul  7 2020, 23:00:51)
[Clang 11.0.3 (clang-1103.0.32.62)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import time
>>> from parser import Parser
>>> p = Parser()
>>> def timer(f):
...     def wrapper(*args, **kwargs):
...         start = time.time()
...         result = f(*args, **kwargs)
...         print(time.time() - start)
...         return result
...     return wrapper
...
>>> def parse_x_times(string, x):
...     for _ in range(x):
...         p.parse(string)
...
>>> parse_x_times = timer(pa
parse_x_times(  pass
>>> parse_x_times = timer(parse_x_times)
>>> string = """
...       [
...         {
...            "precision": "zip",
...            "Latitude":  37.7668,
...            "Longitude": -122.3959,
...            "Address":   "",
...            "City":      "SAN FRANCISCO",
...            "State":     "CA",
...            "Zip":       "94107",
...            "Country":   "US"
...         },
...         {
...            "precision": "zip",
...            "Latitude":  37.371991,
...            "Longitude": -122.026020,
...            "Address":   "",
...            "City":      "SUNNYVALE",
...            "State":     "CA",
...            "Zip":       "94085",
...            "Country":   "US"
...         }
...       ]
... """
>>> import json
>>> def load_x_times(string, x):
...     for _ in range(x):
...         json.loads(string)
...
>>> load_x_times = timer(load_x_times)
>>> load_x_times(string, 10000)
0.0659332275390625
>>> parse_x_times(string, 10000)
5.216763973236084
```
