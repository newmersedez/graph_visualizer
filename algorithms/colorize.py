from classes.graph.graph import *


def colorize(graph: Graph):
    sorted_vertex = graph.getVertexList();

    for item in sorted_vertex:
        print(len(item.getAdjacentVertexList()))
