from PyQt5 import QtWidgets, QtGui, QtCore
from utils.defines import *
from classes.vertex import *

class Verge:
    def __init__(self, start_vertex: Vertex, end_vertex: Vertex, weight: int):
        self.weight = weight
        self.startVertex = start_vertex
        self.endVertex = end_vertex

    def getStartVertex(self):
        return self.startVertex

    def getEndVertex(self):
        return self.endVertex

    def setStartVertex(self, start_vertex):
        self.startVertex = start_vertex

    def setEndVertex(self, end_vertex):
        self.endVertex = end_vertex
