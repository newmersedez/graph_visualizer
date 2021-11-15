from PyQt5 import QtWidgets, QtGui, QtCore
from utils.defines import *
from classes.vertex import *
from math import sqrt, sin, cos, acos, pi, fabs, degrees, radians
from PyQt5.QtCore import qAbs

class Verge(QtWidgets.QGraphicsItem):

    def __init__(self, startVertex, endVertex, name, factor=None, parent=None):
        super().__init__(parent)

        # Verge variables
        self._startVertex = startVertex
        self._endVertex = endVertex
        self._weight = 1
        self._isDirection = False
        self._isWeight = False
        self._name = '\'' + name + '\''
        self._curveFactor = factor

    def toggleDirection(self):
        print('toggle in verge class')
        self._isDirection = not self._isDirection

    def isDirected(self):
        return self._isDirection

    def setWeight(self, weight):
        self._weight = weight
        self._isWeight = True

    def setFactor(self, factor):
        self._curveFactor = factor

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

        pointStart = start + self._startVertex.rect().center()
        pointEnd = end + self._endVertex.rect().center()

        factor = VERTEX_SIZE * self._curveFactor
        angle2 = radians(90) + angle
        point3X = ((pointEnd.x() + pointStart.x()) / 2)
        point3Y = ((pointEnd.y() + pointStart.y()) / 2)

        myPath = QtGui.QPainterPath(pointStart)
        myPath.cubicTo(QtCore.QPointF(point3X + factor * cos(-angle2), point3Y + factor * sin(-angle2)),
                       QtCore.QPointF(point3X + factor * cos(-angle2), point3Y + factor * sin(-angle2)),
                       pointEnd)

        pen = QtGui.QPen()
        pen.setColor(QtCore.Qt.white)
        pen.setWidth(VERGE_WIDTH)
        painter.setPen(pen)
        painter.drawPath(myPath)

        pen.setColor(QtCore.Qt.red)
        painter.setPen(pen)
        painter.drawPoint(QtCore.QPointF(point3X + 3.0/4.0 * factor * cos(-angle2), point3Y + 3.0/4.0 * factor * sin(-angle2)))

        print('center = (', point3X, point3Y, '), red point = (', point3X + factor * cos(-angle2),
              point3Y + factor * sin(-angle2), ')\n')

        # pen.setColor(QtGui.QColor(VERTEX_COLOR))
        # painter.setPen(pen)
        # painter.setFont(QtGui.QFont('Arial', 12))
        # painter.drawText(c2X + 0.8 * factor * cos(-angle2), c2Y + 0.8 * factor * sin(-angle2), self._name)

        #
        # if self._isDirection:
        #     startPoint = pointStart
        #
        #     endPoint = QtCore.QPointF(c2X + factor * 0.8 * cos(-angle2), c2Y + factor * 0.8 * sin(-angle2))
        #
        #     dx, dy = startPoint.x() - endPoint.x(), startPoint.y() - endPoint.y()
        #     length = sqrt(dx ** 2 + dy ** 2)
        #     normX, normY = dx / length, dy / length
        #     perpX = -normY
        #     perpY = normX
        #
        #     leftX = endPoint.x() + ARROW_SIZE * normX + ARROW_SIZE * perpX
        #     leftY = endPoint.y() + ARROW_SIZE * normY + ARROW_SIZE * perpY
        #     rightX = endPoint.x() + ARROW_SIZE * normX - ARROW_SIZE * perpX
        #     rightY = endPoint.y() + ARROW_SIZE * normY - ARROW_SIZE * perpY
        #
        #     point2 = QtCore.QPointF(leftX, leftY)
        #     point3 = QtCore.QPointF(rightX, rightY)
        #
        #     newPen = QtGui.QPen()
        #     newPen.setColor(QtGui.QColor(VERTEX_COLOR))
        #     newPen.setWidth(VERGE_WIDTH)
        #     painter.setPen(newPen)
        #     painter.drawPolygon(point2, endPoint, point3)
        #
        # if self._isWeight:
        #     start_x = (pointEnd.x() + pointStart.x()) / 2
        #     start_y = ((pointEnd.y() + pointStart.y()) / 2) - VERTEX_SIZE / 4
        #     point = QtCore.QPointF(start_x, start_y)
        #
        #     newPen = QtGui.QPen()
        #     newPen.setColor(QtGui.QColor(VERTEX_COLOR))
        #     painter.setPen(newPen)
        #     painter.setFont(QtGui.QFont('Arial', 12))
        #     painter.drawText(point, self._name + ': ' + str(self._weight))

    def getStartVertex(self):
        return self._startVertex

    def getEndVertex(self):
        return self._endVertex
