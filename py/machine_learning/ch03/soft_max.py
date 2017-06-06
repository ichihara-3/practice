# coding: utf-8

import numpy as np

def softmax(a):
    u"""softmax"""
    c = np.max(a)
    exp_a = np.exp(a - c) # オーバーフロー対策
    sum_exp_a = np.sum(exp_a)
    y = exp_a / sum_exp_a
    return y


if __name__ == '__main__':
    a = np.array([0.3, 2.9, 4.0])
    print(softmax(a))
