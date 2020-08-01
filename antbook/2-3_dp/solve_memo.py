# 重さ w(i) 価値 v(i) のn個の品物
# 重さの総和がWを超えないように選んだ時の、max(∑v)

# メモ
# dp[i][w] i番目以降で最大値がwのときの価値
dp = [[-1 for j in range(10001)] for i in range(101)]

def main():
    ans = 0
    n = int(input())
    wv = []
    for i in range(n):
        wv.append(list(map(int, input().split())))
    w = int(input())

    ans = rec(0, w, wv)

    answer=int(input())
    print('result:', ans)
    print('answer:', answer)
    assert answer == ans


def rec(i, w, wv):
    if dp[i][w] >= 0:
        return dp[i][w]
    result = 0
    # 全ての品物を検査済
    if i == len(wv):
        result = 0

    # 重さが上限を超えているなら採用せず次の品物
    elif w < wv[i][0]:
        result = rec(i+1, w, wv)
    else:
        # max(この品物を採用しないパターン vs 採用するパターン)
        result = max(rec(i+1, w, wv), rec(i+1, w-wv[i][0], wv) + wv[i][1])
    dp[i][w] = result
    return result



if __name__ == '__main__':
    main()
