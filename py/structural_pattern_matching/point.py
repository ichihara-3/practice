

def main():
    point = tuple(map(int, input().split()))

    match point:
        case (0, 0):
            print("Origin")
        case (0, y):
            print(f"{y=} on Y axis")
        case (x, 0):
            print(f"{x=} on X axis")
        case (x, y):
            print(f"{x=}, {y=}")
        case _:
            print("Error! not a point")


if __name__ == "__main__":
    main()
