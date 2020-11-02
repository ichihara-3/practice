import sys


class UndirectedGraph:
    def __init__(self, size):
        self.graph = [[] for _ in range(size)]

    def add(self, vertex1, vertex2, weight=1):
        edge = Edge(vertex1, vertex2, weight)
        self.graph[vertex1].append(edge)
        self.graph[vertex2].append(edge)

    def get(self, vertex):
        return sorted(edge for edge in self.graph[vertex])


class Edge:
    def __init__(self, v1, v2, w):
        if v1 > v2:
            v1, v2 = v2, v1
        self._v1 = v1
        self._v2 = v2
        self._weight = w

    def __eq__(self, o):
        return self.values == o.values

    def __lt__(self, o):
        return self.values < o.values

    def opposite(self, v):
        if v == self._v1:
            return self._v2
        elif v == self._v2:
            return self._v1
        else:
            raise ValueError("Not Found")

    @property
    def values(self):
        return self._v1, self._v2, self._weight

    @property
    def weight(self):
        return self._weight


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
        print("-" * 32)
        x = int(input())
        print("-" * 2)
        for edge in graph.get(x):
            print(edge.opposite(x), edge.weight)


if __name__ == "__main__":
    main()
