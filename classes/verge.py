from PyQt5 import QtWidgets, QtGui, QtCore
from utils.defines import *
from classes.vertex import *
from math import sqrt, sin, cos, acos, pi, atan2


class Verge(QtWidgets.QGraphicsItem):

    def __init__(self, startVertex, endVertex, parent=None):
        super().__init__(parent)

        # Verge variables
        self._startVertex = startVertex
        self._endVertex = endVertex
        self._weight = 1
        self._isDirection = False
        self._isWeight = False

    def toggleDirection(self):
        print('toggle in verge class')
        self._isDirection = not self._isDirection

    def isDirected(self):
        return self._isDirection

    def setWeight(self, weight):
        self._weight = weight
        self._isWeight = True

    def boundingRect(self):
        start_x, start_y = self._startVertex.pos().x(), self._startVertex.pos().y()
        end_x, end_y = self._endVertex.pos().x(), self._endVertex.pos().y()

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

        p1 = start + self._startVertex.rect().center()
        p3 = end + self._endVertex.rect().center()

        bounds = p3 - p1
        size = QtCore.QSizeF(bounds.x(), bounds.y())
        return QtCore.QRectF(p1, size)

    def paint(self, painter, option, widget=None):

        start_x, start_y = self._startVertex.pos().x(), self._startVertex.pos().y()
        end_x, end_y = self._endVertex.pos().x(), self._endVertex.pos().y()

        a = end_x - start_x
        b = start_y - end_y
        c = sqrt(a ** 2 + b ** 2)
        angle = 0

        if end_y < start_y and c != 0:
            angle = acos(a / c)
        elif end_y >= start_y and c != 0:
            angle = 2 * pi - acos(a / c)

        start_x += VERTEX_SIZE * 1.2 / 2 * cos(angle)
        start_y -= VERTEX_SIZE * 1.2 / 2 * sin(angle)
        end_x -= VERTEX_SIZE * 1.2 / 2 * cos(angle)
        end_y += VERTEX_SIZE * 1.2 / 2 * sin(angle)

        start = QtCore.QPointF(start_x, start_y)
        end = QtCore.QPointF(end_x, end_y)

        p1 = start + self._startVertex.rect().center()
        p3 = end + self._endVertex.rect().center()

        pen = QtGui.QPen()
        pen.setWidth(VERGE_WIDTH)
        pen.setColor(QtCore.Qt.white)
        painter.setPen(pen)

        painter.setPen(pen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.drawLine(QtCore.QLineF(p1, p3))
        painter.setBrush(QtCore.Qt.NoBrush)

        if self._isDirection:
            startPoint = p1
            endPoint = QtCore.QPointF(p3.x() + VERTEX_SIZE * 0.25 / 2 * cos(angle),
                                      p3.y() - VERTEX_SIZE * 0.25 / 2 * sin(angle))

            dx, dy = startPoint.x() - endPoint.x(), startPoint.y() - endPoint.y()
            length = sqrt(dx ** 2 + dy ** 2)
            normX, normY = dx / length, dy / length
            perpX = -normY
            perpY = normX

            leftX = endPoint.x() + ARROW_SIZE * normX + ARROW_SIZE * perpX
            leftY = endPoint.y() + ARROW_SIZE * normY + ARROW_SIZE * perpY
            rightX = endPoint.x() + ARROW_SIZE * normX - ARROW_SIZE * perpX
            rightY = endPoint.y() + ARROW_SIZE * normY - ARROW_SIZE * perpY

            point2 = QtCore.QPointF(leftX, leftY)
            point3 = QtCore.QPointF(rightX, rightY)

            newPen = QtGui.QPen()
            newPen.setColor(QtCore.Qt.white)
            newPen.setWidth(VERGE_WIDTH / 2)
            painter.setPen(newPen)
            painter.drawPolygon(point2, endPoint, point3)

        if self._isWeight:
            start_x = p1.x() + (p3.x() - p1.x()) / 2
            start_y = (p1.y() + (p3.y() - p1.y()) / 2) - VERTEX_SIZE / 4
            point = QtCore.QPointF(start_x, start_y)

            newPen = QtGui.QPen()
            newPen.setColor(QtGui.QColor(VERTEX_COLOR))
            painter.setPen(newPen)
            painter.setFont(QtGui.QFont('Arial', 17))
            painter.drawText(point, str(self._weight))

    def getStartVertex(self):
        return self._startVertex

    def getEndVertex(self):
        return self._endVertex
