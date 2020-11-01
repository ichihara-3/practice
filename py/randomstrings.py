import argparse
import random
import string

def generate(k=10):
    return ''.join(random.choices(string.ascii_lowercase, k=k))


def generate_x(length=10, times=10):
    for _ in range(times):
        print(generate(length))

def main():
    p = argparse.ArgumentParser()
    p.add_argument('-l', type=int, required=False, default=10)
    p.add_argument('-t', type=int, required=False, default=10)
    args = p.parse_args()

    generate_x(args.l, args.t)


if __name__ == '__main__':
    main()
