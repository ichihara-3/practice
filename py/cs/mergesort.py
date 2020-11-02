import argparse
import sys

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

    res = mergesort(data)
    for i in range(0, len(res), 10):
        assert res[i:i+10] == sorted(res[i:i+10])
        print(' '.join(map(str, res[i:i+10])))


def mergesort(data):
    if len(data) <= 1:
        return data
    lhalf = mergesort(data[:len(data)//2])
    rhalf = mergesort(data[len(data)//2:])

    i, j = 0, 0
    res = []
    while i < len(lhalf) or j < len(rhalf):
        if i == len(lhalf):
            res.append(rhalf[j])
            j += 1
        elif j == len(rhalf):
            res.append(lhalf[i])
            i += 1
        elif lhalf[i] < rhalf[j]:
            res.append(lhalf[i])
            i += 1
        else:
            res.append(rhalf[j])
            j += 1
    return res


if __name__ == '__main__':
    main()
