import argparse
from graph import Edge, UndirectedGraph

def main():
    args = get_args()

    with open(args.graph_filename) as graph_file, \
            open(args.coordinates_filename) as coordinates_file, \
        v, e = map(int, next(graph_file).split())
        graph = UndirectedGraph(size=v)
        for line in graph_file:
            v1, v2, w = map(int, line.split())
            if Edge(v1, v2, w) in graph:
                continue
            graph.add(v1, v2, w)

        node_to_coordinates = []
        coordinates_to_node = {}
        n = int(next(coordinates_file))
        for _ in range(n):
            node, la, lo = map(int, next(coordinates_file).split())
            node_to_coordinates.append((la, lo))
            coordinates_to_node[(la, lo)] = node
    print(node_to_coordinates)
    print(coordinates_to_node)









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
