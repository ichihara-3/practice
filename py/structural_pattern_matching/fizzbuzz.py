
def fizzbuzz(n: int)-> str:
    match n % 3, n % 5:
        case 0, 0:
            res = "fizzbuzz"
        case 0, _:
            res = "fizz"
        case _, 0:
            res = "buzz"
        case _, _:
            res = str(n)
    return res


def main():
    num = int(input("input a number ... : "))
    for i in range(1, num+1):
        print(fizzbuzz(i))


if __name__ == "__main__":
    main()
