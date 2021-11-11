from PyQt5.QtGui import QPainter, QTransform, QColor, QPen
from PyQt5.QtCore import Qt, QRectF, QPointF, QSizeF, QLineF
from PyQt5.QtWidgets import (QAction, QMenu, QApplication, QWidget, QHBoxLayout, QVBoxLayout,
                             QGraphicsView, QGraphicsScene, QPushButton,
                             QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsItem, QGraphicsLineItem, QMainWindow)
from utils.defines import *


class Vertex(QGraphicsEllipseItem):
    def __init__(self, x: int, y: int, name: str, color: str):
        super(Vertex, self).__init__(x, y, VERTEX_SIZE, VERTEX_SIZE)

        self.setPos(x, y)
        self.setBrush(QColor(color))
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        self.setFlag(QGraphicsLineItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        self._x = x
        self._y = y
        self._name = name
        self._color = color
        self.acceptHoverEvents()

    def hoverEnterEvent(self, event):
        self.setBrush(Qt.red)

    def hoverLeaveEvent(self, event):
        self.setBrush(QColor(VERTEX_COLOR))


class Verge(QGraphicsItem):

    def __init__(self, startItem, endItem, parent=None, scene=None):
        super().__init__(parent)

        self.startItem = startItem
        self.endItem = endItem

    def boundingRect(self):
        p1 = self.startItem.pos() + self.startItem.rect().center()
        p3 = self.endItem.pos() + self.endItem.rect().center()
        bounds = p3 - p1
        size = QSizeF(bounds.x(), bounds.y())
        return QRectF(p1, size)

    def paint(self, painter, option, widget=None):

        p1 = self.startItem.pos() + self.startItem.rect().center()
        p3 = self.endItem.pos() + self.endItem.rect().center()

        pen = QPen()
        pen.setWidth(VERGE_WIDTH)
        pen.setColor(Qt.white)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.isSelected():
            pen.setStyle(Qt.DashLine)
        else:
            pen.setStyle(Qt.SolidLine)

        painter.setPen(pen)
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

            # item = QGraphicsEllipseItem(0, 0, 50, 50)
            # item.setBrush(QColor(VERTEX_COLOR))
            # item.setFlags(QGraphicsItem.ItemIsMovable)

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
                    print(self._start.pos().x() + 25, self._start.pos().y() + 25, ' -> ', self._end.pos().x() + 25, self._end.pos().y() + 25)

                    # pen = QPen(Qt.white)
                    # pen.setWidth(VERGE_WIDTH)
                    # line = QGraphicsLineItem(self._start.pos().x() + 25, self._start.pos().y() + 25, self._end.pos().x() + 25, self._end.pos().y() + 25)
                    # line.setPen(pen)

                    verge = Verge(self._start, self._end)
                    self.scene.addItem(verge)

        super(View, self).mouseReleaseEvent(event)

    # def mouseMoveEvent(self, event):
    #     print('move')
    #     super(View, self).mouseMoveEvent(event)

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        # View settings
        self._view = View()

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