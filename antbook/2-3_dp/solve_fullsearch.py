# 重さ w(i) 価値 v(i) のn個の品物
# 重さの総和がWを超えないように選んだ時の、max(∑v)

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


def rec(i, weight, wv):
    if i == len(wv):
        return 0
    if weight < wv[i][0]:
        return rec(i+1, weight, wv)
    return max(rec(i+1, weight, wv), rec(i+1, weight-wv[i][0], wv) + wv[i][1])


if __name__ == '__main__':
    main()
