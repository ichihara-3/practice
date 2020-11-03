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
        print('-' * 2)

        dfs(graph, start)
        print('-' * 32)


def dfs(graph, start):
    stack = [start]
    visited = set()

    while stack:
        node = stack.pop()
        visited.add(node)
        print(node)
        for edge in graph.get(node):
            v = edge.opposite(node)
            if v not in visited:
                stack.append(v)


if __name__ == '__main__':
    main()
