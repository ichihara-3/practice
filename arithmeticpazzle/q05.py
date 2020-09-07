import sys


def main():

    target = int(input())
    if target not in (1000, 2000, 5000, 10000):
        sys.stderr.write('お札は1000, 2000, 5000, 10000のどれか\n')
        return
    ans = solve(target)

    print(ans)


def solve(n, coins=(500, 100, 50, 10), usable=15):
    if usable < 0:
        return 0
    if n < 0:
        return 0
    if n == 0:
        return 1
    if not coins:
        return 0

    ans = 0
    coin = coins[0]
    for i in range(0, n//coin+1):
        ans += solve(n - coin*i, coins[1:], usable-i)
    return ans




if __name__ == '__main__':
    main()
