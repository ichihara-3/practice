import random
import string

from solve_memo import solve


def create():

    n = random.randint(1, 3000)
    m = random.randint(1, 3000)

    s = ''.join(random.choices(string.ascii_lowercase, k=n))
    t = ''.join(random.choices(string.ascii_lowercase, k=m))

    print(s)
    print(t)

if __name__ == '__main__':
    create()
