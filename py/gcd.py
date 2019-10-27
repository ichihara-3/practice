def gcd(a, b):
  if a <= 0 or b <= 0:
    raise ValueError('arguments must be greater than 0')
  x, y = (a, b) if a > b else (b, a)
  while y > 0:
    x, y = y, x % y
  return x


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(usage='calculate the greatest common divisor of two numbers')
    parser.add_argument('a', type=int)
    parser.add_argument('b', type=int)
    args = parser.parse_args()

    print(gcd(args.a, args.b))
