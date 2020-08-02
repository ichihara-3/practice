# LCS: Longest common subsequence
# dp[i][j]: Sのi番目以降, Tのj番目以降での最長共通文字列
# dp[i][j] = 0 (i==len(S)-1 or j == len(T)-1)
# dp[i][j] = max(dp[i+1][j], dp[i][j+1]) (S[i] != T[i])
# dp[i][j] = max(
#                dp[i+1][j+1]+1  (共通文字列を利用する),
#                dp[i+1][j]      (共通文字列を利用しない),
#                dp[i][j]        (共通文字列を利用しない),
#            )


memo = [[-1 for _ in range(1001)] for _ in range(1001)]

def main():
    S = input()
    T = input()

    result = solve(0, 0, S, T)
    print(result)

    ans = int(input())
    assert result == ans, f'answer: {ans:d}, result: {result:d}'


def solve(i, j, S, T):
    result = 0
    if memo[i][j] >= 0:
        return memo[i][j]
    if len(S[i:]) == 0 or len(T[j:]) == 0:
        result = 0
    elif S[i] != T[j]:
        result = max(solve(i+1, j, S, T), solve(i, j+1, S, T))
    else:
        result = max(solve(i+1, j+1, S, T) + 1, solve(i+1, j, S, T), solve(i, j+1, S, T))
    memo[i][j] = result
    return result



if __name__ == "__main__":
    main()
