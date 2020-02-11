

memo = {}

def fibonacci(n):
    if n <= 1:
        return n
    if n in memo:
        return memo[n]
    memo[n] = fibonacci(n - 2) + fibonacci(n - 1)
    return memo[n]



if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        sys.stderr.write('usage: {} COUNT\n'.format(sys.argv[0]))
        sys.exit(1)
    count = int(sys.argv[1])
    for i in range(count):
        print(fibonacci(i))
