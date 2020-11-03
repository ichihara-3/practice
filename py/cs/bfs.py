import sys
from graph import UndirectedGraph

def main():
    with open(sys.argv[1]) as f:
        V = int(next(f))
        E = int(next(f))

        graph = UndirectedGraph(size=V)

        for e in f:
            v1, v2, w = map(int, e.split())
            graph.add(v1, v2, w)

    while True:
        start = int(input())

        bfs(graph, start)


def bfs(graph, start):
    res = []
    queue = [start]
    visited = {}

    while queue:
        node = queue.pop(0)
        res.append(node)
        visited.add(node)
        for edge in graph.get(node):
            v = edge.opposite(node)
            if v not in visited:
                queue.append(v)


if __name__ == '__main__':
    main()
