from PyQt5 import QtWidgets, QtGui, QtCore
from utils.defines import VERTEX_SIZE


class Vertex(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, x: int, y: int, name: str, color: str):
        super(Vertex, self).__init__(x, y, VERTEX_SIZE, VERTEX_SIZE)
        self.setPos(x, y)
        self.setBrush(QtGui.QColor(color))
        self.setFlag(QtWidgets.QGraphicsEllipseItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)
        self._x = x
        self._y = y
        self._name = name
        self._color = color

    def getName(self):
        return self._name

    def hoverEnterEvent(self, event):
        self.setBrush(QtGui.QBrush(QtCore.Qt.red))
        super(Vertex, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(QtGui.QBrush(QtGui.QColor(self._color)))
        super(Vertex, self).hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            print('clicked')