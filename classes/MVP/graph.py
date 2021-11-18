# Model

from classes.graph.verge import *
from classes.graph.vertex import *
import numpy as np

class Graph:
    def __init__(self):
        self._vertexList = list()
        self._vergeList = list()
        self._isDirectedGraph = False
        self._isWeightedGraph = False

    # Vertex methods
    def addVertex(self, vertex: Vertex):
        if vertex is not None:
            self._vertexList.append(vertex)

            print('after add vertex: ')
            for i in self._vertexList:
                print(i.getName())
            print('\n')

    def removeVertex(self, vertex: Vertex):
        if vertex is not None:
            for item in self._vertexList:
                item.removeAdjacentVertex(vertex)

            for item in self._vergeList[:]:
                if item.getStartVertex() == vertex or item.getEndVertex() == vertex:
                    self._vergeList.remove(item)
            self._vertexList.remove(vertex)

            print('after remove vertex: ')
            for i in self._vertexList:
                print(i.getName())
            for i in self._vergeList:
                print(i.getStartVertex().getName(), ' -> ', i.getEndVertex().getName())
            print('\n')

    def findVertexByName(self, name: str):
        for item in self._vertexList:
            if item.getName() == name:
                return item

    # Verge methods
    def addVerge(self, verge: Verge):
        if verge is not None:
            startVertex = verge.getStartVertex()
            endVertex = verge.getEndVertex()

            self._vergeList.append(verge)
            startVertex.addAdjacentVertex(endVertex)
            endVertex.addAdjacentVertex(startVertex)

            print('after add verge: ')
            for i in self._vergeList:
                print(i.getStartVertex().getName(), ' -> ', i.getEndVertex().getName())
            print('\n')

    def removeVerge(self, verge: Verge):
        if verge is not None:
            startVertex = verge.getStartVertex()
            endVertex = verge.getEndVertex()

            if startVertex == endVertex:
                startVertex.setLoop(value=False)

            startVertex.removeAdjacentVertex(endVertex)
            endVertex.removeAdjacentVertex(startVertex)
            self._vergeList.remove(verge)

            print('after remove verge: ')
            for i in self._vergeList:
                print(i.getStartVertex().getName(), ' -> ', i.getEndVertex().getName())
            print('\n')

    def findVergeByName(self, name: str):
        for verge in self._vergeList:
            if verge.getName() == name:
                return verge

    def toggleVergeDirection(self, verge: Verge):
        if verge in self._vergeList:
            verge.toggleDirection()

    def setVergeWeight(self, verge: Verge, weight: int):
        if verge in self._vergeList:
            verge.setWeight(weight)

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

        print('after clean all: ')
        for i in self._vertexList:
            print(i.getName())
        for i in self._vergeList:
            print(i.getStartVertex().getName(), ' -> ', i.getEndVertex().getName())
        print('\n')

    def getAdjacentMatrix(self):
        m = len(self._vertexList)
        matrix = np.array([[0] * m] * m)
        i = 0
        for verge in self._vergeList:
            start = self._vertexList.index(verge.getStartVertex())
            end = self._vertexList.index(verge.getEndVertex())
            matrix[start][end] = verge.getWeight()
            if not verge.isDirected():
                matrix[end][start] = verge.getWeight()

        print(matrix)
        return matrix

    def getIncindenceMatrix(self):
        n = len(self._vergeList)
        m = len(self._vertexList)
        matrix = np.array([[0] * n] * m)
        i = 0
        for verge in self._vergeList:
            start = self._vertexList.index(verge.getStartVertex())
            end = self._vertexList.index(verge.getEndVertex())
            matrix[start][i] = 1
            if verge.isDirected():
                matrix[end][i] = -1
            else:
                matrix[end][i] = 1
            i += 1

        print("hahaha")
        print(matrix)

        return matrix


