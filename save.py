# from classes.window import *
# import sys
#
# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     window = Window()
#     window.show()
#     sys.exit(app.exec())
#

# from PyQt5 import QtGui, QtCore, QtWidgets
# from classes.window import *
# import sys
#
# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     window = Window()
#     window.show()
#     sys.exit(app.exec())

from PyQt5 import QtCore, QtGui, QtWidgets


class Verge(QtWidgets.QGraphicsLineItem):
    def __init__(self, start, p2):
        super().__init__()
        self.start = start
        self.end = None
        self._line = QtCore.QLineF(start.scenePos(), p2)
        self.setLine(self._line)

    def controlPoints(self):
        return self.start, self.end

    def setP2(self, p2):
        self._line.setP2(p2)
        self.setLine(self._line)

    def setStart(self, start):
        self.start = start
        self.updateLine()

    def setEnd(self, end):
        self.end = end
        self.updateLine(end)

    def updateLine(self, source):
        if source == self.start:
            self._line.setP1(source.scenePos())
        else:
            self._line.setP2(source.scenePos())
        self.setLine(self._line)


class ControlPoint(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, parent, onLeft):
        super().__init__(-5, -5, 10, 10, parent)
        self.onLeft = onLeft
        self.lines = []
        # this flag **must** be set after creating self.lines!
        self.setFlags(self.ItemSendsScenePositionChanges)

    def addLine(self, lineItem):
        for existing in self.lines:
            if existing.controlPoints() == lineItem.controlPoints():
                # another line with the same control points already exists
                return False
        self.lines.append(lineItem)
        return True

    def removeLine(self, lineItem):
        for existing in self.lines:
            if existing.controlPoints() == lineItem.controlPoints():
                self.scene().removeItem(existing)
                self.lines.remove(existing)
                return True
        return False

    def itemChange(self, change, value):
        for line in self.lines:
            line.updateLine(self)
        return super().itemChange(change, value)


class Vertex(QtWidgets.QGraphicsItem):
    pen = QtGui.QPen(QtCore.Qt.red, 2)
    brush = QtGui.QBrush(QtGui.QColor(31, 176, 224))
    controlBrush = QtGui.QBrush(QtGui.QColor(214, 13, 36))
    rect = QtCore.QRectF(0, 0, 100, 100)

    def __init__(self, left=False, right=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFlags(self.ItemIsMovable)

        self.controls = []

        for onLeft, create in enumerate((right, left)):
            if create:
                control = ControlPoint(self, onLeft)
                self.controls.append(control)
                control.setPen(self.pen)
                control.setBrush(self.controlBrush)
                if onLeft:
                    control.setX(100)
                control.setY(35)

    def boundingRect(self):
        adjust = self.pen.width() / 2
        return self.rect.adjusted(-adjust, -adjust, adjust, adjust)

    def paint(self, painter, option, widget=None):
        painter.save()
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawRoundedRect(self.rect, 4, 4)
        painter.restore()


class Scene(QtWidgets.QGraphicsScene):
    startItem = newVerge = None

    def controlPointAt(self, pos):
        mask = QtGui.QPainterPath()
        mask.setFillRule(QtCore.Qt.WindingFill)
        for item in self.items(pos):
            if mask.contains(pos):
                # ignore objects hidden by others
                return
            if isinstance(item, ControlPoint):
                return item
            if not isinstance(item, Verge):
                mask.addPath(item.shape().translated(item.scenePos()))

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            item = self.controlPointAt(event.scenePos())
            if item:
                self.startItem = item
                self.newVerge = Verge(item, event.scenePos())
                self.addItem(self.newVerge)
                return
            else:
                item = self.itemAt(event.pos().x(), event.pos().y(), QtGui.QTransform())
                if item is None:
                    self.addItem(Vertex(left=True))
        elif event.button() == QtCore.Qt.RightButton:
            item = self.itemAt(event.pos().x(), event.pos().y(), QtGui.QTransform())
            if item is not None:
                self.removeItem(item)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.newVerge:
            item = self.controlPointAt(event.scenePos())
            if (item and item != self.startItem and
                self.startItem.onLeft != item.onLeft):
                    p2 = item.scenePos()
            else:
                p2 = event.scenePos()
            self.newVerge.setP2(p2)
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.newVerge:
            item = self.controlPointAt(event.scenePos())
            if item and item != self.startItem:
                self.newVerge.setEnd(item)
                if self.startItem.addLine(self.newVerge):
                    item.addLine(self.newVerge)
                else:
                    # delete the Verge if it exists; remove the following
                    # line if this feature is not required
                    self.startItem.removeLine(self.newVerge)
                    self.removeItem(self.newVerge)
            else:
                self.removeItem(self.newVerge)
        self.startItem = self.newVerge = None
        super().mouseReleaseEvent(event)


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.scene = Scene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setScene(self.scene)
        self.setFixedSize(1000, 1000)
        self.view.setRenderHints(QtGui.QPainter.Antialiasing)
        self.setCentralWidget(self.view)
        self.show()

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    # scene = Scene()
    #
    # scene.addItem(Vertex(left=True))
    # scene.addItem(Vertex(left=True))
    #
    # scene.addItem(Vertex(right=True))
    # scene.addItem(Vertex(right=True))
    #
    # scene.addItem(Vertex(right=True))
    # scene.addItem(Vertex(right=True))
    #
    # view = QtWidgets.QGraphicsView(scene)
    # view.setRenderHints(QtGui.QPainter.Antialiasing)
    #
    # view.show()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


