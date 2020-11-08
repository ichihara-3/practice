from os.path import exists
import argparse
import math
import heapq
import pickle
import time

from graph import Edge, UndirectedGraph


class Variables:

    def __init__(self):
        self.node_to_coordinates = []
        self.coordinates_to_node = []

var = Variables()

def main():
    args = get_args()

    if exists('graph.pickle') and exists('node_to_coordinates.pickle') and exists('coordinates_to_node.pickle'):
        with open('graph.pickle', 'rb') as g, \
                open('node_to_coordinates.pickle', 'rb') as n,\
                open('coordinates_to_node.pickle', 'rb') as c:
            graph = pickle.load(g)
            var.node_to_coordinates = pickle.load(n)
            var.coordinates_to_node = pickle.load(c)
    else:

        with open(args.graph_filename) as graph_file, \
                open(args.coordinates_filename) as coordinates_file:

            var.node_to_coordinates = []
            var.coordinates_to_node = {}
            n = int(next(coordinates_file))
            for _ in range(n):
                node, la, lo = map(int, next(coordinates_file).split())
                var.node_to_coordinates.append((la, lo))
                var.coordinates_to_node[(la, lo)] = node

            v, e = map(int, next(graph_file).split())
            graph = UndirectedGraph(size=v)
            for line in graph_file:
                v1, v2, w = map(int, line.split())
                if Edge(v1, v2, w) in graph:
                    continue
                graph.add(v1, v2, w)

            with open('graph.pickle', 'wb') as g, \
                    open('node_to_coordinates.pickle', 'wb') as n,\
                    open('coordinates_to_node.pickle', 'wb') as c:
                pickle.dump(graph, g)
                pickle.dump(var.node_to_coordinates, n)
                pickle.dump(var.coordinates_to_node, c)
    start_la, start_lo = find_nearest_point(var.coordinates_to_node.keys(), int(args.start_latitude.replace('.', '')), int(args.start_longitude.replace('.', '')))
    goal_la, goal_lo = find_nearest_point(var.coordinates_to_node.keys(), int(args.goal_latitude.replace('.', '')), int(args.goal_longitude.replace('.', '')))

    start = var.coordinates_to_node[(start_la, start_lo)]
    goal = var.coordinates_to_node[(goal_la, goal_lo)]

    start_time = time.time()

    path, distance = shortestpath(graph, start, goal)

    elapsed = time.time() - start_time
    print(f'elapsed time: {elapsed}')

    with open(args.outputfilename, 'w') as f:
        f.writelines(map(lambda x: ' '.join(map(str,var.node_to_coordinates[x])) + '\n', path))


def find_nearest_point(coordinates_list, latitude, longitiude):
    min_dist = float('inf')
    nearest_latitude = None
    nearest_longitude = None
    for la, lo in coordinates_list:
        dist = calc_dist(la, lo, latitude, longitiude)
        if dist < min_dist:
            min_dist = dist
            nearest_latitude = la
            nearest_longitude = lo
    return nearest_latitude, nearest_longitude



def calc_dist(start_latitude, start_longitude, goal_latitude, goal_longitude):
    dx = start_latitude - goal_latitude
    dy = start_longitude - goal_longitude
    return dx ** 2 + dy ** 2


# def shortestpath(graph, start, end):

#     d = [float('inf') for _ in range(graph.size)]
#     d[start] = 0
#     A = []
#     prev = [-1 for _ in range(graph.size)]
#     heapq.heappush(A, (d[start], start))

#     while A:
#         _, v = heapq.heappop(A)


#         if v == end:
#             break

#         for edge in graph.get(v):
#             w = edge.opposite(v)
#             if d[w] > d[v] + edge.weight:
#                 d[w] = d[v] + edge.weight
#                 prev[w] = v
#                 heapq.heappush(A, (d[w], w))

#     now = end
#     path = [now]
#     while now != start:
#         now = prev[now]
#         path.append(now)
#     path = reversed(path)
#     return path, d[end]


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
                heapq.heappush(A, (d[w] + euclidean_distance(*var.node_to_coordinates[w], *var.node_to_coordinates[end]), w))

    now = end
    path = [now]
    while now != start:
        now = prev[now]
        path.append(now)
    path = reversed(path)
    return path, d[end]


def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2) **2)


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('graph_filename')
    parser.add_argument('coordinates_filename')
    parser.add_argument('start_latitude')
    parser.add_argument('start_longitude')
    parser.add_argument('goal_latitude')
    parser.add_argument('goal_longitude')
    parser.add_argument('outputfilename')

    return parser.parse_args()


if __name__ == '__main__':
    main()
