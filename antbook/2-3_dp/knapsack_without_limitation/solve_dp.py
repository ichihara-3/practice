# 重さ w(i) 価値 v(i) のn種類の品物
# 重さの総和がWを超えないように選んだ時の、max(∑v)
# dp[i][j] 重さの総和がi(0..W)のときのj(0..n-1)番目までの品物から選んだ時の価値の最大値
# dp[0][j] = 0 重さの総和が0のときのj(0..n-1)番目までの品物から選んだ時の価値の最大値
# dp[0][0] = 0
# dp[i][0] = (n/w) * v
# dp[i][j] = max(
#               dp[i][j-1],    # j番目の商品を使わない場合
#               dp[i-w][j] + v # j番目の商品を使う場合
#            )

dp = [[0 for _ in range(101)] for _ in range(100001)]


def main():
    n = int(input())
    wv = []
    for _ in range(n):
        wv.append(list(map(int, input().split())))
    cap = int(input())
    ans = solve(n, cap, wv)
    print(ans)


def solve(n, cap, wv):
    for i in range(0, cap + 1):
        for j in range(0, n):
            weight = wv[j][0]
            value = wv[j][1]
            if i < weight:
                dp[i][j+1] = dp[i][j]
            else:
                dp[i][j+1] = max(dp[i][j], dp[i-weight][j+1]+value)
    return dp[cap][n]


if __name__ == "__main__":
    main()
