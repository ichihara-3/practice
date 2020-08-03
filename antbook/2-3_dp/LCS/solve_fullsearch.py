# LCS: Longest common subsequence

import sys

sys.setrecursionlimit(1000001)


def main():
    S = input()
    T = input()

    result = solve(0, 0, S, T)
    print(result)

    ans = int(input())
    assert result == ans, f'answer: {ans:d}, result: {result:d}'


def solve(i, j, S, T):
    result = 0
    if len(S[i:]) == 0 or len(T[j:]) == 0:
        result = 0
    elif S[i] != T[j]:
        result = max(solve(i+1, j, S, T), solve(i, j+1, S, T))
    else:
        result = max(solve(i+1, j+1, S, T) + 1, solve(i+1, j, S, T), solve(i, j+1, S, T))
    return result



if __name__ == "__main__":
    main()
