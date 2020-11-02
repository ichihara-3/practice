import sys


class UndirectedGraph:

    def __init__(self, size):
        self.graph = [[[] for _ in range(size)] for _ in range(size)]

    def add(self, vertex1, vertex2, weight=1):
        self.graph[vertex1][vertex2].append(weight)
        self.graph[vertex2][vertex1].append(weight)


    def get(self, vertex):
        return [(i, e) for i, e in enumerate(self.graph[vertex]) if e]



def main():

    with open(sys.argv[1]) as f:
        V = int(next(f))
        E = int(next(f))

        print(V, E)

        graph = UndirectedGraph(size=V)

        for e in f:
            v1, v2, w = map(int, e.split())
            graph.add(v1, v2, w)


    while True:
        print('-' * 32)
        x = int(input())
        print('-' * 2)
        for y, el in graph.get(x):
            for w in el:
                print(y, w)



if __name__ == '__main__':
    main()


