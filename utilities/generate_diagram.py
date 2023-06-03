import ast
import argparse
import networkx as nx
import matplotlib.pyplot as plt
from asciinet import graph_to_ascii


def create_diagram(network_list=None, position_grid=None, output_type=None):
    if network_list is None:
        network_list = input("What is the list of networks: ")
    network_list = ast.literal_eval(network_list)
    G = nx.Graph()
    G.add_edges_from(network_list)

    pos = nx.spring_layout(G)

    if output_type is None:
        output_type = input("What type of output do you want? '1' for svg or '2' for ascii: ")
        output_type = 'svg' if output_type == '1' else 'ascii'

    if output_type.lower() == 'svg':
        if position_grid is None:
            specify_position = input("Do you want to specify the position (y/n): ")
            if specify_position.lower() == 'y':
                position_grid = input("What is the position grid (be sure to specify every node and use a 10 by 10 grid "
                                      "- use format '[11, 00], [1, 04]', etc.):"
                                      "")
        if position_grid:
            position_grid = position_grid.split("],")
            position_grid = [[int(n.split(",")[0].strip(' [')), int(n.split(",")[1].strip(' ]'))] for n in
                             position_grid]
            pos = {(node[0]): (int(str(node[1]).zfill(2)[1:]), 9 - int(str(node[1]).zfill(2)[:1])) for node in
                   position_grid}

        nx.draw(G, pos, with_labels=True)
        plt.savefig("graph.svg", format="svg")
    elif output_type.lower() == 'ascii':
        print(graph_to_ascii(G))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a diagram from a network list and optional position grid.')
    parser.add_argument('--network_list', default=None, help='List of networks. Ex: "[[1, 2], [1, 3], [2, 4]]"')
    parser.add_argument('--position_grid', default=None,
                        help="Position grid. Use format '[11, 00], [1, 04]', etc. Only used if output is 'svg'.")
    parser.add_argument('--output', default=None, choices=['svg', 'ascii'], help="The type of output: 'svg' or 'ascii'")

    args = parser.parse_args()

    create_diagram(args.network_list, args.position_grid, args.output)
