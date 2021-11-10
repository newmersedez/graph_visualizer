from PyQt5 import QtCore, QtGui, QtWidgets


class Vertex(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, x: int, y: int, name: str, color: str):
        super(Vertex, self).__init__()
        self._x = x
        self._y = y
        self._name = name
        self._color = color
        self.adjacentVertexList = list()

    def getPos(self):
        return self._x, self._y

    def getName(self):
        return self._name