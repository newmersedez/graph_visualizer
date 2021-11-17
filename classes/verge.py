from classes.vertex import *
from math import sqrt, sin, cos, acos, pi, radians


class Verge(QtWidgets.QGraphicsItem):

    def __init__(self, startVertex, endVertex, name, weight=1, direction=False, factor=None, parent=None):
        super().__init__(parent)

        # Verge variables
        self._startVertex = startVertex
        self._endVertex = endVertex
        self._name = name
        self._weight = weight
        self._curveFactor = factor
        self._isDirection = direction

        if self._weight == 1:
            self._isWeight = False
        else:
            self._isWeight = True

    def toggleDirection(self):
        self._isDirection = not self._isDirection

    def isDirected(self):
        return self._isDirection

    def setWeight(self, weight):
        self._weight = weight
        self._isWeight = True

    def getStartVertex(self):
        return self._startVertex

    def getEndVertex(self):
        return self._endVertex

    def getName(self):
        return self._name

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
        # Calculate start and end positions
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

        offset = 1.1
        start_x += VERTEX_SIZE * offset / 2 * cos(angle)
        start_y -= VERTEX_SIZE * offset / 2 * sin(angle)
        end_x -= VERTEX_SIZE * offset / 2 * cos(angle)
        end_y += VERTEX_SIZE * offset / 2 * sin(angle)

        pointStart = QtCore.QPointF(start_x, start_y) + self._startVertex.rect().center()
        pointEnd = QtCore.QPointF(end_x, end_y) + self._endVertex.rect().center()

        # Calculate bezier curves for loop
        if self._startVertex == self._endVertex:

            pointStartX = self._startVertex.x() + VERTEX_SIZE * 0.5
            pointStartY = self._startVertex.y()
            pointStart = QtCore.QPointF(pointStartX, pointStartY)

            pointEndX = self._startVertex.x()
            pointEndY = self._startVertex.y() + VERTEX_SIZE * 0.5
            pointEnd = QtCore.QPointF(pointEndX, pointEndY)

            point1X = pointStart.x() - VERTEX_SIZE * 0.5
            point1Y = pointStart.y() - VERTEX_SIZE * 2

            point2X = pointEnd.x() - VERTEX_SIZE * 2
            point2Y = pointEnd.y() - VERTEX_SIZE * 0.5

            myPath = QtGui.QPainterPath(pointStart)
            myPath.cubicTo(QtCore.QPointF(point1X, point1Y), QtCore.QPointF(point2X, point2Y), pointEnd)

            pen = QtGui.QPen()
            pen.setColor(QtCore.Qt.white)
            pen.setWidth(VERGE_WIDTH)
            painter.setPen(pen)
            painter.drawPath(myPath)

            pen.setColor(QtGui.QColor(VERTEX_COLOR))
            painter.setPen(pen)
            painter.setFont(QtGui.QFont('Arial', 14))

            # Update factor for text and arrow drawing
            painter.drawText(pointEnd.x() - VERTEX_SIZE, pointStart.y() - VERTEX_SIZE, '\'' + self._name + '\'')

            # Verge direction
            if self._isDirection:
                endPoint = QtCore.QPointF(pointEndX, pointEndY)
                dx, dy = pointStart.x() - endPoint.x(), pointStart.y() - endPoint.y()
                length = sqrt(dx ** 2 + dy ** 2) / 1.2

                normX, normY = dx / length, dy / length
                perpX, perpY = normY, -normX

                leftX = endPoint.x() + ARROW_SIZE * normX + ARROW_SIZE * perpX - 7
                leftY = endPoint.y() + ARROW_SIZE * normY + ARROW_SIZE * perpY + 3
                rightX = endPoint.x() + ARROW_SIZE * normX - ARROW_SIZE * perpX - 20
                rightY = endPoint.y() + ARROW_SIZE * normY - ARROW_SIZE * perpY + 10

                point2 = QtCore.QPointF(leftX, leftY)
                point3 = QtCore.QPointF(rightX, rightY)

                newBrush = QtGui.QBrush()
                newBrush.setColor(QtCore.Qt.blue)
                painter.setBrush(newBrush)
                painter.drawPoint(endPoint)
                painter.drawPolygon(point2, point3, endPoint)

            # Verge weight display
            if self._isWeight:
                newPen = QtGui.QPen()
                newPen.setColor(QtGui.QColor(VERTEX_COLOR))
                painter.setPen(newPen)
                painter.setFont(QtGui.QFont('Arial', 14))
                textOffset = VERTEX_SIZE / 4
                painter.drawText(pointEnd.x() - VERTEX_SIZE, pointStart.y() - VERTEX_SIZE,
                                 '\'' + self._name + '\': ' + str(self._weight))

        # Calculate bezier curve loop default verge
        else:
            point3X = ((pointEnd.x() + pointStart.x()) / 2)
            point3Y = ((pointEnd.y() + pointStart.y()) / 2)
            factor = VERTEX_SIZE * self._curveFactor
            angle2 = radians(90) + angle

            myPath = QtGui.QPainterPath(pointStart)
            myPath.cubicTo(QtCore.QPointF(point3X + factor * cos(-angle2), point3Y + factor * sin(-angle2)),
                           QtCore.QPointF(point3X + factor * cos(-angle2), point3Y + factor * sin(-angle2)),
                           pointEnd)

            pen = QtGui.QPen()
            pen.setColor(QtCore.Qt.white)
            pen.setWidth(VERGE_WIDTH)
            painter.setPen(pen)
            painter.drawPath(myPath)

            # Update factor for text and arrow drawing
            pen.setColor(QtGui.QColor(VERTEX_COLOR))
            painter.setPen(pen)
            painter.setFont(QtGui.QFont('Arial', 14))

            factor *= 3.0 / 4.0
            textOffset = VERTEX_SIZE / 4
            painter.drawText(point3X + factor * cos(-angle2), point3Y + factor * sin(-angle2) - textOffset,
                             '\'' + self._name + '\'')

            # Verge direction
            if self._isDirection:
                endPoint = QtCore.QPointF(point3X + factor * cos(-angle2),  point3Y + factor * sin(-angle2))
                dx, dy = pointStart.x() - endPoint.x(), pointStart.y() - endPoint.y()
                length = sqrt(dx ** 2 + dy ** 2) / 1.2

                normX, normY = dx / length, dy / length
                perpX, perpY = -normY, normX

                leftX = endPoint.x() + ARROW_SIZE * normX + ARROW_SIZE * perpX
                leftY = endPoint.y() + ARROW_SIZE * normY + ARROW_SIZE * perpY
                rightX = endPoint.x() + ARROW_SIZE * normX - ARROW_SIZE * perpX
                rightY = endPoint.y() + ARROW_SIZE * normY - ARROW_SIZE * perpY

                point2 = QtCore.QPointF(leftX, leftY)
                point3 = QtCore.QPointF(rightX, rightY)

                newBrush = QtGui.QBrush()
                newBrush.setColor(QtGui.QColor(VERTEX_COLOR))
                painter.setBrush(newBrush)
                painter.drawPolygon(point2, endPoint, point3)

            # Verge weight display
            if self._isWeight:
                newPen = QtGui.QPen()
                newPen.setColor(QtGui.QColor(VERTEX_COLOR))
                painter.setPen(newPen)
                painter.setFont(QtGui.QFont('Arial', 14))
                textOffset = VERTEX_SIZE / 4
                painter.drawText(point3X + factor * cos(-angle2), point3Y + factor * sin(-angle2) - textOffset,
                                 '\'' + self._name  + '\': ' + str(self._weight))
