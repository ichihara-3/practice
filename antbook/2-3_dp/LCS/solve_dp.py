# LCS: Longest common subsequence
# dp[i][j]: Sのi-1番目まで, Tのj-1番目まででの最長共通文字列
# dp[0][0] = 0 長さ0の文字列
# dp[0][1] = 0 長さ1の文字列と長さ0の文字列
# dp[1][0] = 0 長さ0の文字列と長さ1の文字列
# dp[i][j] = max(dp[i-1][j], dp[i][j-1]) (S[i] != T[j])
# dp[i][j] = max(
#                dp[i-1][j-1]+1  (共通文字列を利用する),
#                dp[i-1][j]        (共通文字列を利用しない),
#                dp[i][j-1]        (共通文字列を利用しない),
#            )


dp = [[0 for _ in range(1001)] for _ in range(1001)]

def main():
    S = input()
    T = input()

    result = solve(S, T)
    print(result)

    ans = int(input())
    assert result == ans, f'answer: {ans:d}, result: {result:d}'


def solve(S, T):
    for i, s in enumerate(S, start=1):
        for j, t in enumerate(T, start=1):
            if s != t:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
            else:
                dp[i][j] = max(dp[i-1][j-1] + 1, dp[i-1][j], dp[i][j-1])
    return dp[len(S)][len(T)]


if __name__ == "__main__":
    main()
