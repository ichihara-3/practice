import argparse
import sys

sys.setrecursionlimit(10000000)

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

    output = []
    for x in heapsort(data):
        output.append(str(x))
        if len(output) == 10:
            print(' '.join(output))
            output = []
    if output:
        print(' '.join(output))




def heapsort(data):
    while len(data):
        _heapsort(data, (len(data))//2-1)
        yield data[0]
        data= data[1:]


def _heapsort(data, idx):
    if idx < 0:
        return
    downheap(data, idx)
    if idx == 0:
        return
    _heapsort(data, idx - 1)


def downheap(data, idx):
    left = 2 * idx + 1
    right = 2 * idx + 2
    if left >= len(data):
        return
    if right < len(data) and data[right] < data[left]:
        swap(data, left, right)
    if data[idx] > data[left]:
        swap(data, idx, left)


def swap(array, x, y):
    array[x], array[y] = array[y], array[x]



if __name__ == '__main__':
    main()
