def main():
    n = int(input())
    now = (0, 0)


    ans = solve(n, now, [now])
    print(ans)


def solve(n, now, visited):
    if n == 0:
        return 1

    deadend = True
    answer = 0
    for move in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        moveto = (now[0]+move[0], now[1]+move[1])
        if moveto in visited:
            continue
        else:
            deadend = False
            answer += solve(n-1, moveto, visited + [moveto])
    return answer


if __name__ == '__main__':
    main()
