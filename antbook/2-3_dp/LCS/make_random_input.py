import random
import string

from solve_memo import solve


def create():

    n = random.randint(1, 1000)
    m = random.randint(1, 1000)

    s = ''.join(random.choices(string.ascii_lowercase, k=n))
    t = ''.join(random.choices(string.ascii_lowercase, k=m))

    print(s)
    print(t)
    print(solve(0, 0, s, t))

if __name__ == '__main__':
    create()
