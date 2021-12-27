from classes.graph.graph import *


def createName(graph: Graph, completed_nodes):
    name_from_graph = 1 if len(graph.getEdgeList()) == 0 else int(graph.getEdgeList()[-1].getName()) + 1
    name_from_graph += len(completed_nodes)
    return (str(name_from_graph))


def complete(graph: Graph):
    matrix = graph.getAdjacentMatrix()
    completed_nodes = []
    for x in range(len(matrix)):
        for y in range(x, len(matrix[x])):
            if matrix[x][y] > 0 or x == y:
                matrix[x][y] = 0
            else:
                matrix[x][y] = 1
                matrix[y][x] = 1
                completed_nodes.append(Edge(graph.getVertexList()[x], graph.getVertexList()[y], color=QtCore.Qt.green,
                    name=createName(graph, completed_nodes)))
    # adjMatrix = matrix + graph.getAdjacentMatrix()
    # print(adjMatrix)
    # graph.setEdgesFromAdjacentMatrix(adjMatrix)
    return completed_nodes

def setVisualForComplete(graph: Graph, completed_nodes):
    for i in completed_nodes:
        graph.addEdge(i)