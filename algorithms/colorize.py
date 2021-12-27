from classes.graph.graph import *


def colorize(graph: Graph):
    sorted_vertex = graph.getVertexList();

    for item in sorted_vertex:
        print("vertex {} = {}".format(item.getName(), len(item.getAdjacentVertexList())))
