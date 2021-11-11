from PyQt5 import QtWidgets, QtGui, QtCore
from utils.defines import *


class Vertex(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, x: int, y: int, name: str, color: str):
        super(Vertex, self).__init__(x, y, VERTEX_SIZE, VERTEX_SIZE)

        self.setPos(x, y)
        self.setBrush(QtGui.QColor(color))
        self.setFlag(QtWidgets.QGraphicsEllipseItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsLineItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        self._x = x
        self._y = y
        self._name = name
        self._color = color
        self.adjacentVertexList = list()

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtGui.QColor(VERTEX_COLOR))
        painter.drawEllipse(self._x, self._y, VERTEX_SIZE, VERTEX_SIZE)
        painter.drawText(self.rect(), QtCore.Qt.AlignCenter, str(self._name))
        painter.setBrush(QtCore.Qt.NoBrush)

    def addAdjacentVertex(self, vertex):
        self.adjacentVertexList.append(vertex)

    def removeAdjacentVertex(self, vertex):
        if vertex in self.adjacentVertexList:
            self.adjacentVertexList.remove(vertex)

    def getName(self):
        return self._name
