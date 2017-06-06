# coding: utf-8

import numpy as np

def AND(x1, x2):
    """AND gate"""
    x = np.array([x1, x2])
    w = np.array([1, 1])
    b = -1.5
    tmp = np.sum(w * x) + b
    if tmp <= 0:
        return 0
    else:
        return 1

def NAND(x1, x2):
    """NAND gate"""
    x = np.array([x1, x2])
    w = np.array([-1, -1])
    b = 1.5
    tmp = np.sum(w * x) + b
    if tmp <= 0:
        return 0
    else:
        return 1

def OR(x1, x2):
    """OR gate"""
    x = np.array([x1, x2])
    w = np.array([1, 1])
    b = -0.5
    tmp = np.sum(w * x) + b
    if tmp <= 0:
        return 0
    else:
        return 1

def XOR(x1, x2):
    """XOR gate"""
    s1 = NAND(x1, x2)
    s2 = OR(x1, x2)
    return AND(s1, s2)


if __name__ == '__main__':
    params = [
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1],
    ]
    for param in params:
        print('x1, x2 =', param)
        print('AND :', AND(*param))
        print('NAND:', NAND(*param))
        print('OR  :', OR(*param))
        print('XOR :', XOR(*param))
        print('==============================')


