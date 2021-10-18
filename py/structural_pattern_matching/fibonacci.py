
def memorize(func):
    memo = {}
    def wrapper(n):
        if n in memo:
            return memo[n]
        result = func(n)
        memo[n] = result
        return result
    return wrapper


@memorize
def fibonacci(n: int) -> int:
    match n:
        case 0 | 1:
            return n
        case _:
            return fibonacci(n-1) + fibonacci(n-2)


def main():
    num = int(input("input a number ... : "))
    for i in range(1, num+1):
        print(fibonacci(i))



if __name__ == "__main__":
    main()
