def main():

    n = int(input())

    ans = 0
    for i in range(1, n + 1):
        first = i
        i = i * 3 + 1
        while i != 1:
            if first == i:
                ans += 1
                break
            if i % 2 == 0:
                i //= 2
            else:
                i = i * 3 + 1

    print(ans)


if __name__ == "__main__":
    main()
