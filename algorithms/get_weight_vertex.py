from classes.graph.graph import *
from tkinter import *
from tkinter import messagebox
from algorithms.dijkstra import *
from utils.colorpalletes import *

# edge = ребро
# vertex = вершина

def getWeightVertex(graph: Graph):

    if graph.empty() or len(graph.getVertexList()) == 0:
        return
    weight = 0
    for vertex in graph.getVertexList():
        weight = 0
        for edge in vertex.getAdjacentEdgeList():
            if vertex == edge.getEndVertex() or not edge.isDirected():
                weight += edge.getWeight()
        vertex.setServiceValue("w(" + vertex.getName() + ") = " + str(weight))

def getRadiusDiameter(graph: Graph):
    dijkstraMax = {}
    for vertex in graph.getVertexList():
        dijkstraMax[vertex] = max([x for x in dijkstra_algo(graph, vertex).values() if x is not None])

    messageDialod = QtWidgets.QMessageBox()
    messageDialod.setWindowTitle("R(G), D(G)\n")
    messageDialod.setStyleSheet(WINDOW_DARK)
    messageDialod.setText('Радиус графа:  \nR = ' + str(min(dijkstraMax.values())) +
                          '\nДиаметр графа:  \nD = ' + str(max(dijkstraMax.values())))
    messageDialod.exec_()

def getVectDegree(graph: Graph):

    if graph.empty() or len(graph.getVertexList()) == 0:
        return
    vectDegree = {}

    for i in graph.getVertexList():
        vectDegree[i] = None
    degree = 0

    if (graph._isDirectedGraph == True):
        for vertex in graph.getVertexList():
            degree = 0
            for edge in vertex.getAdjacentEdgeList():
                if vertex == edge.getEndVertex() or not edge.isDirected():
                    degree += 1
            vectDegree[vertex] = degree

    if (graph._isDirectedGraph == False):
        for vertex in graph.getVertexList():
            degree = 0
            for edge in vertex.getAdjacentEdgeList():
                degree += 1
            vectDegree[vertex] = degree

    messageDialod = QtWidgets.QMessageBox()
    messageDialod.setWindowTitle("Вектор степеней вершин графа:\n")
    messageDialod.setStyleSheet(WINDOW_DARK)
    print(vectDegree.values())
    res = ''
    j = 1
    for i in vectDegree.values():
        res += str(j) + ' = [' + str(i) + ']\n'
        j += 1
    messageDialod.setText(res)
    messageDialod.exec_()