import itertools
from algorithms.colorize import *

def wedding(graph: Graph):  # Rina
    if(len(set(colorize(graph).values()))) != 2:
        return False
    coloredVertex = colorize(graph)
    groupOne = []
    groupTwo = []
    man = []
    woman = []
    for ver in coloredVertex.keys():
        if coloredVertex[ver] == 1:
            groupOne.append(ver)
        else:
            groupTwo.append(ver)
    if len(groupOne) > len(groupTwo):
        man = groupTwo
        woman = groupOne
    else:
        man = groupOne
        woman = groupTwo
    for ver in graph.getVertexList():
        if len(ver.getAdjacentEdgeList()) == 0:
            return False
    allSubset = []

    for i in range(1, len(man)+1):
        allSubset = allSubset + list(itertools.combinations(man, i))

    for currentComb in allSubset:
        womanlist = []
        for verFromCombMan in currentComb:
            for verFromCombWoman in verFromCombMan.getAdjacentVertexList():
                womanlist.append(verFromCombWoman)

        if len(set(womanlist)) < len(currentComb):
            return False
    allEdgesVariant = []
    allEdgesVariant = list(itertools.combinations(graph.getEdgeList(), len(man)))
    for combOfEdges in allEdgesVariant:
        vertexFromEdges = []
        for edge in combOfEdges:
            vertexFromEdges.append(edge.getStartVertex())
            vertexFromEdges.append(edge.getEndVertex())
        if len(set(vertexFromEdges)) == len(man)*2:
            return combOfEdges

    return True

def setVisualForWedding(path):
    for i in path:
        i.setColor(QtCore.Qt.blue)