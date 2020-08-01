from random import randint

from solve_fullsearch import rec


def create():

    n = randint(1, 101)
    wv = []
    for i in range(n):
        wv.append((randint(1, 101), randint(1, 101)))
    w = randint(1, 10000)

    print(n)
    for w, v in wv:
        print(w, v)
    print(w)
    print(rec(0, w, wv))


create()
