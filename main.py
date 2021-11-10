from PyQt5 import QtCore, QtGui, QtWidgets
from utils.defines import *
import sys


class Vertex:
    def __init__(self, x: int, y: int, item: QtWidgets.QGraphicsEllipseItem, name: str, color: str):
        super(Vertex, self).__init__()
        self._x = x
        self._y = y
        self._name = name
        self._color = color
        self.adjacentVertexList = list()
        self.graphicsItem = item

    def getPos(self):
        return self._x, self._y

    def getName(self):
        return self._name


class SceneView(QtWidgets.QGraphicsView):
    def __init__(self):
        super(SceneView, self).__init__()
        # Graph utils
        self._vertexList = list()
        self._vergeList = list()

        # Scene settings
        self._scene = QtWidgets.QGraphicsScene(self)
        self._scene.setSceneRect(0, 0, FIELD_WIDTH, FIELD_HEIGHT)

        # View settings
        self.setScene(self._scene)
        self.setFixedSize(FIELD_WIDTH, FIELD_HEIGHT)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setStyleSheet('background-color: #151515;')
        self.setMouseTracking(True)

        # brush = QtGui.QBrush(QtGui.QColor(VERTEX_COLOR))
        # pen = QtGui.QPen(QtGui.QColor(FIELD_COLOR))
        # ellipse = self._scene.addEllipse(100, 100, VERTEX_SIZE, VERTEX_SIZE, pen, brush)
        # ellipse.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            circle = QtWidgets.QGraphicsEllipseItem(event.pos().x(), event.pos().y(), VERTEX_SIZE, VERTEX_SIZE)
            circle.setBrush(QtGui.QColor(VERTEX_COLOR))
            self._scene.addItem(circle)
            circle.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)

        elif event.button() == QtCore.Qt.RightButton:
            item = self._scene.itemAt(event.pos().x(), event.pos().y(), QtGui.QTransform())

            if item is not None:
                self._scene.removeItem(item)


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Window settings
        self._width = WIN_WIDTH
        self._height = WIN_HEIGHT
        self._view = SceneView()

        self.setWindowTitle("Graph Visualizer")
        self.setFixedSize(WIN_WIDTH, WIN_HEIGHT)
        self.setStyleSheet('background-color: #282828;')

        self.button = QtWidgets.QPushButton('text', self)                           # delete after
        self.button.setFixedSize(395, 1200)

        # Layout management
        self._mainWidget = QtWidgets.QWidget()
        self._mainLayout = QtWidgets.QHBoxLayout()

        self._sceneLayout = QtWidgets.QVBoxLayout()
        self._menuLayout = QtWidgets.QVBoxLayout()

        self._sceneLayout.addWidget(self._view)
        self._menuLayout.addWidget(self.button)                                      # delete after

        self._mainLayout.addLayout(self._sceneLayout)
        self._mainLayout.addLayout(self._menuLayout)

        self._mainWidget.setLayout(self._mainLayout)
        self.setCentralWidget(self._mainWidget)


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
