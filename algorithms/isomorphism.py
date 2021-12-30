import itertools

import numpy

from algorithms.bfs import *


def isomorph(graph: Graph):  # Rina
    vertexList = graph.getVertexList()
    vertexListCopy = []
    for i in vertexList:
        vertexListCopy.append(i)
    subgraphs = [[], []]
    subgraphsedges = [[], []]
    negativeFirstBfs = []
    secondRoot = 0
    bfsFirstResult = bfs(graph, vertexListCopy[0])
    for i in bfsFirstResult.keys():
        if bfsFirstResult[i] is None:
            secondRoot = i
            break
    if secondRoot == 0:
        return None
    bfsSecondtResult = bfs(graph, secondRoot)
    for i in bfsSecondtResult.keys():
        if bfsSecondtResult[i] is None:
            negativeFirstBfs.append(i)

    for i in bfsFirstResult.keys():
        if bfsFirstResult[i] is not None:
            subgraphs[0].append(i)
            for j in i.getAdjacentEdgeList():
                subgraphsedges[0].append(j)
        else:
            subgraphs[1].append(i)
            for j in i.getAdjacentEdgeList():
                subgraphsedges[1].append(j)

    for i in subgraphs[0]:
        vertexListCopy.remove(i)
    if len(subgraphs[0]) != len(negativeFirstBfs):
        return None
    # for i in subgraphs[0]:
    #     print(i.getName())
    subgraphsedges1 = [[], []]
    subgraphsedges1[0] = list(set(subgraphsedges[0]))
    subgraphsedges1[1] = list(set(subgraphsedges[1]))

    first = Graph()
    second = Graph()
    # First Graph init
    for i in subgraphs[0]:
        first.addVertex(i)
    for i in subgraphsedges1[0]:
        first.addEdge(i)
    # Second Graph init
    for i in subgraphs[1]:
        second.addVertex(i)
    for i in subgraphsedges1[1]:
        second.addEdge(i)

    print(first.getAdjacentMatrix())
    print(second.getAdjacentMatrix())

    if numpy.array_equal(first.getAdjacentMatrix(), second.getAdjacentMatrix()):
        return True

    if len(first.getEdgeList()) != len(second.getEdgeList()):
        return False
    if len(first.getVertexList()) != len(second.getVertexList()):
        return False

    return checkIsomorphismMatrix(first.getAdjacentMatrix(), second.getAdjacentMatrix())


def checkIsomorphismMatrix(a : np.array, b : np.array):
    if a.shape != b.shape:
        return False
    n = a.shape[0]
    perms = [i for i in range(0, n)]
    for perm in itertools.permutations(perms):
        matrix = np.zeros((n, n))
        i0 = 0
        for i in perm:
            j0 = 0
            for j in perm:
                matrix[i0][j0] = b[i][j]
                j0 += 1
            i0 += 1
        flag = True
        for i in range(0, n):
            for j in range(0, n):
                if matrix[i][j] != a[i][j]:
                    flag = False
                    break
            if not flag:
                break
        if flag:
            return True
    return False

