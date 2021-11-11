from PyQt5.QtGui import QPainter, QTransform, QColor, QPen
from PyQt5.QtCore import Qt, QRectF, QPointF, QSizeF, QLineF
from PyQt5.QtWidgets import (QAction, QMenu, QApplication, QWidget, QHBoxLayout, QVBoxLayout,
                             QGraphicsView, QGraphicsScene, QPushButton,
                             QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsItem, QGraphicsLineItem, QMainWindow)
from utils.defines import *
from math import sqrt, sin, cos, acos, pi


class Vertex(QGraphicsEllipseItem):
    def __init__(self, x: int, y: int, name: str, color: str):
        super(Vertex, self).__init__(x, y, VERTEX_SIZE, VERTEX_SIZE)

        self.setPos(x, y)
        self.setBrush(QColor(color))
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        self.setFlag(QGraphicsLineItem.ItemSendsGeometryChanges)
        self._x = x
        self._y = y
        self._name = name
        self._color = color
        self.acceptHoverEvents()

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(VERTEX_COLOR))
        painter.drawEllipse(self._x, self._y, VERTEX_SIZE, VERTEX_SIZE)
        painter.setBrush(Qt.NoBrush)


class Verge(QGraphicsItem):

    def __init__(self, startItem, endItem, parent=None, scene=None):
        super().__init__(parent)

        self.startItem = startItem
        self.endItem = endItem
        self.pen = QPen()

        self.pen.setWidth(VERGE_WIDTH)
        self.pen.setColor(Qt.white)

    def boundingRect(self):
        start_x, start_y = self.startItem.pos().x(), self.startItem.pos().y()
        end_x, end_y = self.endItem.pos().x(), self.endItem.pos().y()

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

        start = QPointF(start_x, start_y)
        end = QPointF(end_x, end_y)

        p1 = start + self.startItem.rect().center()
        p3 = end + self.endItem.rect().center()

        bounds = p3 - p1
        size = QSizeF(bounds.x(), bounds.y())
        return QRectF(p1, size)

    def paint(self, painter, option, widget=None):
        start_x, start_y = self.startItem.pos().x(), self.startItem.pos().y()
        end_x, end_y = self.endItem.pos().x(), self.endItem.pos().y()

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

        start = QPointF(start_x, start_y)
        end = QPointF(end_x, end_y)

        p1 = start + self.startItem.rect().center()
        p3 = end + self.endItem.rect().center()

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(self.pen)
        painter.drawLine(QLineF(p1, p3))
        painter.setBrush(Qt.NoBrush)


class View(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, FIELD_WIDTH, FIELD_HEIGHT)
        self.setStyleSheet('background-color: #202020;')
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setFixedSize(FIELD_WIDTH, FIELD_HEIGHT)

        self._start = None
        self._end = None

    def contextMenuEvent(self, e):
        pos = e.pos()
        mnu = QMenu()
        mnu.addAction('Add vertex').setObjectName('add vertex')
        mnu.addAction('Delete vertex').setObjectName('delete vertex')
        mnu.addAction('Set verge wight').setObjectName('delete vertex')
        mnu.addAction('Toggle direction').setObjectName('toggle direction')
        mnu.addAction('Delete verge').setObjectName('delete verge')
        mnu.addAction('Clear all').setObjectName('clear all')
        ret = mnu.exec_(self.mapToGlobal(pos))
        if not ret:
            return
        obj = ret.objectName()
        if obj == 'add vertex':
            item = Vertex(0, 0, 'name', VERTEX_COLOR)
            self.scene.addItem(item)
            item.setPos(self.mapToScene(pos))

        elif obj == 'delete vertex':
            pos_x, pos_y = e.pos().x(), e.pos().y()
            item = self.scene.itemAt(pos_x, pos_y, QTransform())
            if item is not None:
                self.scene.removeItem(item)

        elif obj == 'clear all':
            for item in self.scene.items():
                self.scene.removeItem(item)

    def resizeEvent(self, e):
        w, h = self.viewport().width(), self.viewport().height()
        self.setSceneRect(0, 0, w, h)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            pos_x, pos_y = event.pos().x(), event.pos().y()
            item = self.scene.itemAt(pos_x, pos_y, QTransform())

            if item is not None:
                self._start = item
        super(View, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            pos_x, pos_y = event.pos().x(), event.pos().y()
            item = self.scene.itemAt(pos_x, pos_y, QTransform())

            if item is not None:
                self._end = item
                if self._start.type() == 4 and self._end.type() == 4:
                    verge = Verge(self._start, self._end)
                    self.scene.addItem(verge)

        super(View, self).mouseReleaseEvent(event)


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        # View settings
        self._view = View()
        self._view.viewport().repaint()

        # Window settings
        self.setFixedSize(WIN_WIDTH, WIN_HEIGHT)
        self.setWindowTitle('Graph Visualizer')
        self.setStyleSheet('background-color: #303030;')
        self.setCentralWidget(self._view)

        # Layout management
        self._mainWidget = QWidget()
        self._mainLayout = QHBoxLayout()

        self._sceneLayout = QVBoxLayout()
        self._menuLayout = QVBoxLayout()

        self._sceneLayout.addWidget(self._view)

        self._mainLayout.addLayout(self._sceneLayout)
        self._mainLayout.addLayout(self._menuLayout)

        self._mainWidget.setLayout(self._mainLayout)
        self.setCentralWidget(self._mainWidget)

        self.initUI()

    def initUI(self):
        button1 = QPushButton('Change color theme', self)
        button1.setFixedSize(395, 100)

        button2 = QPushButton('Create vertex', self)
        button2.setFixedSize(395, 100)

        button3 = QPushButton('Delete vertex', self)
        button3.setFixedSize(395, 100)

        self._menuLayout.addWidget(button1)
        self._menuLayout.addWidget(button2)
        self._menuLayout.addWidget(button3)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())