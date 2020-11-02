import argparse
import sys

sys.setrecursionlimit(100000)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')

    args = parser.parse_args()

    data = []
    with open(args.filename) as f:
        for line in f:
            try:
                data.extend(list(map(int, line.split())))
            except ValueError as e:
                print('入力データが不正です')
                print('-------- error情報 --------')
                print(e.with_traceback(sys.exc_info()[2]))
                sys.exit(1)

    data = quicksort(data)
    for i in range(0, len(data), 10):
        print(' '.join(map(str, data[i:i+10])))


def quicksort(data):
    # _quicksort(data, 0, len(data)-1)
    if not data:
        return data
    pivot = data[0]
    left = []
    right = []
    for i in range(1, len(data)):
        if data[i] < pivot:
            left.append(data[i])
        else:
            right.append(data[i])

    return quicksort(left) + [pivot] + quicksort(right)



def _quicksort(data, left, right):
    i = left
    j = right
    if i >= j:
        return
    pivot = data[i+(j-i)//2]
    while i <= j:
        while data[i] < pivot:
            i += 1
        while data[j] > pivot:
            j -= 1
        if i >= j:
            break
        swap(data, i, j)
        i += 1
        j -= 1
    _quicksort(data, left, i-1)
    _quicksort(data, j+1, right)


def swap(data, x, y):
    data[x], data[y] = data[y], data[x]



if __name__ == '__main__':
    main()
