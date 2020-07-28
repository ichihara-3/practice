def main():
    count = 0
    n, m = map(int, input().split())
    number = 1
    while number < n:
        number = number * 2 if number <= m else number + m
        count += 1
    print(count)

main()
