from PyQt5 import QtWidgets, QtGui, QtCore
from utils.defines import *


class Vertex(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, x: int, y: int, name: str, color: str):
        super(Vertex, self).__init__(x, y, VERTEX_SIZE, VERTEX_SIZE)

        # Vertex variables
        self._x = x
        self._y = y
        self._name = name
        self._color = color
        self._adjacentVertexList = list()

        # Vertex settings
        self.setPos(x, y)
        self.setBrush(QtGui.QColor(color))
        self.setFlag(QtWidgets.QGraphicsEllipseItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsLineItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtGui.QColor(VERTEX_COLOR))
        painter.drawEllipse(self._x, self._y, VERTEX_SIZE, VERTEX_SIZE)

        painter.setPen(QtCore.Qt.white)
        painter.setFont(QtGui.QFont('Arial', 17))
        painter.drawText(self.rect(), QtCore.Qt.AlignCenter, str(self._name))
        painter.setBrush(QtCore.Qt.NoBrush)

    def addAdjacentVertex(self, vertex):
        self._adjacentVertexList.append(vertex)

    def findAdjacentVertex(self, vertex):
        if vertex in self._adjacentVertexList:
            return True
        return False

    def removeAdjacentVertex(self, vertex):
        if vertex in self._adjacentVertexList:
            self._adjacentVertexList.remove(vertex)

    def getAdjacentVertexList(self):
        return self._adjacentVertexList

    def getName(self):
        return self._name
