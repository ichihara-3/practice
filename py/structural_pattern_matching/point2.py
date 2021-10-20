from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

def main():
    point = Point(*map(int, input().split()))

    match point:
        case Point(0, 0):
            print("Origin")
        case Point(0, y):
            print(f"{y=} on Y axis")
        case Point(x=x, y=0):
            print(f"{x=} on X axis")
        case Point(x, y):
            print(f"{x=}, {y=}")
        case _:
            print("Somewhere else")


if __name__ == "__main__":
    main()
