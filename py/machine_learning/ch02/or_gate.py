# coding: utf-8

import numpy as np

def OR(x1, x2):
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    b = -0.3
    tmp = np.sum(w*x) + b
    if tmp <= 0:
        return 0
    else:
        return 1


if __name__ == '__main__':
    params = [
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1],
    ]
    for param in params:
        print(OR(*param))
