from functools import reduce
import argparse
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')

    args = parser.parse_args()

    data = []
    with open(args.filename) as f:
        for line in f:
            data.extend(line.split())

    data = bucketsort(data)
    for s in data:
        print(s, flush=True)


def bucketsort(data):
    buckets = [[] for _ in range(26)]
    for s in data:
        if not s:
            continue
        buckets[ord(s[0])-97].append(s)
    for i, bucket in enumerate(buckets):
        buckets[i] = mergesort(bucket)
    return reduce(lambda x, y: x + y, buckets)


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
