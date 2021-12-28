from classes.graph.graph import *
from algorithms.bfs import *


def isConnected(graph: Graph):
    vertex = graph.getVertexList()[0]
    a = bfs(graph, vertex)
    for i in a.values():
        if i is None:
            return False
    return True
