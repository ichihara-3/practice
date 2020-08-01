# dp[i][j]: i番目以降で重さの総和がj以下となる価値の総和の最大値
# dp[n][j] = 0
# dp[i][j] = dp[i+1][j] (j < w[i])
# dp[i][j] = max(dp[i+1][j], dp[i+1][j-w[i]]+v[i]) 上記以外

# メモ
# dp[i][w] i番目以降で最大値がwのときの価値
dp = [[0 for j in range(10001)] for i in range(101)]

def main():
    ans = 0
    n = int(input())
    wv = []
    for i in range(n):
        wv.append(list(map(int, input().split())))
    w = int(input())

    ans = solve(0, w, wv, n)

    answer=int(input())
    print('result:', ans)
    print('answer:', answer)
    assert answer == ans


def solve(i, w, wv, n):
    for i in range(n-1, -1, -1):
        for j in range(w+1):
            if j < wv[i][0]:
                dp[i][j] = dp[i+1][j]
            else:
                dp[i][j] = max(dp[i+1][j], dp[i+1][j-wv[i][0]] + wv[i][1])
    return dp[0][w]


if __name__ == '__main__':
    main()
