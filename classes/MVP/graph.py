# Model

from classes.graph.edge import *
from classes.graph.vertex import *
import numpy as np

class Graph:
    def __init__(self):
        self._vertexList = list()
        self._edgeList = list()
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

            for item in self._edgeList[:]:
                if item.getStartVertex() == vertex or item.getEndVertex() == vertex:
                    self._edgeList.remove(item)
            self._vertexList.remove(vertex)

            print('after remove vertex: ')
            for i in self._vertexList:
                print(i.getName())
            for i in self._edgeList:
                print(i.getStartVertex().getName(), ' -> ', i.getEndVertex().getName())
            print('\n')

    def findVertexByName(self, name: str):
        for item in self._vertexList:
            if item.getName() == name:
                return item

    # Edge methods
    def addEdge(self, edge: Edge):
        if edge is not None:
            startVertex = edge.getStartVertex()
            endVertex = edge.getEndVertex()

            self._edgeList.append(edge)
            startVertex.addAdjacentVertex(endVertex, edge)
            endVertex.addAdjacentVertex(startVertex, edge)

            print('after add edge: ')
            for i in self._edgeList:
                print(i.getStartVertex().getName(), ' -> ', i.getEndVertex().getName())
            print('\n')

    def removeEdge(self, edge: Edge):
        if edge is not None:
            startVertex = edge.getStartVertex()
            endVertex = edge.getEndVertex()

            if startVertex == endVertex:
                startVertex.setLoop(value=False)

            startVertex.removeAdjacentVertex(endVertex)
            endVertex.removeAdjacentVertex(startVertex)
            self._edgeList.remove(edge)

            print('after remove edge: ')
            for i in self._edgeList:
                print(i.getStartVertex().getName(), ' -> ', i.getEndVertex().getName())
            print('\n')

    def findEdgeByName(self, name: str):
        for edge in self._edgeList:
            if edge.getName() == name:
                return edge

    def toggleEdgeDirection(self, edge: Edge):
        if edge in self._edgeList:
            edge.toggleDirection()

    def setEdgeWeight(self, edge: Edge, weight: int):
        if edge in self._edgeList:
            edge.setWeight(weight)

    # Utils
    def getVertexList(self):
        return self._vertexList

    def getEdgeList(self):
        return self._edgeList

    def clear(self):
        self._vertexList.clear()
        self._edgeList.clear()
        self._isDirectedGraph = False
        self._isWeightedGraph = False

        print('after clean all: ')
        for i in self._vertexList:
            print(i.getName())
        for i in self._edgeList:
            print(i.getStartVertex().getName(), ' -> ', i.getEndVertex().getName())
        print('\n')

    def getAdjacentMatrix(self):
        m = len(self._vertexList)
        matrix = np.array([[0] * m] * m)
        i = 0
        for edge in self._edgeList:
            start = self._vertexList.index(edge.getStartVertex())
            end = self._vertexList.index(edge.getEndVertex())
            matrix[start][end] = edge.getWeight()
            if not edge.isDirected():
                matrix[end][start] = edge.getWeight()
        return matrix

    def getIncidenceMatrix(self):
        n = len(self._edgeList)
        m = len(self._vertexList)
        matrix = np.array([[0] * n] * m)
        i = 0
        for edge in self._edgeList:
            start = self._vertexList.index(edge.getStartVertex())
            end = self._vertexList.index(edge.getEndVertex())
            matrix[start][i] = 1
            if edge.isDirected():
                matrix[end][i] = -1
            else:
                matrix[end][i] = 1
            i += 1
        return matrix


