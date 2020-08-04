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


dp = [[0 for _ in range(3001)] for _ in range(3001)]


def main():
    S = input()
    T = input()

    result = solve(S, T)
    print(result)


def solve(S, T):
    for i in range(1, len(S) + 1):
        for j in range(1, len(T) + 1):
            if S[i - 1] != T[j - 1]:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1], dp[i-1][j-1])
            else:
                dp[i][j] = max(dp[i - 1][j - 1] + 1, dp[i - 1][j], dp[i][j - 1])
    result = ""
    i = len(S)
    j = len(T)
    while dp[i][j] != 0:
        if dp[i][j] == dp[i-1][j]:
            i -= 1
        elif dp[i][j] == dp[i][j-1]:
            j -= 1
        else:
            result += S[i-1]
            i -= 1
            j -= 1
    return "".join(reversed(result))


if __name__ == "__main__":
    main()
