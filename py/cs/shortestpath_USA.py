from os.path import exists
import argparse
import math
import pickle

from graph import Edge, UndirectedGraph

def main():
    args = get_args()

    if exists('graph.pickle') and exists('node_to_coordinates.pickle') and exists('coordinates_to_node.pickle'):
        with open('graph.pickle', 'rb') as g, \
                open('node_to_coordinates.pickle', 'rb') as n,\
                open('coordinates_to_node.pickle', 'rb') as c:
            graph = pickle.load(g)
            node_to_coordinates = pickle.load(n)
            coordinates_to_node = pickle.load(c)
    else:

        with open(args.graph_filename) as graph_file, \
                open(args.coordinates_filename) as coordinates_file:

            node_to_coordinates = []
            coordinates_to_node = {}
            n = int(next(coordinates_file))
            for _ in range(n):
                node, la, lo = map(int, next(coordinates_file).split())
                node_to_coordinates.append((la, lo))
                coordinates_to_node[(la, lo)] = node

            v, e = map(int, next(graph_file).split())
            graph = UndirectedGraph(size=v)
            for line in graph_file:
                v1, v2, w = map(int, line.split())
                distance = calc_dist(*node_to_coordinates[v1], *node_to_coordinates[v2])
                if Edge(v1, v2, distance) in graph:
                    continue
                graph.add(v1, v2, distance)

            with open('graph.pickle', 'wb') as g, \
                    open('node_to_coordinates.pickle', 'wb') as n,\
                    open('coordinates_to_node.pickle', 'wb') as c:
                pickle.dump(graph, g)
                pickle.dump(node_to_coordinates, n)
                pickle.dump(coordinates_to_node, c)



    print([edge.values for edge in graph.get(0)])



def calc_dist(start_latitude, start_longitude, goal_latitude, goal_longitude):
    dx = start_latitude - goal_latitude
    dy = start_longitude - goal_longitude
    return dx ** 2 + dy ** 2


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
