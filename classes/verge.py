from PyQt5 import QtWidgets, QtGui, QtCore
from utils.defines import *
from classes.vertex import *
from numpy.linalg import norm
import numpy as np

class Verge:
    def __init__(self, start_vertex: Vertex, end_vertex: Vertex, weight: int):
        self._weight = weight
        self._startVertex = start_vertex
        self._endVertex = end_vertex

    def getStartVertex(self):
        return self._startVertex

    def getEndVertex(self):
        return self._endVertex

    def setStartVertex(self, start_vertex):
        self._startVertex = start_vertex

    def setEndVertex(self, end_vertex):
        self._endVertex = end_vertex

    def collidePoint(self, x: int, y: int):
        x1, y1 = self._startVertex.getPos()
        x2, y2 = self._endVertex.getPos()

        p1 = np.array([x1, y1])
        p2 = np.array([x2, y2])
        p3 = np.array([x, y])
        d = norm(np.cross(p2 - p1, p1 - p3)) / norm(p2 - p1)
        if d <= VERGE_WIDTH:
            return True
        return False
