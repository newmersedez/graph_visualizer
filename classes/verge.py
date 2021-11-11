from PyQt5 import QtWidgets, QtGui, QtCore
from utils.defines import *
from classes.vertex import *
from math import sqrt, sin, cos, acos, pi


class Verge(QtWidgets.QGraphicsItem):

    def __init__(self, startVertex, endVertex, parent=None):
        super().__init__(parent)

        # Verge variables
        self.startVertex = startVertex
        self.endVertex = endVertex

    def boundingRect(self):
        start_x, start_y = self.startVertex.pos().x(), self.startVertex.pos().y()
        end_x, end_y = self.endVertex.pos().x(), self.endVertex.pos().y()

        a = end_x - start_x
        b = start_y - end_y
        c = sqrt(a ** 2 + b ** 2)
        angle = 0

        if end_y < start_y and c != 0:
            angle = acos(a / c)
        elif end_y >= start_y and c != 0:
            angle = 2 * pi - acos(a / c)

        start_x += VERTEX_SIZE / 2 * cos(angle)
        start_y -= VERTEX_SIZE / 2 * sin(angle)
        end_x -= VERTEX_SIZE / 2 * cos(angle)
        end_y += VERTEX_SIZE / 2 * sin(angle)

        start = QtCore.QPointF(start_x, start_y)
        end = QtCore.QPointF(end_x, end_y)

        p1 = start + self.startVertex.rect().center()
        p3 = end + self.endVertex.rect().center()

        bounds = p3 - p1
        size = QtCore.QSizeF(bounds.x(), bounds.y())
        return QtCore.QRectF(p1, size)

    def paint(self, painter, option, widget=None):

        start_x, start_y = self.startVertex.pos().x(), self.startVertex.pos().y()
        end_x, end_y = self.endVertex.pos().x(), self.endVertex.pos().y()

        a = end_x - start_x
        b = start_y - end_y
        c = sqrt(a ** 2 + b ** 2)
        angle = 0

        if end_y < start_y and c != 0:
            angle = acos(a / c)
        elif end_y >= start_y and c != 0:
            angle = 2 * pi - acos(a / c)

        start_x += VERTEX_SIZE / 2 * cos(angle)
        start_y -= VERTEX_SIZE / 2 * sin(angle)
        end_x -= VERTEX_SIZE / 2 * cos(angle)
        end_y += VERTEX_SIZE / 2 * sin(angle)

        start = QtCore.QPointF(start_x, start_y)
        end = QtCore.QPointF(end_x, end_y)

        p1 = start + self.startVertex.rect().center()
        p3 = end + self.endVertex.rect().center()

        pen = QtGui.QPen()
        pen.setWidth(VERGE_WIDTH)
        pen.setColor(QtCore.Qt.white)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(pen)
        painter.drawLine(QtCore.QLineF(p1, p3))
        painter.setBrush(QtCore.Qt.NoBrush)

    def getStartVertex(self):
        return self.startVertex

    def getEndVertex(self):
        return self.endVertex
