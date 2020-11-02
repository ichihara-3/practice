import sys


def main():

    with open(sys.argv[1]) as f:
        V = int(next(f))
        E = int(next(f))
        Graph = [[[] for _ in range(V)] for _ in range(V)]

        for e in f:
            v1, v2, w = map(int, e.split())
            Graph[v1][v2].append(w)
            Graph[v2][v1].append(w)


    while True:
        x = int(input())
        for i in range(len(Graph[x])):
            for w in Graph[x][i]:
                print(i, w)


if __name__ == '__main__':
    main()


