# Model

from classes.vertex import *
from classes.verge import *


class Graph:
    def __init__(self):
        self._vertexList = list()
        self._vergeList = list()
        self._isDirectedGraph = False
        self._isWeightedGraph = False

    # Vertex methods
    def addVertex(self, vertex):
        self._vertexList.append(vertex)

        print('after add vertex: ')
        for i in self._vertexList:
            print(i.getName())
        print('\n')

    def findVertexByName(self, name: str):
        for vertex in self._vertexList:
            if vertex.getName() == name:
                return vertex

    def removeVertex(self, vertex: Vertex):
        pass

    # Verge methods
    def addVerge(self, verge: Verge):
        pass

    def findVergeByName(self, name: str):
        for verge in self._vergeList:
            if verge.getName() == name:
                return verge

    def removeVerge(self, verge: Verge):
        pass

    def toggleVergeDirection(self, verge: Verge):
        pass

    def setVergeWeight(self, verge: Verge, weight: int):
        pass

    # Utils
    def getVertexList(self):
        return self._vertexList

    def getVergeList(self):
        return self._vergeList

    def clear(self):
        self._vertexList.clear()
        self._vergeList.clear()
        self._isDirectedGraph = False
        self._isWeightedGraph = False
