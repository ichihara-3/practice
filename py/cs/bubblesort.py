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

    bubblesort(data)
    for i in range(0, len(data), 10):
        print(' '.join(map(str, data[i:i+10])))


def bubblesort(data):
    for i in range(len(data)):
        finished = True
        for j in range(len(data)-i-1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
                finished = False
        if finished:
            break


if __name__ == '__main__':
    main()
