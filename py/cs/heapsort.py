import argparse
import sys

sys.setrecursionlimit(10000000)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()

    data = []
    with open(args.filename) as f:
        for line in f:
            try:
                data.extend(list(map(int, line.split())))
            except ValueError as e:
                print("入力データが不正です")
                print("-------- error情報 --------")
                print(e.with_traceback(sys.exc_info()[2]))
                sys.exit(1)

    output = []
    heapsort(data)
    for x in data:
        output.append(str(x))
        if len(output) == 10:
            print(" ".join(output))
            output = []
    if output:
        print(" ".join(output))


def heapsort(data):
    if not data:
        return
    for i in range(len(data)):
        upheap(data, i)
    for j in range(len(data) - 1, 0, -1):
        swap(data, 0, j)
        downheap(data, j)


def upheap(data, n):
    while n > 0:
        parent = (n - 1) // 2
        if data[parent] < data[n]:
            swap(data, parent, n)
            n = parent
        else:
            break


def downheap(data, n):
    now = 0
    left = 2 * now + 1
    right = 2 * now + 2
    target = 0
    while left < n:
        if data[now] < data[left]:
            target = left
        if right < n and data[left] < data[right]:
            target = right
        if target:
            swap(data, now, target)
            now = target
            left = 2 * now + 1
            right = 2 * now + 2
            target = 0
        else:
            break


def swap(data, x, y):
    data[x], data[y] = data[y], data[x]


if __name__ == "__main__":
    main()
