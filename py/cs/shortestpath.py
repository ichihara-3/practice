import heapq
import sys
from graph import UndirectedGraph

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
        start = int(input('start:'))
        end = int(input('end:'))

        path, distance = shortestpath(graph, start, end)

        print(' '.join(map(str, path)))
        print(distance)


def shortestpath(graph, start, end):

    d = [float('inf') for _ in range(graph.size)]
    d[start] = 0
    A = []
    prev = [-1 for _ in range(graph.size)]
    heapq.heappush(A, (d[start], start))

    while A:
        _, v = heapq.heappop(A)

        if v == end:
            break

        for edge in graph.get(v):
            w = edge.opposite(v)
            if d[w] > d[v] + edge.weight:
                d[w] = d[v] + edge.weight
                prev[w] = v
                heapq.heappush(A, (d[w], w))

    now = end
    path = [now]
    while now != start:
        now = prev[now]
        path.append(now)
    path = reversed(path)
    return path, d[end]



if __name__ == '__main__':
    main()
